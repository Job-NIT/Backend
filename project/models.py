from user.models import Employer
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    detail = models.TextField()
    dead_line = models.DateTimeField()
    budget = models.PositiveIntegerField(default=0)
    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    def __str__(self):
        return f'{self.title} | {self.employer}'
