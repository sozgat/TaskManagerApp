from django.contrib import admin
from tasks.models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):

    list_display = ['id','task','created_at']
    list_display_links = ['task','created_at']
    list_filter = ['created_at']
    search_fields = ['task']
    class Meta:
        model = Task

admin.site.register(Task, TaskAdmin)
