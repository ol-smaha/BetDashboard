from django.urls import path

from users.views import AboutUsView

urlpatterns = [
    path('about-us/', AboutUsView.as_view(), name='about-us'),

]

