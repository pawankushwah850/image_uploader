from django import forms
from django.core.cache import cache

from .models import ImageHandlerModel
from .utils import get_client_ip


class ImageHandlerModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user_ip = get_client_ip(kwargs.pop("request"))
        super(ImageHandlerModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ImageHandlerModel
        fields = ('image',)

    def save(self, commit=True):
        instance = super(ImageHandlerModelForm, self).save()
        instance.ip_address = self.user_ip
        instance.save()
        upload_count = cache.get(self.user_ip)
        if upload_count:
            cache.set(self.user_ip, upload_count + 1)
        else:
            cache.set(self.user_ip, 1)

        return instance
