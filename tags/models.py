from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=50, db_index=True, verbose_name="Tag")
    css_color = models.CharField(max_length=50, default="null", verbose_name="Css Color for Bootstrap")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.tag
        #return f"{self.task}"

class TagsTaskIntegration(models.Model):
    task_id = models.IntegerField()
    tag_id = models.IntegerField()

    def __int__(self):
        return  self.task_id