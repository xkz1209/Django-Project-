from django.db import models

import os
import csv
from datetime import datetime
import uuid

# Create your models here.


class Voter(models.Model):
    def generate_voter_id():
        return str(uuid.uuid4())
    voter_id_num = models.CharField(max_length=100,default=generate_voter_id)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50, blank=True, null=True)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.voter_score})'

def str_to_bool(value):
    if value.upper() == 'TRUE':
        return True
    elif value.upper() == 'FALSE':
        return False
    else:
        raise ValueError(f"Invalid boolean value: {value}")

def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'static', 'newton_voters.csv')

    Voter.objects.all().delete()

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
           # print(row)
            voter = Voter(
                voter_id_num = row['Voter ID Number'],
                last_name=row['Last Name'],
                first_name=row['First Name'],
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apartment_number=row['Residential Address - Apartment Number'] or None,
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                party_affiliation=row['Party Affiliation'] or None,
                precinct_number=row['Precinct Number'],
                v20state=bool(str_to_bool(row['v20state'])),
                v21town=bool(str_to_bool(row['v21town'])),
                v21primary=bool(str_to_bool(row['v21primary'])),
                v22general=bool(str_to_bool(row['v22general'])),
                v23town=bool(str_to_bool(row['v23town'])),
                voter_score=int(row['voter_score'])
            )
            voter.save()
