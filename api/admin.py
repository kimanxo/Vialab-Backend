from django.contrib import admin
from .models import Exam, Feedback, Announce, FAQ, About, Order, Newsletter


# Registering the models in the admin dashboard.
admin.site.register([Exam, Feedback, Announce, FAQ, About, Order, Newsletter])
