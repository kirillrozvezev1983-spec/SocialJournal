from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import RegisterForm, PostForm
from .models import Post, Like, Profile
from django.contrib.auth.models import User


def home(request):
    # Главная страница объясняет идею проекта и показывает несколько свежих постов.
    posts = Post.objects.select_related("author").all()[:3]
    return render(request, "network/home.html", {"posts": posts})


def interesting(request):
    posts_list = Post.objects.select_related("author").prefetch_related("likes")
    paginator = Paginator(posts_list, 8)
    page = paginator.get_page(request.GET.get("page"))
    liked_ids = []
    if request.user.is_authenticated:
        liked_ids = list(Like.objects.filter(user=request.user, post__in=page.object_list).values_list("post_id", flat=True))
    return render(request, "network/interesting.html", {"page": page, "posts": page.object_list, "liked_ids": liked_ids})


def register(request):
    if request.user.is_authenticated:
        return redirect("cabinet")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Аккаунт создан. Добро пожаловать!")
            return redirect("cabinet")
    else:
        form = RegisterForm()
    return render(request, "network/register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("cabinet")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("cabinet")
        messages.error(request, "Неверный логин или пароль. Попробуйте ещё раз.")
    else:
        form = AuthenticationForm()
    return render(request, "network/login.html", {"form": form})


@require_POST
def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def cabinet(request):
    profile, created = Profile.objects.get_or_create(user=request.user, defaults={"age": 0, "work": "Не указано", "hobbies": ""})
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Пост опубликован!")
            return redirect("cabinet")
    else:
        form = PostForm()
    posts = Post.objects.filter(author=request.user).select_related("author").prefetch_related("likes")
    return render(request, "network/cabinet.html", {"profile": profile, "form": form, "posts": posts})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Пост обновлён.")
            return redirect("cabinet")
    else:
        form = PostForm(instance=post)
    return render(request, "network/edit_post.html", {"form": form, "post": post})


@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, "Пост удалён.")
    return redirect("cabinet")


@require_POST
def toggle_like(request, post_id):
    if not request.user.is_authenticated:
        messages.info(request, "Чтобы ставить лайки, войдите в аккаунт.")
        return redirect("login")
    post = get_object_or_404(Post, id=post_id)
    if post.author_id == request.user.id:
        messages.info(request, "Нельзя ставить лайк собственному посту.")
        return redirect(request.POST.get("next", "interesting"))
    like = Like.objects.filter(user=request.user, post=post)
    if like.exists():
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)
    return redirect(request.POST.get("next", "interesting"))


def guest_room(request, username):
    guest = get_object_or_404(User, username=username)
    if request.user.is_authenticated and request.user.id == guest.id:
        return redirect("cabinet")
    profile, created = Profile.objects.get_or_create(user=guest, defaults={"age": 0, "work": "Не указано", "hobbies": ""})
    posts = Post.objects.filter(author=guest).select_related("author").prefetch_related("likes")
    liked_ids = []
    if request.user.is_authenticated:
        liked_ids = list(Like.objects.filter(user=request.user, post__in=posts).values_list("post_id", flat=True))
    return render(request, "network/guest_room.html", {"guest": guest, "profile": profile, "posts": posts, "liked_ids": liked_ids})
