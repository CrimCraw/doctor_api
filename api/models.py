from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.forms import ChoiceField
from django.utils.translation import gettext_lazy as _
from api.managers import UserManager
from django.core.mail import send_mail
from django.db import models



class User(AbstractBaseUser, PermissionsMixin):
    role =[
        ('user', 'User'),
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('manager', 'Manager'),
    ]
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True, )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    avatar = models.ImageField(upload_to='avatars/')
    roles = models.CharField(max_length=30, choices=role, default='user')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)



class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(_('speciality'), max_length=30, blank=True)
    experience = models.PositiveIntegerField(_('experience'), default=0)
    location = models.CharField(_('location'), max_length=30, blank=True)
    clinic_name = models.CharField(_('clinic name'), max_length=30, blank=True)
    consultation_fee = models.DecimalField(_('consultation'), max_digits=5, decimal_places=2)
    is_consultation_free = models.BooleanField(_('consultation free'), default=False)
    available_today = models.BooleanField(_('is available today'), default=False)
    rating_percentage = models.PositiveIntegerField(_('rating percentage'), default=0)
    patient_stories = models.PositiveIntegerField(_('patient stories'), default=0)

    def __str__(self):
        return self.speciality

    class Meta:
        verbose_name = _('Doctor')
        verbose_name_plural = _('Doctors')

class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=150, blank=True)
    img = models.ImageField(upload_to='news/')
    created_at = models.DateField(_('created at'), auto_now_add=True)

    def __str__(self):
        return self.title


class Date(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor')
    date = models.DateField(_('date'))
    time = models.TimeField(_('time'))
    status = models.CharField(max_length=15, choices=STATUS, default='pending')
    created_at = models.DateField(_('created at'), auto_now_add=True)

    objects = models.Manager()

    class Meta:
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f'{self.doctor} - {self.time}'