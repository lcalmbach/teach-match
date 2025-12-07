from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from school_management.models import Substitution


class Command(BaseCommand):
    help = "Increase start_date and end_date of all Substitution entries by one year."

    def handle(self, *args, **options):
        substitutions = Substitution.objects.all()
        count = substitutions.count()

        self.stdout.write(f"Found {count} substitution entries…")

        updated = 0
        for sub in substitutions:
            # Add exactly one year using relativedelta (safer than timedelta)
            sub.start_date = sub.start_date + relativedelta(years=1)
            sub.end_date = sub.end_date + relativedelta(years=1)
            sub.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Updated {updated} substitution entries."))
