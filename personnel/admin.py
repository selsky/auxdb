from personnel.models import Person
from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.localflavor.us.forms import USSocialSecurityNumberField 

class MyPersonAdminForm(forms.ModelForm):
    class Meta:
        model = Person
#        widgets = {
#            'ssn': USSocialSecurityNumberField(),
#        }

    def clean (self):
        cleaned_data = self.cleaned_data
        idno   = cleaned_data.get("idno")
        rank   = cleaned_data.get("rank")
        shield = cleaned_data.get("shield")
        if shield == None:
            if rank == 'APO' or rank == 'A/Sgt':
                raise ValidationError('APOs and A/Sgts must have shield numbers')
        else:
            if not (rank == 'APO' or rank == 'A/Sgt'):
                raise ValidationError('Only APOs and A/Sgts may have shield numbers')
        if idno < 0 and rank != 'APP':
            raise ValidationError('Only applicants may have negative id numbers')
        return super(MyPersonAdminForm,self).clean()

class PersonAdmin(admin.ModelAdmin):
    list_display = ['rank', 'last_name', 'first_name']
    form = MyPersonAdminForm

admin.site.register(Person, PersonAdmin)
