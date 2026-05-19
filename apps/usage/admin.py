from django.contrib import admin
from .models import UsageRecord, APIRequestLog
# Register your models here.
admin.site.register(UsageRecord)
admin.site.register(APIRequestLog)