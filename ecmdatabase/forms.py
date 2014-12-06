from django import forms
from ecmdatabase.models import Dataset
from django.shortcuts import render_to_response

class DatasetUploadForm(forms.ModelForm):

	class Meta:
		model = Dataset
		fields = ('data_file',)
