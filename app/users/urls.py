from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import AboutUsView, Tariff, TermsConditionsView, NotificationChangeActiveStatusView

urlpatterns = [
    path('about/', AboutUsView.as_view(), name='about'),
    path('tariff/', Tariff.as_view(), name='tariff'),
    path('terms/', TermsConditionsView.as_view(), name='terms'),
    path('change-is-active/notification/<int:id>/', login_required(NotificationChangeActiveStatusView.as_view()),
         name='notification_change_is_active'),

]

