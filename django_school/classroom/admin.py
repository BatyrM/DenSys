from django.contrib import admin
from .models import User, Patient, Teacher

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Teacher)