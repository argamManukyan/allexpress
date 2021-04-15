from django import forms
from .models import ProductVariantImages,ProductVariants


class ImageUploadForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)

    class Meta:
        model = ProductVariantImages
        fields = "__all__"

class VariantUploadForm(forms.ModelForm):

    class Meta:
        model = ProductVariants
        fields = "__all__"

