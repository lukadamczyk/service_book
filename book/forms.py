from django import forms
from .models import Complaint, Fault


class FilterComplaintsForm(forms.ModelForm):

    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(FilterComplaintsForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['status'].required = False
        self.fields['vehicle'].required = False


    class Meta:
        model = Complaint
        fields = ['status', 'vehicle', 'date_from', 'date_to']


class FilterFaultForm(forms.ModelForm):

    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)

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

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        end_date = cleaned_data.get('end_date')
        # import pdb;
        # pdb.set_trace()

        if status == 'close' and end_date is None:
            raise forms.ValidationError('You have to fill out the field end_date')


