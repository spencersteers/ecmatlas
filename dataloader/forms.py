from django import forms
from django.shortcuts import render_to_response
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from experiments.models import Dataset


class DatasetUploadForm(forms.ModelForm):

	class Meta:
		model = Dataset
		fields = ('data_file',)


class DatasetUploaderForm(forms.Form):
    """
    Uploader Form
    """

    upload  = forms.FileField()

    def clean_upload(self):
        upload = self.cleaned_data['upload']
        content_type = upload.content_type
        if content_type in settings.CONTENT_TYPES:
            if upload._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s')\
                       % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(upload._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))

        return upload
