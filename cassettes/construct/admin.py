from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Cassette)
admin.site.register(Workstation)
admin.site.register(Step)
admin.site.register(Part)
admin.site.register(Modulemap)