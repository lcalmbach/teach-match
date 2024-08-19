from django.core.management.base import BaseCommand
from django.utils import timezone
from school_management.models import Substitution, SubstitutionStatus

class Command(BaseCommand):
    help = 'Update the status of Substitutions based on end_date'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        substitutions = Substitution.objects.filter(
    end_date__lt=today
    ).exclude(
        status=SubstitutionStatus.objects.get(name='abgeschlossen')
    )

        for substitution in substitutions:
            substitution.status = SubstitutionStatus.objects.get(name='abgeschlossen')
            substitution.save()
            print(substitution.id)

        self.stdout.write(self.style.SUCCESS('Successfully updated substitution statuses'))
