from django.views.generic import TemplateView
from django.views.generic.list import ListView
from .models import TariffPlan


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
            'title': 'Tariffs',
        }
        return context_data


