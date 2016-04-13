from django.forms import ModelForm
from .models import File

class ModelFormWithFileField(ModelForm):
    class Meta:
        model = File
        fields = ['upl_date', 'title', 'file']
