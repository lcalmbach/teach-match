# src/school_management/management/commands/import_classes.py

import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from pathlib import Path

from school_management.models import SchoolClass, School


class Command(BaseCommand):
    help = 'Imports school classes from CSV file into SchoolClass model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=r'C:\Users\ssscal\dev\teach-match\src\data\untis\classes.csv',
            help='Path to the CSV file containing school classes'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing school classes before import'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Perform a dry run without saving to database'
        )

    def handle(self, *args, **options):
        file_path = Path(options['file'])
        clear_existing = options['clear']
        dry_run = options['dry_run']

        # Validate file exists
        if not file_path.exists():
            raise CommandError(f'CSV file not found: {file_path}')

        self.stdout.write(self.style.NOTICE(f'Reading CSV file: {file_path}'))

        # Read CSV file
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                
                if not rows:
                    raise CommandError('CSV file is empty')
                
                self.stdout.write(
                    self.style.SUCCESS(f'Found {len(rows)} rows in CSV')
                )
                
                # Display CSV headers for verification
                headers = reader.fieldnames
                self.stdout.write(
                    self.style.NOTICE(f'CSV columns: {", ".join(headers)}')
                )

        except Exception as e:
            raise CommandError(f'Error reading CSV file: {str(e)}')

        # Dry run - just display what would be imported
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be saved')
            )
            self.display_preview(rows[:5])
            return

        # Clear existing data if requested
        if clear_existing:
            count = SchoolClass.objects.count()
            if count > 0:
                self.stdout.write(
                    self.style.WARNING(f'Deleting {count} existing school classes...')
                )
                SchoolClass.objects.all().delete()

        # Import data
        self.import_classes(rows)

    def display_preview(self, rows):
        """Display preview of data to be imported"""
        self.stdout.write(self.style.NOTICE('\nPreview of first 5 rows:'))
        for i, row in enumerate(rows, 1):
            self.stdout.write(f'\n--- Row {i} ---')
            for key, value in row.items():
                self.stdout.write(f'  {key}: {value}')

    def import_classes(self, rows):
        """Import school classes from CSV rows"""
        created_count = 0
        updated_count = 0
        error_count = 0
        errors = []

        with transaction.atomic():
            for row_num, row in enumerate(rows, 1):
                class_room_id = None
                try:
                    # Extract data from CSV row
                    # Adjust column names based on your actual CSV structure
                    class_room_id = row.get('id', '').strip()
                    if not class_room_id:
                        raise ValueError('Missing class id')
                    
                    longname = row.get('longname', '').strip()
                    dept_id = row.get('class_department_id', '').strip()
                    school = School.objects.filter(code=dept_id).first()
                    
                    # Create or update
                    obj, created = SchoolClass.objects.update_or_create(
                        untis_id=class_room_id,
                        teacher_name=longname,
                        name=class_room_id,
                        school=school 
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Created: {obj} ({class_room_id})')
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'↻ Updated: {obj} ({class_room_id})')
                        )

                except Exception as e:
                    error_count += 1
                    error_msg = f'Row {row_num} (ID: {class_room_id or "unknown"}): {str(e)}'
                    errors.append(error_msg)
                    self.stdout.write(self.style.ERROR(f'✗ Error: {error_msg}'))

        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('Import completed!'))
        self.stdout.write(f'  Created: {created_count}')
        self.stdout.write(f'  Updated: {updated_count}')
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'  Errors: {error_count}'))
            self.stdout.write('\nError details:')
            for error in errors:
                self.stdout.write(self.style.ERROR(f'  - {error}'))
        self.stdout.write('='*60)

    def extract_short_name(self, untis_id):
        """
        Extract short name from Untis ID (e.g., CL_E01 -> E01)
        
        Args:
            untis_id (str): The Untis ID string
            
        Returns:
            str: The extracted short name
        """
        if untis_id and '_' in untis_id:
            return untis_id.split('_', 1)[1]
        return untis_id