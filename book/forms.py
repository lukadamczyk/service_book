import datetime, re

from django import forms
from .models import Complaint, Fault
from bootstrap_datepicker_plus import DatePickerInput



class FilterComplaintsForm(forms.ModelForm):

    date_from = forms.DateField(required=False,
                                widget=DatePickerInput(format='MM/DD/YYYY'),
                                label='Od')
    date_to = forms.DateField(required=False,
                              widget=DatePickerInput(format='MM/DD/YYYY'),
                              label='Do')

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(FilterComplaintsForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['status'].required = False
        self.fields['status'].label = 'Stan'
        self.fields['vehicle'].required = False
        self.fields['vehicle'].label = 'Pojazd'



    class Meta:
        model = Complaint
        fields = ['status', 'vehicle', 'date_from', 'date_to']


class FilterFaultForm(forms.ModelForm):

    date_from = forms.DateField(required=False,
                                widget=DatePickerInput(format='MM/DD/YYYY'),
                                label='Od')
    date_to = forms.DateField(required=False,
                              widget=DatePickerInput(format='MM/DD/YYYY'),
                              label='Do')

    def __init__(self, *args, **kwargs):
        super(FilterFaultForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['vehicle'].required = False

    class Meta:
        model = Fault
        fields = ['status', 'vehicle', 'zr_number', 'date_from', 'date_to']
        labels = {
            'status': 'Status',
            'vehicle': 'Pojazd',
            'zr_number': 'Numer ZR',
        }


class AddComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        exclude = ['client', 'tasks', 'end_date']
        widgets = {
            'entry_date': DatePickerInput(format='MM/DD/YYYY'),
            'end_date': DatePickerInput(format='MM/DD/YYYY'),
        }
        labels = {
            'document_number': 'Nr reklamacji',
            'entry_date': 'Data rozpoczęcia',
            'status': 'Status',
            'vehicle': 'Pojazd'
        }


    def __init__(self, *args, **kwargs):
        super(AddComplaintForm, self).__init__(*args, **kwargs)
        fields = ['document_number']
        for field in fields:
            self.fields[field].error_messages.update({
                'required': 'To pole jest wymagane',
                'unique': 'Dokument o takim numerze już istnieje'
            })

    def clean(self):
        cleaned_data = super().clean()
        entry_date = cleaned_data.get('entry_date')

        if entry_date:
            today = datetime.date.today()
            if entry_date > today:
                raise forms.ValidationError('Podaj właściwą datę rozpoczęcia reklamacji, nie może być pózniejsza niż '
                                            '{}'.format(datetime.date.today()))



class AddFaultForm(forms.ModelForm):

    class Meta:
        model = Fault
        exclude = ['complaint', 'vehicle', 'entry_date']
        widgets = {
            'end_date': DatePickerInput(format='MM/DD/YYYY'),
        }
        labels = {
            'name': 'Usterka',
            'category': 'Kategoria',
            'description': 'Opis',
            'actions': 'Podjęte działania',
            'comments': 'Uwagi',
            'zr_number': 'Numer ZR',
            'end_date': 'Data zakończenia',
            'need': 'Potrzeby'
        }

    def __init__(self, *args, **kwargs):
        super(AddFaultForm, self).__init__(*args, **kwargs)
        fields = ['name', 'category', 'description', 'status']
        for field in fields:
            self.fields[field].error_messages.update({
                'required': 'To pole jest wymagane'
            })
            if field == 'category':
                self.fields[field].error_messages.update({
                    'invalid_choice': 'Wybierz jedną z proponowanych kategori'
                })

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        end_date = cleaned_data.get('end_date')
        zr_number = cleaned_data.get('zr_number')

        if status == 'close' and end_date is None:
            raise forms.ValidationError('Podaj datę zakończenia usterki')

        if status == 'open' and end_date:
            raise forms.ValidationError('Nie można podać daty zakończnia usterki przy otwarty statusie')

        if zr_number:
            if not re.match(r"^\d{6}$", zr_number):
                raise forms.ValidationError('Podaj właściwy numer ZR (6 cyfr)')


class NumberOfFaults(forms.Form):
    number = forms.IntegerField(required=True,
                                label='Liczba usterek')


class EditFaultForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditFaultForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['name'].required = False
        self.fields['end_date'].required = False
        self.fields['category'].required = False
        self.fields['description'].required = False

    class Meta:
        model = Fault
        exclude = ['complaint', 'vehicle', 'entry_date']
        labels = {
            'name': 'Usterka',
            'category': 'Kategoria',
            'description': 'Opis',
            'actions': 'Podjęte działania',
            'comments': 'Uwagi',
            'zr_number': 'Numer ZR',
            'end_date': 'Data zakończenia',
            'need': 'Potrzeby'
        }


class EditComplaintForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditComplaintForm, self).__init__(*args, **kwargs)
        self.fields['document_number'].required = False
        self.fields['entry_date'].required = False
        self.fields['end_date'].required = False
        self.fields['status'].required = False
        self.fields['vehicle'].required = False

    class Meta:
        model = Complaint
        exclude = ['client', 'tasks']
        labels = {
            'document_number': 'Nr reklamacji',
            'entry_date': 'Od',
            'end_date': 'Do',
            'status': 'Status',
            'vehicle': 'Pojazd'
        }
