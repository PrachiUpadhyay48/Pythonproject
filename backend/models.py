import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, help_text=_(
        'The groups this user belongs to. A user will get all permissions '
        'granted to each of their groups.'
    ),
                                    related_name='backend_user_permissions'  # Add a unique related_name
                                    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='backend_user_permissions'  # Add a unique related_name
    )


STATUS_CHOICES = [
    ('Open', 'Open'),
    ('In Progress', 'In Progress'),
    ('Closed', 'Closed'),
]


class Incident(models.Model):
    objects = None
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10)
    pin_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    incident_id = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        if not self.id or not self.city or not self.country:
            self.id = custom_generate_unique_id()  # Implement your custom logic to generate a unique ID
            city, country = get_city_and_country(self.pin_code)
            self.city = city or ''
            self.country = country or ''
        super().save(*args, **kwargs)
