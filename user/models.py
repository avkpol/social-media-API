from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=150, blank=True, null=True, unique=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    bio = models.TextField(blank=True)

    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()


# class UserProfile(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         primary_key=True,
#     )
#     profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
#     bio = models.TextField(blank=True)
#
#     def __str__(self):
#         return self.user.username if self.user else ""
#
#     def save(self, *args, **kwargs):
#         if not self.user.username:
#             self.user.username = self.user.username
#         super().save(*args, **kwargs)


class Follower(models.Model):
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_followers"
    )
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_following"
    )

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

