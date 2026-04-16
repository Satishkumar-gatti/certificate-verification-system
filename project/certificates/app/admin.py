from django.contrib import admin
from .models import User, Certificate

# Register models
admin.site.register(User)
admin.site.register(Certificate)