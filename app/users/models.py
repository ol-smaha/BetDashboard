from enum import StrEnum
from django.contrib.auth.models import AbstractUser
from django.db import models


class TariffPlanVariant(StrEnum):
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

    def __str__(self):
        return self.email


class AboutUs(models.Model):
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=32)
    fb_link = models.URLField(verbose_name='facebook', blank=True, null=True)
    inst_link = models.URLField(verbose_name='instagram', blank=True, null=True)
    twit_link = models.URLField(verbose_name='twitter', blank=True, null=True)
    img = models.ImageField(upload_to='media/images/', blank=True, null=True)


class ContactUs(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE,
                             related_name='contact_messages')
    message = models.TextField(null=True, blank=True)

