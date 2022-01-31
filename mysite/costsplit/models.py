from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Plan(models.Model):
    # connect plan with specified user
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='plan', null=True)
    title = models.CharField(max_length=50)
    payment_date = models.DateField()
    total_members = models.IntegerField(default=1)
    plan_info = models.CharField(max_length=400, default=None)

    def __str__(self):
        return self.title


class Cost(models.Model):
    # connect cost with a plan
    plan_of_cost = models.ForeignKey(
        Plan, on_delete=models.CASCADE, null=True)
    cost_name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=50, decimal_places=2)
    number_of_members = models.IntegerField()
    payment_date = models.DateField()
    cost_info = models.CharField(max_length=400, default=None)
    cost_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.plan_of_cost}: {self.cost_name}'

    def cost_per_person(self):
        return round(self.cost/self.number_of_members, 2)

    class Meta:
        # change admin panel naming
        verbose_name = 'Cost'
        verbose_name_plural = 'Costs'
