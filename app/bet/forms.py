from datetime import datetime

from django import forms
from django.forms import ModelForm

from bet.constants import BetResultEnum, BET_BASE_ORDERING_FIELDS_CHOICES, BOOL_FIELD_CHOICES, BetFootballTypeEnum, \
    GameStatusEnum, BetFootballPredictionEnum, LiveTypeEnum
from bet.models import SportKind, CompetitionBase, BetBase, BetFootball, BettingService


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
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    coefficient_min = forms.DecimalField(
        required=False,
        min_value='1.00',
        step_size='0.01',
        decimal_places=2,
        label='Коефіцієнт з',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    coefficient_max = forms.DecimalField(
        required=False,
        min_value='1.00',
        step_size='0.01',
        decimal_places=2,
        label='Коефіцієнт по',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    result = forms.MultipleChoiceField(
        choices=BetResultEnum.choices(),
        required=False,
        label='Результат ставки',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )
    betting_service = forms.MultipleChoiceField(
        choices=BettingService.name_choices(),
        required=False,
        label='Сервіс',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )
    is_live_type = forms.MultipleChoiceField(
        choices=BOOL_FIELD_CHOICES,
        required=False,
        label='Лайв',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )
    date_game_start = forms.DateField(
        required=False,
        input_formats='%m/%d/%Y',
        label='Дата з',
        widget=forms.DateInput(attrs={'class': 'form-control datetimepicker-input',
                                      'pattern': "\d{2}/\d{2}/\d{4}"})
    )
    date_game_end = forms.DateField(
        required=False,
        input_formats='%m/%d/%Y',
        label='Дата по',
        widget=forms.DateInput(attrs={'class': 'form-control datetimepicker-input',
                                      'pattern': "\d{2}/\d{2}/\d{4}"})
    )
    is_favourite = forms.MultipleChoiceField(
        choices=BOOL_FIELD_CHOICES,
        required=False,
        label='Улюблене',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-checkbox'})
    )


class BetHistoryFilterForm(BetBaseFilterForm):
    pass


class FootballSearchForm(forms.Form):
    search = forms.CharField(
        label='Пошук',
        max_length=128,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))


class FootballBetHistoryFilterForm(BetBaseFilterForm, FootballSearchForm):
    sport_kind = None

    bet_type = forms.MultipleChoiceField(
        choices=BetFootballTypeEnum.choices(),
        required=False,
        label='Тип ставки',
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
        fields = ['user', 'amount', 'coefficient', 'result', 'is_live_type', 'sport_kind',
                  'date_game', 'betting_service', 'is_favourite']
        labels = {
            'amount': 'Сума',
            'coefficient': 'Коефіцієнт',
            'result': 'Результат',
            'is_live_type': 'Лайв',
            'sport_kind': 'Вид спорту',
            'betting_service': 'Сервіс',
            'date_game': 'Дата події',
            'is_favourite': 'Улюблене?',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control',
                                               'placeholder': '0',
                                               'min': '0.00',
                                               'step': '1.0'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control',
                                                    'placeholder': '1.00',
                                                    'min': '1.00',
                                                    'step': '0.01'}),
            'result': forms.Select(attrs={'class': 'selectize-control single',
                                          'placeholder': 'Виберіть значення...'}),
            'is_live_type': forms.Select(attrs={'class': 'selectize-control single'},
                                         choices=BOOL_FIELD_CHOICES),
            'sport_kind': forms.Select(attrs={'class': 'selectize-control single',
                                              'placeholder': 'Виберіть значення...'}),
            'betting_service': forms.Select(attrs={'class': 'selectize-control single',
                                                   'placeholder': 'Виберіть значення...'}),
            'date_game': forms.DateInput(attrs={'class': 'form-control',
                                                'placeholder': f'{datetime.now().strftime("%m/%d/%Y")}',
                                                'pattern': "\d{2}/\d{2}/\d{4}"}),
            'is_favourite': forms.Select(attrs={'class': 'selectize-control single'},
                                         choices=BOOL_FIELD_CHOICES),
        }


class BetFootballCreateForm(ModelForm):
    class Meta:
        model = BetFootball
        fields = ['user', 'prediction', 'amount', 'coefficient', 'result', 'competition', 'team_home', 'team_guest',
                  'date_game', 'is_live_type', 'betting_service', 'is_favourite']
        labels = {
            'prediction': 'Прогноз',
            'amount': 'Сума',
            'coefficient': 'Коефіцієнт',
            'result': 'Результат',
            'is_live_type': 'Лайв',
            'competition': 'Змагання',
            'betting_service': 'Сервіс',
            'team_home': 'Команда 1',
            'team_guest': 'Команда 2',
            'date_game': 'Дата події',
            'is_favourite': 'Улюблене?',
        }
        widgets = {
            'prediction': forms.Select(attrs={'class': 'selectize-control single',
                                              'placeholder': 'Виберіть значення...'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control',
                                               'placeholder': '0',
                                               'min': '0.00',
                                               'step': '1.0'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control',
                                                    'placeholder': '1.00',
                                                    'min': '1.00',
                                                    'step': '0.01'}),
            'result': forms.Select(attrs={'class': 'selectize-control single',
                                          'placeholder': 'Виберіть значення...'}),
            'competition': forms.Select(attrs={'class': 'selectize-control single',
                                               'placeholder': 'Виберіть значення...'}),
            'is_live_type': forms.Select(attrs={'class': 'selectize-control single'},
                                         choices=BOOL_FIELD_CHOICES),
            'betting_service': forms.Select(attrs={'class': 'selectize-control single',
                                                   'placeholder': 'Виберіть значення...'}),
            'team_home': forms.Select(attrs={'class': 'selectize-control single',
                                             'placeholder': 'Виберіть значення...'}),
            'team_guest': forms.Select(attrs={'class': 'selectize-control single',
                                              'placeholder': 'Виберіть значення...'}),
            'date_game': forms.DateInput(attrs={'class': 'form-control',
                                                'placeholder': f'{datetime.now().strftime("%m/%d/%Y")}',
                                                'pattern': "\d{2}/\d{2}/\d{4}"}),
            'is_favourite': forms.Select(attrs={'class': 'selectize-control single'},
                                         choices=BOOL_FIELD_CHOICES),
        }


class RatingFilterForm(BetBaseFilterForm):
    sport_kind = None
    result = None
    is_favourite = None


class StatisticFilterForm(BetBaseFilterForm):
    amount_min = None
    amount_max = None
    coefficient_min = None
    coefficient_max = None
    result = None
    is_favourite = None


class SportKindCreateForm(ModelForm):
    class Meta:
        model = SportKind
        fields = ['user', 'name']
        labels = {'name': 'Назва'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть значення ...'}),
        }


class CompetitionCreateForm(ModelForm):
    class Meta:
        model = CompetitionBase
        fields = ['user', 'name', 'sport_kind', 'country']
        labels = {
            'name': 'Назва',
            'sport_kind': 'Вид спорту',
            'country': 'Країна'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть значення...'}),
            'sport_kind': forms.Select(attrs={'class': 'selectize-control single',
                                              'placeholder': 'Виберіть значення...'},
                                       choices=SportKind.name_choices()),
            'country': forms.Select(attrs={'class': 'selectize-control single',
                                           'placeholder': 'Виберіть значення...'}),
        }


class ServiceCreateForm(ModelForm):
    class Meta:
        model = BettingService
        fields = ['user', 'name']
        labels = {'name': 'Назва'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть значення...'}),
        }
