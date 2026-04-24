"""
Accounts Models: CustomUser, Address, SiteSettings, Tokens, Sessions
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user with e-commerce fields"""

    class UserType(models.TextChoices):
        CUSTOMER = 'customer', 'Xaridor'
        SELLER = 'seller', 'Sotuvchi'
        ADMIN = 'admin', 'Administrator'

    class AccountStatus(models.TextChoices):
        ACTIVE = 'active', 'Faol'
        INACTIVE = 'inactive', 'Nofaol'
        SUSPENDED = 'suspended', 'To\'xtatilgan'
        DELETED = 'deleted', 'O\'chirilgan'

    class Gender(models.TextChoices):
        MALE = 'male', 'Erkak'
        FEMALE = 'female', 'Ayol'
        OTHER = 'other', 'Boshqa'

    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    profile_image_url = models.ImageField(upload_to='profiles/', blank=True)
    user_type = models.CharField(max_length=10, choices=UserType.choices, default=UserType.CUSTOMER)
    account_status = models.CharField(max_length=10, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    customer_segment = models.CharField(max_length=50, blank=True)
    lifetime_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    loyalty_points = models.IntegerField(default=0)
    preferred_language = models.CharField(max_length=10, default='uz')
    timezone = models.CharField(max_length=50, default='Asia/Tashkent')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Address(models.Model):
    """User shipping/billing addresses"""

    class AddressType(models.TextChoices):
        SHIPPING = 'shipping', 'Yetkazish'
        BILLING = 'billing', 'To\'lov'
        BOTH = 'both', 'Ikkalasi'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=AddressType.choices, default=AddressType.BOTH)
    is_default = models.BooleanField(default=False)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=50, default="O'zbekiston")
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50, blank=True)
    street_address = models.TextField()
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Manzil'
        verbose_name_plural = 'Manzillar'

    def __str__(self):
        return f"{self.full_name} — {self.city}, {self.region}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='email_verification_tokens')
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class UserSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions')
    session_token = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    device_type = models.CharField(max_length=20, blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session: {self.user.username} ({self.ip_address})"


class SiteSettings(models.Model):
    """Singleton — site-wide settings"""
    site_name = models.CharField(max_length=100, default='NexGear')
    site_domain = models.CharField(max_length=100, default='nexgear.uz')
    contact_email = models.EmailField(default='info@nexgear.uz')
    contact_phone = models.CharField(max_length=20, default='+998 90 123 45 67')
    instagram_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Sayt Sozlamalari'
        verbose_name_plural = 'Sayt Sozlamalari'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton
        super().save(*args, **kwargs)
