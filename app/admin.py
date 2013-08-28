from django.contrib import admin
from models import Alert

class AlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'alert_server_time', 'start', 'finish', 'period', 'time', 'alert_email', 'email', 'alert_sms', 'phone')

admin.site.register(Alert, AlertAdmin)