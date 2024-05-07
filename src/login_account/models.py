from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Benutzername", help_text='Der Benutzer, dem dieses Profil gehört.', related_name='profile')
    bio = models.TextField(max_length=500, verbose_name="Über mich", blank=True, help_text='eine kleine Zusammenfassung über mich.')
    location = models.CharField(max_length=30, verbose_name="Ort", blank=True, help_text='Der Ort, an dem ich mich befinde.')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()