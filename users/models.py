from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class ThumbnailSizes(models.Model):
    """
    Sizes of the thumbnails
    """
    size = models.IntegerField(help_text='Height of the thumbnail is pixels')

    def __str__(self):
        return str(self.size)


class AccountTier(models.Model):
    """
    Account tiers
    """
    name = models.CharField(max_length=40, blank=False, unique=True, help_text='Name of tier')
    thumbnail_size = models.ManyToManyField(ThumbnailSizes, help_text='Avallable thumbnail sizes')
    original_file = models.BooleanField(help_text='Presence of the link to the originally uploaded file')
    expiring_links = models.BooleanField(help_text='Ability to generate expiring links')

    def __str__(self):
        return self.name
    
    @classmethod
    def get_default_pk(cls):
        """
        Return default account tier (Basic)
        """
        default_pk = cls.objects.get(name='Basic')
        return default_pk


class AccountManager(BaseUserManager):

    def create_user(self, username, password):
        if not username:
            raise ValueError('Users must have a username.')
        
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    account_tier = models.ForeignKey(AccountTier, on_delete=models.SET_NULL, null=True, default=AccountTier.get_default_pk)

    objects = AccountManager()

    USERNAME_FIELD = 'username'

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
