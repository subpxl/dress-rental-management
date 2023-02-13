from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not email:
            raise ValueError('User must have an email')
        print("in model ", email, password)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    SELLER = 1
    CUSTOMER = 2
    AFFILIATE = 3
    STAFF = 4
    MANAGER = 5

    ROLE_CHOICE = (
        (SELLER, 'Seller'),
        (CUSTOMER, 'Customer'),
        (AFFILIATE, 'Affliate'),
        (STAFF, 'Affliate'),
        (MANAGER, 'Manager'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username']

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def full_name(self, app_label):
        return f'{self.first_name} {self.last_name}'

    def get_role(self):
        if self.role == 1:
            user_role = 'Seller'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role

# class Staff User
#     seller = fk


# class Customer User



class Address(models.Model):
    address = models.CharField(max_length=100)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def _str_(self):
        return f'{self.name}'