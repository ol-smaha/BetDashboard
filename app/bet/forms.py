from django import forms
from django.forms import ModelForm

from bet.constants import BetResultEnum, BET_BASE_ORDERING_FIELDS_CHOICES, BOOL_FIELD_CHOICES, BetTypeEnum, \
    GameStatusEnum, BetPredictionEnum
from bet.models import SportKind, CompetitionBase, BetBase, BetFootball


class OrderingBaseForm(forms.Form):
    ordering = forms.ChoiceField(
        choices=BET_BASE_ORDERING_FIELDS_CHOICES,
        required=False,
        label='Сортувати по',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class BetBaseFilterForm(forms.Form):
    sport_kind = forms.MultipleChoiceField(
        choices=SportKind.name_choices(),
        required=False,
        label='Вид спорту',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )
    prediction = forms.MultipleChoiceField(
        choices=BetPredictionEnum.choices(),
        required=False,
        label='Прогноз',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )
    amount_min = forms.DecimalField(
        required=False,
        min_value='0.00',
        decimal_places=2,
        step_size='10.0',
        label='Сума з',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    amount_max = forms.DecimalField(
        required=False,
        min_value='0.00',
        step_size='10.0',
        decimal_places=2,
        label='Сума по',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    coefficient_min = forms.DecimalField(
        required=False,
        min_value='1.00',
        step_size='0.01',
        decimal_places=2,
        label='Коефіцієнт з',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    coefficient_max = forms.DecimalField(
        required=False,
        min_value='1.00',
        step_size='0.01',
        decimal_places=2,
        label='Коефіцієнт по',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    result = forms.MultipleChoiceField(
        choices=BetResultEnum.choices(),
        required=False,
        label='Результат події',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )
    date_game_start = forms.DateField(
        required=False,
        input_formats='%m/%d/%Y',
        label='Дата з',
        widget=forms.DateInput(attrs={'class': 'form-control datetimepicker-input'})
    )
    date_game_end = forms.DateField(
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


class BetHistoryFilterForm(BetBaseFilterForm, OrderingBaseForm):
    prediction = None


class FootballSearchForm(forms.Form):
    search = forms.CharField(
        label='Пошук',
        max_length=128,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))


class FootballBetHistoryFilterForm(BetBaseFilterForm, OrderingBaseForm, FootballSearchForm):
    sport_kind = None
    prediction = None

    bet_type = forms.MultipleChoiceField(
        choices=BetTypeEnum.choices(),
        required=False,
        label='Тип ставки',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )

    game_status = forms.MultipleChoiceField(
        choices=GameStatusEnum.choices(),
        required=False,
        label='Статус Ігри',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )

    competition = forms.MultipleChoiceField(
        choices=CompetitionBase.name_choices(),
        required=False,
        label='Змагання',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )


class BetProfitGraphFilterForm(BetBaseFilterForm):
    prediction = None
    result = None
    is_favourite = None


class BetCreateForm(ModelForm):

    class Meta:
        model = BetBase
        fields = ['user', 'prediction', 'amount', 'coefficient', 'result', 'sport_kind',
                  'date_game', 'is_favourite']
        widgets = {
            'prediction': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control',
                                               'min': '0.00',
                                               'step': '10.0'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control',
                                                    'min': '1.00',
                                                    'step': '0.01'}),
            'result': forms.Select(attrs={'class': 'form-control'}),
            'sport_kind': forms.Select(attrs={'class': 'form-control'}),
            'date_game': forms.DateInput(attrs={'class': 'form-control datetimepicker-input'}),
            'is_favourite': forms.Select(attrs={'class': 'form-control'}, choices=BOOL_FIELD_CHOICES),
        }


class BetFootballCreateForm(ModelForm):
    class Meta:
        model = BetFootball
        fields = ['user', 'prediction', 'amount', 'coefficient', 'result', 'sport_kind',
                  'date_game', 'is_favourite', 'bet_type', 'competition']
        widgets = {
            'prediction': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control',
                                               'min': '0.00',
                                               'step': '10.0'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control',
                                                    'min': '1.00',
                                                    'step': '0.01'}),
            'result': forms.Select(attrs={'class': 'form-control'}),
            'sport_kind': forms.Select(attrs={'class': 'form-control'}),
            'date_game': forms.DateInput(attrs={'class': 'form-control datetimepicker-input'}),
            'bet_type': forms.Select(attrs={'class': 'form-control'}),
            'competition': forms.Select(attrs={'class': 'form-control'}),
            'is_favourite': forms.Select(attrs={'class': 'form-control'}, choices=BOOL_FIELD_CHOICES),
        }




