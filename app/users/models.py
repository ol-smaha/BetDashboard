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

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    tariff_plan = models.ForeignKey(to=TariffPlan,
                                    on_delete=models.PROTECT)

    def __str__(self):
        return self.email

