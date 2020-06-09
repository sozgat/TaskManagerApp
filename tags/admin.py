from django.contrib import admin
from tags.models import *
# Register your models here.

class TagAdmin(admin.ModelAdmin):

    list_display = ['id','tag','created_at']
    list_display_links = ['tag','created_at']
    list_filter = ['created_at']
    search_fields = ['tag']
    class Meta:
        model = Tag

admin.site.register(Tag, TagAdmin)

class TagsTaskIntegrationAdmin(admin.ModelAdmin):

    list_display = ['task_id','tag_id']
    list_display_links = ['task_id','tag_id']
    search_fields = ['task_id']
    class Meta:
        model = TagsTaskIntegration

admin.site.register(TagsTaskIntegration, TagsTaskIntegrationAdmin)


