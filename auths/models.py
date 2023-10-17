from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Model
from django_resized import ResizedImageField
from safedelete.models import HARD_DELETE, SafeDeleteModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **kwargs: Any) -> Model:
        if not email or not password:
            raise ValueError("Need email and password")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email: str, password: str, **kwargs: Any) -> Model:
        kwargs.setdefault("is_superuser", False)
        kwargs.setdefault("is_staff", False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(
        self, email: str, password: str, **kwargs: Any
    ) -> Model:
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("role", 1)
        return self._create_user(email, password, **kwargs)


class RoleChoices(models.IntegerChoices):
    SuperAdmin = 1, "Super Admin"
    PendudukUser = 2, "Penduduk User"
    DesaAdmin = 3, "Desa Admin"
    DesaUser = 4, "Desa User"


class User(AbstractBaseUser, PermissionsMixin):
    _human_name = "Pengguna"

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=13, default="-")
    username = models.CharField(max_length=64, help_text="Full name")
    photo = ResizedImageField(
        size=[180, 320], upload_to="user", blank=True, null=True
    )
    address = models.TextField(null=True, blank=True)
    role = models.IntegerField(choices=RoleChoices.choices)
    desa = models.ForeignKey(
        "datamaster.Desa", on_delete=models.CASCADE, null=True, blank=True
    )

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role"]

    def __repr__(self) -> str:
        return self.username

    class Meta:
        db_table = "app_user"


class DesaJabatanChoices(models.IntegerChoices):
    KepalaDesa = 1, "Kepala Desa"
    KabagPemerintahan = 2, "Kabag Pelayanan Pemerintahan"
    KabagUmum = 3, "Kabag Pelayanan Umum"


class UserDesaProfile(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    jabatan = models.IntegerField(choices=DesaJabatanChoices.choices)

    def __repr__(self) -> str:
        return f"{self.user.username}-{self.jabatan}"

    class Meta:
        db_table = "app_user_desa_profile"
