# src/school_management/management/commands/import_teachers.py

import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from pathlib import Path

from school_management.models import Teacher, School


class Command(BaseCommand):
    help = 'Imports teachers from CSV file into Teacher model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=r'C:\Users\ssscal\dev\teach-match\src\data\untis\teachers.csv',
            help='Path to the CSV file containing teachers'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing teachers before import'
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
            count = Teacher.objects.count()
            if count > 0:
                self.stdout.write(
                    self.style.WARNING(f'Deleting {count} existing teachers...')
                )
                Teacher.objects.all().delete()

        # Import data
        self.import_teachers(rows)

    def display_preview(self, rows):
        """Display preview of data to be imported"""
        self.stdout.write(self.style.NOTICE('\nPreview of first 5 rows:'))
        for i, row in enumerate(rows, 1):
            self.stdout.write(f'\n--- Row {i} ---')
            for key, value in row.items():
                self.stdout.write(f'  {key}: {value}')

    def import_teachers(self, rows):
        """Import teachers from CSV rows"""
        created_count = 0
        updated_count = 0
        error_count = 0
        errors = []

        with transaction.atomic():
            for row_num, row in enumerate(rows, 1):
                teacher_id = None
                try:
                    # Extract data from CSV row
                    # Adjust column names based on your actual CSV structure
                    teacher_id = row.get('id', '').strip()
                    if not teacher_id:
                        raise ValueError('Missing teacher id')
                    
                    # Extract teacher information
                    full_name = row.get('surname', '').strip()
                    names = full_name.split(' ')
                    last_name = names[0] if names else ''
                    first_name = ' '.join(names[1:]) if len(names) > 1 else ''
                    
                    # Extract department/school information
                    dept_id = row.get('teacher_department', '').strip()
                    school = School.objects.filter(code=dept_id).first()
                       
                    
                    # Create or update
                    obj, created = Teacher.objects.update_or_create(
                        untis_id=teacher_id,
                        first_name=first_name,
                        last_name = last_name
                    )
                    
                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Created: {obj} ({teacher_id})')
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'↻ Updated: {obj} ({teacher_id})')
                        )

                except Exception as e:
                    error_count += 1
                    error_msg = f'Row {row_num} (ID: {teacher_id or "unknown"}): {str(e)}'
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
        Extract short name from Untis ID (e.g., TE_ABC -> ABC)
        
        Args:
            untis_id (str): The Untis ID string
            
        Returns:
            str: The extracted short name
        """
        if untis_id and '_' in untis_id:
            return untis_id.split('_', 1)[1]
        return untis_id