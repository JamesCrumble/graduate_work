from django.contrib import admin

from .models import NotificationStatus, NotificationTasks, Templates


class NotificationTasksInline(admin.TabularInline):
    model = NotificationTasks


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    inlines = (NotificationTasksInline,)


@admin.register(NotificationStatus)
class NotificationStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(NotificationTasks)
class NotificationTasksAdmin(admin.ModelAdmin):
    pass
