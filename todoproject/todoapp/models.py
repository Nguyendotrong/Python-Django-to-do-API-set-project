from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Q

# Create your models here.
class Task(models.Model):
    NEW, COMPLETE = range(2)
    STATUS = [
        (NEW, 'New'),
        (COMPLETE, 'Complete')
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=NEW)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    date_of_modification = models.DateTimeField(auto_now=True)
    date_of_completion = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(date_of_completion__gt=F('date_of_creation')),
                name="mycustomconstraint_checktime1"
            )
        ]

