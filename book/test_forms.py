import datetime

from django.test import TestCase
from .forms import AddComplaintForm, EditComplaintForm


today = datetime.date.today()
def create_form(doc, date, status, vehicle, form):
    data = {
        'document_number': doc,
        'entry_date': date,
        'status': status,
        'vehicle': vehicle
    }
    add_form = AddComplaintForm(date)
    return add_form

class AddComplainFormTestCase(TestCase):

    def test_valid_form(self):
        test_form = create_form('Kw23', today, 'open', 'SA132-002', AddComplaintForm)
        self.assertFalse(test_form.is_valid())