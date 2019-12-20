from django.contrib import admin
from .models import Status, Employee, Project, Activity, DailyReport
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# Register your models here.

admin.site.register(Status)
admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Activity)
admin.site.register(DailyReport)

class ProfileInline(admin.StackedInline):
    model = Employee
    max_num = 1
    can_delete = False


class UserAdmin(AuthUserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

