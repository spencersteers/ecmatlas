# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file, ',
        help_text='max size: 42 MB'
    )

class EmailForm(forms.Form):
    contactInputTextEmailSubject = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'contactInputTextEmailSubject'}),
        required = True)
    contactEmailMessage = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'contactEmailMessage'}),
        required = True)
        
    '''def clean(self):
        #cleaned_data = super(EmailForm, self).clean()
        contactInputTextEmailSubject = self.cleaned_data.get('contactInputTextEmailSubject')
        contactEmailMessage = self.cleaned_data.get('contactEmailMessage')
        if not contactInputTextEmailSubject:
            raise forms.ValidationError("You must enter a subject!")
        if not contactEmailMessage:
            raise forms.ValidationError("You must enter a message!")
        return self.cleaned_data'''
        