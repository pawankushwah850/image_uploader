from django.db import models


class ImageHandlerModel(models.Model):
    ip_address = models.GenericIPAddressField(max_length=200, verbose_name="ip_address", blank=True, null=True)
    image = models.ImageField(upload_to="images/", null=False, blank=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return f'{self.pk}'

