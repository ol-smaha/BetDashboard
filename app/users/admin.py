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
    list_display = ['name', 'max_service_count', 'is_active', 'price']

    @admin.action(description='Зробити активним')
    def tariff_set_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Зробити неактивним')
    def tariff_set_active(self, request, queryset):
        queryset.update(is_active=False)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TariffPlan, TariffPlanAdmin)
