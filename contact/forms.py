from django import forms
from contact.models import Branch, Contact


class EmergencyDetailsForm(forms.ModelForm):
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'style': "width: 100%"}), label="Branch", required=True)
    contact_name = forms.CharField(max_length=255, label="Area Name", required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    extension_number = forms.IntegerField(label="Extension No.", required=True,widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Contact
        fields = ('branch', 'contact_name','extension_number',)


