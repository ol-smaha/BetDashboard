from django.forms import HiddenInput
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, DetailView
from django.views.generic.list import ListView

from .forms import UserCreateMessageForm, UnregisteredUserCreateMessageForm
from .models import TariffPlan, AboutUs, UnregisteredContact, Feedback, Notification


class HomePageView(TemplateView):
    template_name = 'test_home.html'


class Tariff(ListView):
    model = TariffPlan
    template_name = 'tariff/tariff_plan.html'

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context_data = {
            'tariffs': self.get_queryset(),
            'title': 'Тарифний план',
        }
        return context_data


class AboutUsView(CreateView):
    model = AboutUs
    template_name = 'about_us/about_us.html'
    form_class = UserCreateMessageForm
    success_url = reverse_lazy('about')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['form'].fields['user'].initial = self.request.user.pk
        context['form'].fields['user'].widget = HiddenInput()
        model_object = self.model.objects.all().first()
        context.update({
            'object': model_object,
            'title': 'Про нас'
        })
        return context


class TermsConditionsView(TemplateView):
    template_name = 'terms/terms_and_conditions.html'


class HomeView(CreateView):
    model = Feedback
    template_name = 'landing/index.html'
    form_class = UnregisteredUserCreateMessageForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        feedbacks = self.model.objects.all()

        context.update({
            'feedbacks': feedbacks
        })

        return context


class NotificationChangeActiveStatusView(DetailView):
    model = Notification
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        self.get_object().change_is_active()
        return redirect(reverse_lazy('bet_list') + f'?{self.request.GET.urlencode()}')

