from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, TariffPlan


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (
            'Custom Field Heading',
            {
                'fields': (
                    'tariff_plan',
                ),
            },
        ),
    )


class TariffPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_service_count']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TariffPlan, TariffPlanAdmin)
