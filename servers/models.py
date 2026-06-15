from django.db import models
from django.contrib.auth.models import User

class Server(models.Model):
    server_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    config_bin = models.BinaryField(blank=True, null=True, default=b'')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servers')
    
    def __str__(self):
        return self.server_name
