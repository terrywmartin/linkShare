from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Link

  
class LinkModelForm(ModelForm):
    class Meta:
        model = Link
        fields = [ 'type', 'link',  ]

    def __init__(self, *args, **kwargs):
        
        super(LinkModelForm, self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
 