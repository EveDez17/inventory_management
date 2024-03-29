from django.db import models

from django.conf import settings

from django.utils import timezone

class SecurityGate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    type = models.CharField(max_length=100)
    operational_status = models.BooleanField(default=True)

class AccessLog(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(default=timezone.now)
    access_type = models.CharField(max_length=50)


class SecurityGateTransaction(models.Model):
    security_gate = models.ForeignKey(SecurityGate, on_delete=models.CASCADE)
    vehicle_reg = models.CharField(max_length=50)
    trailer_number = models.CharField(max_length=50, blank=True, null=True)
    driver_name = models.CharField(max_length=100)
    date_time = models.DateTimeField(default=timezone.now)
    purpose = models.TextField()
    
class WaitingBay(models.Model):
    security_gate = models.ForeignKey(SecurityGate, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    expected_wait_time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Waiting Bay'
        verbose_name_plural = 'Waiting Bays'

    def __str__(self):
        return f"Bay {self.pk}: {'Open' if self.status else 'Closed'}"

