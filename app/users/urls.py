from django.urls import path

from users.views import AboutUsView, Tariff

urlpatterns = [
    path('about/', AboutUsView.as_view(), name='about'),
    path('tariff/', Tariff.as_view(), name='tariff'),
]

