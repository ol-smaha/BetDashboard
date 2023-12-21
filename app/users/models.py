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
        super(CustomUser, self).save(*args, **kwargs)
        if created:
            from bet.utils import user_data_setup

            print(" === 1111 ")
            thread = Thread(target=user_data_setup, args=(self,))
            thread.start()
            print(" === 2222 ")

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
                             related_name='feedback')
    full_name = models.CharField(max_length=128, null=True, blank=True)
    comment = models.TextField(null=False, blank=False)
    bet_count = models.IntegerField(null=True, blank=True)

