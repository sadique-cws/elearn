from django import forms
from cws.models import *

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        


