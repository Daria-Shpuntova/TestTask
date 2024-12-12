from django.db import models

class FormTemplate(models.Model):
    name = models.CharField(max_length=255)
    fields = models.JSONField()  # Хранит поля в формате JSON

    def __str__(self):
        return self.name
