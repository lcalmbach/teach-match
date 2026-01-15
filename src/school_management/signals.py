from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_for_person(sender, instance, created, **kwargs):
    if created and not instance.user:
        # Create a User object
        user = User.objects.create_user(
            username=f"default_{instance.id}", password="defaultpassword"
        )
        instance.user = user
        instance.save()

        # Assign role based on some logic or external input
        role = instance.get_role()  # Assume get_role() method determines the role
        if role == "teacher":
            group = Group.objects.get(name="Teacher")
        elif role == "candidate":
            group = Group.objects.get(name="Candidate")
        elif role == "school-admin":
            group = Group.objects.get(name="School Admin")

        user.groups.add(group)
        user.save()
