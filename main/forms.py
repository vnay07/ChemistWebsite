from django import forms
from . models import Buisness

class BuisnessForm(forms.ModelForm):
   
    class Meta:
        model = Buisness
        fields = ['name','id','ordered_date']

        widgets = {
            "ordered_date": forms.TextInput(attrs={'readonly':'readonly'}) 
        }