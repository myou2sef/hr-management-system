from django.db import models

class ZKDevice(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=15)
    port = models.IntegerField(default=4370)
    
    def __str__(self):
        return f"{self.name} ({self.ip_address})"

class AttendanceLog(models.Model):
    user_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=20)
    punch = models.CharField(max_length=20)
    device = models.ForeignKey(ZKDevice, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user_id} - {self.timestamp}"
