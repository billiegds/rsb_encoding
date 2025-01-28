from django import forms
from .models import Voter

class VoterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = '__all__'


class PartyLeaderSearchForm(forms.Form):
    query = forms.CharField(max_length=200, label='Search by Party Leader Name', required=False)
