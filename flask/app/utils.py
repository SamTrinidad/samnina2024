import math
import random
import re
import time
from app.models import DynamoDBModel
from flask import render_template, request
import uuid
from typing import Dict, List
from uuid import uuid4

def process_rsvp(form: Dict[str, str]) -> None:
    people: Dict[str, Dict[str, str]] = {}
    validation_errors: List[str] = []
    first_person_id: str = None
    attributes: List[str] = ['firstname', 'lastname', 'drink', 'id']

    for key in form:
        if key.startswith('person['):
            _, person_id, attribute = key.strip(']').split('[')
            person_id = person_id.strip(']')

            if attribute not in attributes:
                continue

            if first_person_id is None:
                first_person_id = person_id
            if person_id not in people:
                people[person_id] = {
                    'validation_errors': [],
                    'firstname': '',
                    'lastname': '',
                    'drink': False,
                }

            if attribute == 'drink':
                people[person_id][attribute] = request.form.get(key) == 'on'
            else:
                if not request.form[key].isalpha():
                    people[person_id]['validation_errors'].append(f"{attribute} must be alphabetical.")
                people[person_id][attribute] = request.form[key]

            if attribute == 'firstname' and people[person_id][attribute] == '':
                people[person_id]['validation_errors'].append("First name is required.")

    post = form.to_dict()

    if not people[first_person_id]['lastname'] or people[first_person_id]['lastname'] == '':
        people[first_person_id]['validation_errors'].append("Last name is required for first person.")

    if not post['tel'] or post['tel'] == '':
        validation_errors.append("Phone number is required.")

    if validation_errors:
        return render_template('rsvp.html', validation_errors=validation_errors, people=people)

    rsvp_entry = dict(
        id=uuid4().hex,
        people=len(people),
        tel=post['tel']
    )
    i = 1
    alcohol_count = 0
    for person_id, person in people.items():
        rsvp_entry[f'person{i}'] = {
            'firstname': person['firstname'],
            'lastname': person['lastname'],
            'drink': person['drink'],
        }
        alcohol_count += 1 if person['drink'] else 0
        i += 1
    rsvp_entry['alcohol_count'] = alcohol_count

    try:
        rsvp = DynamoDBModel.DynamoDBModel('rsvp')
        rsvp.put_item(rsvp_entry)

    except Exception as e:
        print(e)
        return render_template('rsvp.html', validation_errors={'form': 'Error saving RSVP.'}, people=people), 500

    return render_template('rsvp.accepted.html')

def generate_id():
    def f(x, y):
        if y != 0:
            a = math.floor(math.log10(y))
        else:
            a = -1
        return int(x*10**(1+a)+y)
    return f(int(time.time()), random.randint(0, 1000000))