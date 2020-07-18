from django import forms
from favorite.models import Favorite


class FavoriteForm(forms.ModelForm):
    # favorite_name = forms.CharField(max_length=255, label="Favorite", required=True,
    #                                 widget=forms.TextInput(attrs={'class': 'form-control', 'width': '20%'}))
    favorite_name = forms.CharField(max_length=255, label="Favorite", required=True,
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'width': '120px'}))

    # extension_number = forms.IntegerField(label="Extension No.", required=True,widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Favorite
        fields = ('favorite_name',)


# class FavoriteContactForm(forms.ModelForm):
#     favorite = forms.ModelMultipleChoiceField(queryset=Favorite.objects.all(), label='Favorite', required=False,
#                                               widget=forms.CheckboxSelectMultiple(
#                                                   attrs={'class': 'form-control kt_checkbox'}))
#
#     class Meta:
#         model = Favorite_link_with_contact
#         fields = ('favorite',)
