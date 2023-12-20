from app.utils import process_rsvp, generate_id
from flask import Blueprint, render_template, request
import os

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    return render_template('index.html', API_KEY=os.getenv('GOOGLE_API_KEY'))

@routes.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    if request.method == 'POST':
        return process_rsvp(request.form)

    id = generate_id()
    people = {
        id: {
            'id': id,
            'firstname':'',
            'lastname':'',
            'drink':True,
            'validation_errors': {}
        },
    }
    return render_template('rsvp.html', people=people)

@routes.route('/rsvp_add_person', methods=['GET'])
def rsvp_add():
    return render_template('person.html', id=generate_id(), first=False, drink=True, validation_errors={})


