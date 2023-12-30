from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, TariffPlan, AboutUs, ContactUs, Feedback, Notification, FQA


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]
    list_display_links = list_display
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


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone']


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['user', 'message']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'comment', 'bet_count']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_active']


class FQAAdmin(admin.ModelAdmin):
    list_display = ['question', 'description', 'is_active']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TariffPlan, TariffPlanAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(FQA, FQAAdmin)



