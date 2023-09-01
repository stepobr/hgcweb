from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CassetteType)
admin.site.register(Cassette)
admin.site.register(CassetteAssembly)
admin.site.register(Modulemap)
admin.site.register(Workstation)
admin.site.register(Step)