from django import forms

from bet.constants import BetResultEnum, BET_BASE_ORDERING_FIELDS_CHOICES, BOOL_FIELD_CHOICES
from bet.models import BetBase, SportKind


class BetHistoryFilterForm(forms.Form):
    ordering = forms.ChoiceField(
        choices=BET_BASE_ORDERING_FIELDS_CHOICES,
        required=False,
        label='Сортувати по',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sport_kind = forms.MultipleChoiceField(
        choices=SportKind.name_choices(),
        required=False,
        label='Вид спорту',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )
    result = forms.MultipleChoiceField(
        choices=BetResultEnum.choices(),
        required=False,
        label='Результат події',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )
    dategamestart = forms.DateField(
        required=False,
        input_formats='%m/%d/%Y',
        label='Дата з',
        widget=forms.DateInput(attrs={'class': 'form-control datetimepicker-input'})
    )
    dategameend = forms.DateField(
        required=False,
        input_formats='%m/%d/%Y',
        label='Дата по',
        widget=forms.DateInput(attrs={'class': 'form-control datetimepicker-input'})
    )
    is_favourite = forms.MultipleChoiceField(
        choices=BOOL_FIELD_CHOICES,
        required=False,
        label='Улюблене',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )

    class Meta:
        fields = ('ordering', 'sport_kind', 'result', 'dategamestart', 'dategameend', 'is_favourite')

