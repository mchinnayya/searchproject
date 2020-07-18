from django import forms

from branch.models import Branch


class BranchForm(forms.ModelForm):
    branch_name = forms.CharField(max_length=255, label="Branch Name", required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    branch_code = forms.CharField(label="Branch Code", required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Branch
        fields = ('branch_name', 'branch_code',)