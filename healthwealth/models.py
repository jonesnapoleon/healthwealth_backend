from django.db import models
from .managers import UserManager
from cloudinary.models import CloudinaryField
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
import uuid
from .constant import DOCUMENT_CATEGORY_CHOICES


phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Format: '+999999999'. Up to 15 digits allowed.",
)


class User(AbstractUser):

    username = None
    first_name = None
    last_name = None
    full_name = models.CharField(max_length=75)
    email = models.EmailField(_('Email address'), unique=True)

    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    phone_number = models.CharField("Phone number", validators=[phone_regex], max_length=17, blank=True, null=True, default=None)
    birth_date = models.DateField("Birth date", null=True, blank=True, default=None)
    address = models.TextField(null=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Document(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    uploaded_by = models.ForeignKey(to=User, related_name='uploaded_files', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    category = models.CharField(max_length=50, choices=DOCUMENT_CATEGORY_CHOICES, null=True)
    document_url = CloudinaryField('image')

    title = models.TextField(null=False)
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=7)

    description = models.TextField(null=True, default=None)

    issuername = models.CharField(max_length=100, null=True, default=None)
    issueddate = models.DateField(null=True, default=None)

    class Meta:
        verbose_name_plural = "Secured Health Document"


class DocumentAccess(models.Model):
    document = models.ForeignKey(to=Document, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    access_granted_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Document Access"
