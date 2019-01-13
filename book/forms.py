from django import forms
from .models import Complaint


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

