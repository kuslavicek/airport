from django.db import models
from django.utils.timezone import now

class Plane(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="flying")  # e.g., flying, landed, at gate, etc.
    location = models.CharField(max_length=50, blank=True, null=True)  # Location (runway, gate, hangar)
    updated_at = models.DateTimeField(default=now)  # Last updated timestamp

    def save(self, *args, **kwargs):
        self.updated_at = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Runway(models.Model):
    name = models.CharField(max_length=50)
    is_free = models.BooleanField(default=True)
    current_plane = models.ForeignKey(Plane, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Gate(models.Model):
    name = models.CharField(max_length=50)
    is_free = models.BooleanField(default=True)
    current_plane = models.ForeignKey(Plane, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Hangar(models.Model):
    name = models.CharField(max_length=50)
    is_free = models.BooleanField(default=True)
    current_plane = models.ForeignKey(Plane, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
