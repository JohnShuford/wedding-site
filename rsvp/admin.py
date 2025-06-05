from django.contrib import admin
from .models import Guest

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'attending', 'group_id')
    fields = (
        'first_name',
        'last_name',
        'email',
        'attending',
        'group_id',  # 👈 add this to make it editable!
        'dietary_restrictions',
        'message_for_couple',
    )