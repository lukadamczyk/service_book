import datetime, re

from django import forms
from .models import Complaint, Fault, Fault_without_complaint, Owner
from bootstrap_datepicker_plus import DatePickerInput


class FilterComplaintsForm(forms.ModelForm):

    date_from = forms.DateField(required=False,
                                widget=DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
                                label='Od')
    date_to = forms.DateField(required=False,
                              widget=DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
                              label='Do')

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(FilterComplaintsForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['status'].required = False
        self.fields['status'].label = 'Stan'
        self.fields['vehicle'].required = False
        self.fields['vehicle'].label = 'Pojazd'
        self.fields['client'].required = False
        self.fields['client'].label = 'Klient'



    class Meta:
        model = Complaint
        fields = ['status', 'vehicle', 'date_from', 'date_to', 'client']


class FilterFaultForm(forms.ModelForm):

    date_from = forms.DateField(required=False,
                                widget=DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
                                label='Od')
    date_to = forms.DateField(required=False,
                              widget=DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
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


class FilterFaultWithoutComplaintForm(forms.ModelForm):

    date_from = forms.DateField(required=False,
                                widget=DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
                                label='Od')
    date_to = forms.DateField(required=False,
                              widget=DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
                              label='Do')
    blank_choice = ('', '---------')
    list_of_choices = [blank_choice]
    for owner in Owner.objects.all():
        list_of_choices.append((owner.id, owner.name))
    client = forms.ChoiceField(choices=list_of_choices,
                               required=False,
                               label='Klient',
                               initial='')

    def __init__(self, *args, **kwargs):
        super(FilterFaultWithoutComplaintForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].required = False
        self.fields['status'].required = False


    class Meta:
        model = Fault_without_complaint
        fields = ['status', 'vehicle', 'date_from', 'date_to']
        labels = {
            'status': 'Status',
            'vehicle': 'Pojazd',
        }


class AddComplaintForm(forms.ModelForm):
    file_doc = forms.FileField(required=False,
                               allow_empty_file=True,
                               label='Załącznik')

    class Meta:
        model = Complaint
        exclude = ['client', 'tasks', 'author']
        widgets = {
            'entry_date': DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
            'end_date': DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
        }
        labels = {
            'document_number': 'Nr reklamacji',
            'entry_date': 'Data rozpoczęcia',
            'end_date': 'Data zakończenia',
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
        end_date = cleaned_data.get('end_date')
        status = cleaned_data.get('status')

        if entry_date:
            today = datetime.date.today()
            if entry_date > today:
                raise forms.ValidationError('Podaj właściwą datę rozpoczęcia reklamacji, nie może być pózniejsza niż '
                                            '{}'.format(datetime.date.today()))
        if end_date and end_date < entry_date:
            raise forms.ValidationError('Data zakończenia reklamacji nie moze być wcześniejsza niź '
                                                        'data rozpoczęcia')
        if end_date and status == 'open':
            raise forms.ValidationError('Aby zamknąć rekalacje potrzeba wybrać zamknięty status '
                                                        'reklamacji i podać datę zakończenia')

        if not end_date and status == 'close':
            raise forms.ValidationError('Aby zamknąć rekalacje potrzeba wybrać zamknięty status '
                                        'reklamacji i podać datę zakończenia')
        if end_date:
            if end_date > datetime.date.today() and status == 'close':
                raise forms.ValidationError('Data zamknięcia reklamacji nie może być poźniejsza niż {}'.format(
                datetime.date.today()))


class AddFaultForm(forms.ModelForm):

    class Meta:
        model = Fault
        exclude = ['complaint', 'vehicle', 'entry_date']
        widgets = {
            'end_date': DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
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
            if field == 'name':
                self.fields[field].error_messages.update({
                    'max_length': 'To pole może zawierać maksymalinie 40 znaków'
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


class AddFaultWithoutComplaintForm(forms.ModelForm):

    class Meta:
        model = Fault_without_complaint
        widgets = {
            'entry_date': DatePickerInput(options=
            {
                'locale': 'pl'
            }),
            'end_date': DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
        }
        labels = {
            'name': 'Usterka',
            'vehicle': 'Pojazd',
            'category': 'Kategoria',
            'description': 'Opis',
            'actions': 'Podjęte działania',
            'comments': 'Uwagi',
            'entry_date': 'Data wpłynięcia',
            'end_date': 'Data zakończenia',
            'need': 'Potrzeby'
        }
        fields = ['name', 'vehicle', 'category', 'description', 'actions', 'comments', 'status', 'entry_date',
                  'end_date', 'need']

    def __init__(self, *args, **kwargs):
        super(AddFaultWithoutComplaintForm, self).__init__(*args, **kwargs)
        fields = ['name', 'category', 'description', 'status']
        for field in fields:
            self.fields[field].error_messages.update({
                'required': 'To pole jest wymagane'
            })
            if field == 'category':
                self.fields[field].error_messages.update({
                    'invalid_choice': 'Wybierz jedną z proponowanych kategori'
                })
            if field == 'name':
                self.fields[field].error_messages.update({
                    'max_length': 'To pole może zawierać maksymalinie 40 znaków'
                })

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        end_date = cleaned_data.get('end_date')
        entry_date = cleaned_data.get('entry_date')
        today = datetime.date.today()

        if status == 'close' and end_date is None:
            raise forms.ValidationError('Podaj datę zakończenia usterki')

        if status == 'open' and end_date:
            raise forms.ValidationError('Nie można podać daty zakończnia usterki przy otwarty statusie')

        if end_date and end_date > today:
            raise forms.ValidationError('Data zakończenia nie może być póżniejsza niż {}'.format(today.strftime(
                        '%d/%m/%Y')))
        if entry_date and entry_date > today:
            raise forms.ValidationError('Data wpłynięcia nie może być póżniejsza niż {}'.format(today.strftime(
                        '%d/%m/%Y')))
        if status == 'close' and end_date < entry_date:
            raise forms.ValidationError('Data zakończenia nie może być wcześniejsza od daty wpłynięcia usterki')


class EditFaultWithoutComplaintForm(forms.ModelForm):

    class Meta:
        model = Fault_without_complaint
        widgets = {
            'entry_date': DatePickerInput(options=
            {
                'locale': 'pl'
            }),
            'end_date': DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
        }
        labels = {
            'name': 'Usterka',
            'vehicle': 'Pojazd',
            'category': 'Kategoria',
            'description': 'Opis',
            'actions': 'Podjęte działania',
            'comments': 'Uwagi',
            'entry_date': 'Data wpłynięcia',
            'end_date': 'Data zakończenia',
            'need': 'Potrzeby'
        }
        fields = ['name', 'vehicle', 'category', 'description', 'actions', 'comments', 'status', 'entry_date',
                  'end_date', 'need']

    def __init__(self, *args, **kwargs):
        super(EditFaultWithoutComplaintForm, self).__init__(*args, **kwargs)
        fields = ['name', 'category', 'description', 'status']
        self.fields['status'].required = False
        self.fields['name'].required = False
        self.fields['vehicle'].required = False
        self.fields['entry_date'].required = False
        self.fields['category'].required = False
        self.fields['description'].required = False
        for field in fields:
            if field == 'category':
                self.fields[field].error_messages.update({
                    'invalid_choice': 'Wybierz jedną z proponowanych kategori'
                })
            if field == 'name':
                self.fields[field].error_messages.update({
                    'max_length': 'To pole może zawierać maksymalinie 40 znaków'
                })

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        end_date = cleaned_data.get('end_date')
        entry_date = cleaned_data.get('entry_date')
        today = datetime.date.today()

        if status == 'close' and end_date is None:
            raise forms.ValidationError('Podaj datę zakończenia usterki')

        if status == 'open' and end_date:
            raise forms.ValidationError('Nie można podać daty zakończnia usterki przy otwarty statusie')

        if end_date and end_date > today:
            raise forms.ValidationError('Data zakończenia nie może być póżniejsza niż {}'.format(today.strftime(
                        '%d/%m/%Y')))
        if entry_date and entry_date > today:
            raise forms.ValidationError('Data wpłynięcia nie może być póżniejsza niż {}'.format(today.strftime(
                        '%d/%m/%Y')))
        if status == 'close' and end_date < entry_date:
            raise forms.ValidationError('Data zakończenia nie może być wcześniejsza od daty wpłynięcia usterki')


class NumberOfFaults(forms.Form):
    number = forms.IntegerField(required=True,
                                label='Liczba usterek')


class EditFaultForm(AddFaultForm):

    def __init__(self, *args, **kwargs):
        super(EditFaultForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['name'].required = False
        self.fields['end_date'].required = False
        self.fields['category'].required = False
        self.fields['description'].required = False

    class Meta(AddFaultForm.Meta):
        model = Fault
        exclude = ['complaint', 'vehicle', 'entry_date']


class EditComplaintForm(forms.ModelForm):
    file_doc = forms.FileField(required=False,
                               allow_empty_file=True,
                               label='Załącznik')

    def __init__(self, *args, **kwargs):
        super(EditComplaintForm, self).__init__(*args, **kwargs)
        self.fields['document_number'].required = False
        self.fields['entry_date'].required = False
        self.fields['end_date'].required = False
        self.fields['status'].required = False
        self.fields['vehicle'].required = False

    class Meta:
        model = Complaint
        exclude = ['tasks', 'author', 'client']
        widgets = {
            'entry_date': DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
            'end_date': DatePickerInput(options=
                                          {
                                              'locale': 'pl'
                                          }),
        }
        labels = {
            'document_number': 'Nr reklamacji',
            'entry_date': 'Data rozpoczęcia',
            'end_date': 'Data zakończenia',
            'status': 'Status',
            'vehicle': 'Pojazd'
        }

    def clean(self):
        cleaned_data = super().clean()
        doc_number = cleaned_data.get('document_number')
        entry_date = cleaned_data.get('entry_date')
        end_date = cleaned_data.get('end_date')
        status = cleaned_data.get('status')
        vehicle = cleaned_data.get('vehicle')

        if not doc_number:
            raise forms.ValidationError('Wprowadź numer reklamacji')

        if entry_date:
            if entry_date > datetime.date.today():
                raise forms.ValidationError('Data rozpoczęcia reklamacji nie może być późniejsza niż {}'.format(
                    datetime.date.today()))

        if not entry_date:
            raise forms.ValidationError('Wprowadź datę rozpoczęcia reklamacji')

        if end_date and end_date < entry_date:
            raise forms.ValidationError('Data zakończenia reklamacji nie może być wcześniejsza niż '
                                                        'data rozpoczęcia')
        if end_date and status == 'open':
            raise forms.ValidationError('Aby zamknąć rekalacje potrzeba wybrać zamknięty status '
                                                        'reklamacji i podać datę zakończenia')

        if not end_date and status == 'close':
            raise forms.ValidationError('Aby zamknąć rekalacje potrzeba wybrać zamknięty status '
                                        'reklamacji i podać datę zakończenia')

        if end_date:
            if end_date > datetime.date.today() and status == 'close':
                raise forms.ValidationError('Data zamknięcia reklamacji nie może być poźniejsza niż {}'.format(
                datetime.date.today()))
