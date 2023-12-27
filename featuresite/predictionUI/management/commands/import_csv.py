import csv
from django.core.management.base import BaseCommand
from predictionUI.models import EmployeeData

class Command(BaseCommand):
    help = 'Import data from a CSV file into EmployeeData model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                EmployeeData.objects.create(
                    name=row['name'],
                    age=row['age'],
                    gender=row['gender'],
                    civil_status=row['civil_status'],
                    relative_size=row['relative_size'],
                    work_experiences=row['work_experiences'],
                    monthly_salary=row['monthly_salary']
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
