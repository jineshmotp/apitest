# models.py

from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    # page = models.IntegerField()
    # pagesize = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.description}"


