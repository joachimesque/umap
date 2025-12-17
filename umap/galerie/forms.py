from django import forms
from . import models


class PicturesForm(forms.ModelForm):
    layer_point = forms.ModelChoiceField(
        queryset=models.LayerPoint.objects.all().order_by("pk")
    )
    files = forms.FileField(
        widget=forms.TextInput(
            attrs={
                "name": "files",
                "type": "file",
                "class": "form-control",
                "multiple": "true",
                "accept": "image/*",
            }
        ),
        label="Sélection des images",
    )

    class Meta:
        model = models.Picture
        fields = ["files", "layer_point"]
