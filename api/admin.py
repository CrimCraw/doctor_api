from django.contrib import admin
from .models import User,Doctor, News, Date

admin.site.register(Doctor)
admin.site.register(News)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff')


@admin.register(Date)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user','status', 'doctor', 'date', 'time')
    search_fields = ('date', 'time','status')
