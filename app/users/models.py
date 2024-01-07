from enum import Enum
from threading import Thread

from django.contrib.auth.models import AbstractUser
from django.db import models


class TariffPlanVariant(str, Enum):
    FREE = 'FREE'
    MAX = 'MAX'

    @classmethod
    def choices(cls):
        res = (
            (cls.FREE, cls.FREE),
            (cls.MAX, cls.MAX)
        )
        return res


class FQACategoryVariant(str, Enum):
    ALL = 'ALL'
    LANDING = 'LANDING'
    SERVICE = 'SERVICE'

    @classmethod
    def choices(cls):
        res = tuple([(e.value, e.value) for e in cls])
        return res


class TariffPlan(models.Model):
    name = models.CharField(max_length=16, choices=TariffPlanVariant.choices())
    description = models.TextField(null=True, blank=True)
    max_service_count = models.IntegerField()
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    tariff_plan = models.ForeignKey(to=TariffPlan,
                                    on_delete=models.PROTECT,
                                    null=True,
                                    blank=True)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save()

        if created:
            from bet.utils import user_data_setup, create_registration_notifications

            create_registration_notifications(user=self)
            thread = Thread(target=user_data_setup, args=(self,))
            thread.start()

    def __str__(self):
        return self.email or self.username


class AboutUs(models.Model):
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=32)
    telegram_link = models.URLField(verbose_name='telegram', blank=True, null=True)
    img = models.ImageField(upload_to='media/images/', blank=True, null=True)


class ContactUs(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='contact_messages')
    message = models.TextField(null=True, blank=True)


class UnregisteredContact(models.Model):
    unregistered_email = models.EmailField(max_length=128, null=True, blank=True)
    message = models.TextField(null=True, blank=True)


class Feedback(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='feedback', null=True, blank=True)
    full_name = models.CharField(max_length=128, null=True, blank=True)
    comment = models.TextField(null=False, blank=False)
    bet_count = models.IntegerField(null=True, blank=True)


class Notification(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='notifications', null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def change_is_active(self, commit=True):
        self.is_active = not self.is_active
        if commit:
            self.save()


class FQA(models.Model):
    question = models.CharField(max_length=254, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    category = models.CharField(choices=FQACategoryVariant.choices(), default=FQACategoryVariant.ALL)
    is_active = models.BooleanField(default=True)
