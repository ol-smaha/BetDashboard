from django import forms

from bet.constants import BetResultEnum
from bet.models import BetBase, SportKind


class BetHistoryFilterForm(forms.Form):
    sport_kind = forms.MultipleChoiceField(
        choices=SportKind.name_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )
    result = forms.MultipleChoiceField(
        choices=BetResultEnum.choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )
    is_favourite = forms.MultipleChoiceField(
        choices=BetBase.is_favourite_choices(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )

    class Meta:
        fields = ('sport_kind', 'result', 'is_favourite')
