"""
Models to build and manage User profiles and settings
"""

# stdlib
from datetime import date
# django
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField
# app
from photos.models import PhotoBase

def profile_image(instance, filename: str) -> str:
    """
    Generate cast logo filename from cast slug
    """
    return f"users/{instance.user.username}/profile_image.{filename.split('.')[-1]}"

def user_photo(instance, filename: str) -> str:
    """
    Generate cast logo filename from cast slug
    """
    return f"users/{instance.profile.user.username}/photos/{filename}"

def age(born: date) -> int:
    """
    Returns how old a given date is as year int
    """
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class Profile(models.Model):
    """
    Profile info to add on top of the auth.User model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Public Profile
    image = ImageField(blank=True, upload_to=profile_image, verbose_name='Profile Photo')
    full_name = models.CharField(max_length=128, blank=True)
    alt = models.CharField(max_length=128, blank=True, verbose_name='Stage Name')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Public Bio')
    location = models.CharField(max_length=64, blank=True)

    # Social Buttons
    external_url = models.URLField(blank=True, verbose_name='Personal Website')
    facebook_url = models.URLField(blank=True, verbose_name='Facebook Page')
    twitter_user = models.CharField(max_length=15, blank=True, verbose_name='Twitter Username')
    instagram_user = models.CharField(max_length=30, blank=True, verbose_name='Instagram Username')

    # Visibility Flags
    show_email = models.BooleanField(default=False, verbose_name='Show Email on Profile')
    searchable = models.BooleanField(default=True, verbose_name="Searchable Profile")

    # Config
    email_confirmed = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)

    def save_from_form(self, form: 'SignUpForm'):
        """
        Assign profile attrs from new user form
        """
        self.birth_date = form.cleaned_data.get('birth_date')
        self.full_name = ' '.join([form.cleaned_data.get(key, '') for key in (
            'first_name',
            'last_name',
        )])
        self.alt = form.cleaned_data.get('alt')

    @property
    def name(self) -> str:
        """
        Returns the desired display name for the user
        """
        return self.alt or self.full_name

    @property
    def age(self) -> int:
        """
        Returns the user's age as an int
        """
        return age(self.birth_date)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<Profile {self.name} - {self.user.username}>'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Creates a profile for a new User model
    """
    if created:
        Profile.objects.create(user=instance) #pylint: disable=E1101
    instance.profile.save()

class Photo(PhotoBase):
    """
    Photos associated with a user profile
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
    image = ImageField(upload_to=user_photo)
