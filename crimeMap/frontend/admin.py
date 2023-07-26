from django.contrib import admin
from .models import Arrestinfo
from .models import Callinfo

# Register your models here.
admin.site.register(Arrestinfo)
admin.site.register(Callinfo)