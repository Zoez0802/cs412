# File: models.py
# Author: Minjie Zuo (minjiez@bu.edu), 3/16/2026
# Description: This file defines the Voter model and a function
# to load voter data from a CSV file into the database.

import csv
from django.db import models


class Voter(models.Model):
    """Store voter record from the Newton voter file."""
    #fields from CSV file:
    last_name = models.TextField()
    first_name = models.TextField()

    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True)
    zip_code = models.CharField(max_length=10)

    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)

    #These fields indicate whether or not a given voter participated in several recent elections:
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    #how many of the past 5 elections the voter participated in.
    voter_score = models.IntegerField()

    def __str__(self):
        """Return a string representation of this voter."""
        return f'{self.first_name} {self.last_name}'
    

def load_data():
    """Load voter records from CSV file into Django model instances."""

    # Delete old records to prevent duplicates.
    Voter.objects.all().delete()

    filename = r"C:\Users\zuomi\OneDrive\桌面\newton_voters.csv"
    f = open(filename)
    f.readline()

    for line in f:
        fields = line.strip().split(',')

        try:
            # Create a new Voter object with this record from CSV.
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9],
                precinct_number=fields[10],
                # fixed: convert TRUE /FALSE string to boolean
                v20state=(fields[11] == 'TRUE'),
                v21town=(fields[12] == 'TRUE'),
                v21primary=(fields[13] == 'TRUE'),
                v22general=(fields[14] == 'TRUE'),
                v23town=(fields[15] == 'TRUE'),

                voter_score=fields[16],
            )

            voter.save()

        except:
            print(f'Skipped: {fields}')

    print(f'Done. Created {len(Voter.objects.all())} Voters.')