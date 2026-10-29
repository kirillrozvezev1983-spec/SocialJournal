from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # Дополнительные данные хранятся отдельно, а не в отдельных таблицах для каждого человека.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveSmallIntegerField()
    work = models.CharField(max_length=100)
    hobbies = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Пост {self.author.username}: {self.text[:30]}"

    def likes_count(self):
        # Число лайков считается запросом, отдельное поле не создаём.
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "post"], name="one_like_per_user_post")]

    def __str__(self):
        return f"{self.user.username} — {self.post_id}"
