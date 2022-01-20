from user.models import Employer, Freelancer
from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Project(models.Model):
    image = models.ImageField(upload_to='projects', null=True, blank=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
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
    freelancer = models.ForeignKey(
        Freelancer,
        on_delete=models.SET_NULL,
        related_name='projects',
        null=True,
        blank=True
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.freelancer} for {self.project.title}'
