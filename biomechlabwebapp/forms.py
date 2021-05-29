from django import forms
from biomechlabwebapp.models import Files
class FilesForm(forms.ModelForm):
	class Meta:
		model =  Files
		fields = "__all__"