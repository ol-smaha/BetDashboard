from django.urls import path

from users.views import AboutUsView, Tariff, TermsConditionsView

urlpatterns = [
    path('about/', AboutUsView.as_view(), name='about'),
    path('tariff/', Tariff.as_view(), name='tariff'),
    path('terms/', TermsConditionsView.as_view(), name='terms'),

]

