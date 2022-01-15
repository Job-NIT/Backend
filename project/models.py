from user.models import Employer, Freelancer
from django.db import models
from django.core.validators import MinValueValidator


class Project(models.Model):
    image = models.ImageField(upload_to='projects', null=True, blank=True)
    title = models.CharField(max_length=255)
    detail = models.TextField()
    dead_line = models.DateTimeField()
    budget = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    def __str__(self):
        return f'{self.title} | {self.employer}'


class ProjectRequest(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    freelancer = models.ForeignKey(
        Freelancer,
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.freelancer} for {self.project.title}'
