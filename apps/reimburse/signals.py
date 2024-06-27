from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import Reimburse, ReimburseLine, ReimburseHistory
from bson.decimal128 import Decimal128, create_decimal128_context
import decimal

@receiver(post_save, sender=ReimburseLine)
def update_activity(sender, instance, created, **kwargs):
    subtotal = instance.quantity * instance.price
    ReimburseLine.objects.filter(id=instance.id).update(subtotal = subtotal)
    total = decimal.Decimal(0.0)
    for ln in instance.reimburse.reimburseline_set.all():
        total = total + ln.subtotal
    Reimburse.objects.filter(id=instance.reimburse.id).update(total=total)

@receiver(post_delete, sender=ReimburseLine)
def delete_activity(sender, instance, **kwargs):
    total = decimal.Decimal(0.0)
    for ln in instance.reimburse.reimburseline_set.all():
        total = total + ln.subtotal
    Reimburse.objects.filter(id=instance.reimburse.id).update(total=total)


@receiver(post_save, sender=Reimburse)
def update_history(sender, instance, created, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3]=='get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        return None
    user = request.user
    if instance.state == Reimburse.SUBMIT:
        msg = f"{user.username} Submit the document"
    elif instance.state == Reimburse.PAID:
        msg = f"{user.username} Paid the document"
    elif instance.state == Reimburse.REJECT:
        msg = f"{user.username} Reject the document"
    elif instance.state == "RD":
        msg = f"{user.username} Re-draft the document"
        Reimburse.objects.filter(id=instance.id).update(state="D")
    else:
        return None
    ReimburseHistory.objects.create(reimburse=instance,user=user, message=msg)

