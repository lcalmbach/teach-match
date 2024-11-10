from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Send a test email to check if email settings are correct"

    def handle(self, *args, **kwargs):
        # Define the test email details
        subject = "Test Email from Django"
        message = "This is a test email sent from the Django environment to verify email settings."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [
            "lcalmbach@gmail.com"
        ]  # Replace with the email address you want to send to
        try:
            send_mail(subject, message, from_email, recipient_list)
            self.stdout.write(self.style.SUCCESS("Test email sent successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send test email: {e}"))
