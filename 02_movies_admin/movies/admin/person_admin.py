from django.contrib import admin
from ..models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    order_fields = ['full_name']
    search_fields = ['full_name']
