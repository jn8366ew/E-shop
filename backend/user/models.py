from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import cart
import user_profile

# we define and expand different fields of user model related to other models.
# Hence, we use BaseUserManager to customizing user model.
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # password hashed by set_password method
        user.set_password(password)
        user.save()

        # 1:1 Rel
        shopping_cart = cart.models.Cart(user=user)
        shopping_cart.save()

        # 1:1 Rel
        profile = user_profile.models.UserProfile(user=user)
        profile.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Everytime when a user create an account,
    # execute UserAccountManager.
    objects = UserAccountManager()


    # Associate with Djoser Endpoints
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
