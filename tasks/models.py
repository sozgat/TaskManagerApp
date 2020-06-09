from django.db import models


class Task(models.Model):
    task = models.CharField(max_length=250, db_index=True, verbose_name="Task")
    is_completed = models.BooleanField(default=False, verbose_name="Is completed ?")
    #user_id = models.IntegerField(null=True ,verbose_name="User ID")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.task
        #return f"{self.task}"
