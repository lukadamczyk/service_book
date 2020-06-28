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


class AddComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        exclude = ['client']
        widgets = {
            'entry_date': DatePickerInput(format='MM/DD/YYYY'),
            'end_date': DatePickerInput(format='MM/DD/YYYY'),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        end_date = cleaned_data.get('end_date')

        if status == 'close' and end_date is None:
            raise forms.ValidationError('You have to fill out the field end_date')


class AddFaultForm(forms.ModelForm):

    class Meta:
        model = Fault
        exclude = ['complaint', 'vehicle', 'entry_date']
        widgets = {
            'end_date': DatePickerInput(format='MM/DD/YYYY'),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        end_date = cleaned_data.get('end_date')
        # import pdb;
        # pdb.set_trace()

        if status == 'close' and end_date is None:
            raise forms.ValidationError('You have to fill out the field end_date')


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


class EditComplaintForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditComplaintForm, self).__init__(*args, **kwargs)
        self.fields['document_number'].required = False
        self.fields['entry_date'].required = False
        self.fields['end_date'].required = False
        self.fields['status'].required = False
        self.fields['tasks'].required = False
        self.fields['vehicle'].required = False

    class Meta:
        model = Complaint
        exclude = ['client']
