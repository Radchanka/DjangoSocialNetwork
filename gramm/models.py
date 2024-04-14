from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise ValueError('The Password field must be set and not empty')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    biography = models.TextField(blank=True)
    avatar = CloudinaryField('avatar', null=True, blank=True)
    profile_activation_token = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomUserManager()

    @property
    def followers_count(self):
        return Subscription.objects.filter(following=self).count()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)  # Поле для тегов
    likes = models.ManyToManyField(get_user_model(), through='Like', related_name='liked_posts',
                                   blank=True)

    def __str__(self):
        return f"Post {self.id} by {self.user.username}"


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.post}"


class Subscription(models.Model):
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"


class Image(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return f"Image {self.id} for Post {self.post.id}"
