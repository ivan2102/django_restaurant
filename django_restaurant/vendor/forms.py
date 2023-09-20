from django import forms
from .models import Vendor, OpeningHours

class VendorForm(forms.ModelForm):

 
 class Meta:
        model = Vendor
        fields = ['vendor_name']


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']

