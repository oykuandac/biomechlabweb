from django.db import models
from django.forms import ModelForm, Textarea

# Create your models here.
class Files(models.Model):
	attachment = models.FileField()

	def __str__(self):
		return self.attachment

	def delete(self, *args, **kwargs):
		self.attachment.delete()
		super().delete(*args, **kwargs)

class Meta:
	db_table = "biomechlabwebapp_files"