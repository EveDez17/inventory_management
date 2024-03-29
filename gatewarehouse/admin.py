from django.contrib import admin
from .models import SecurityGate, AccessLog, SecurityGateTransaction, WaitingBay

admin.site.register(SecurityGate)
admin.site.register(AccessLog)
admin.site.register(SecurityGateTransaction)
admin.site.register(WaitingBay)
