from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class Reimburse(models.Model):
    DRAFT = "D"
    SUBMIT = "S"
    PAID = "P"
    REJECT = "R"

    STATE = [
        (DRAFT, "Draft"),
        (SUBMIT, "Waiting Approval"),
        (PAID, "Paid"),
        (REJECT, "Rejected"),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reimburse_user_set")
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reimburse_approver_set")
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    total = models.IntegerField(default=0)
    state = models.CharField(max_length=1, choices=STATE, default=DRAFT)

    def __str__(self):
        return self.title

class ReimburseHistory(models.Model):
    reimburse = models.ForeignKey(Reimburse, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)

class ReimburseLine(models.Model):
    reimburse = models.ForeignKey(Reimburse, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    attachment = models.FileField(upload_to="reimburse_attachment")
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)


