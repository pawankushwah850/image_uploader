from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView
from .models import ImageHandlerModel
from .forms import ImageHandlerModelForm
from .utils import get_client_ip
from django.contrib.messages import success, error


class ImageUploadView(ListView, CreateView):

    def get(self, request, *args, **kwargs):
        image_handler_from = ImageHandlerModelForm(request=request)
        return render(request, "image_upload.html", context={"form": image_handler_from})

    def post(self, request, *args, **kwargs):
        user_ip = get_client_ip(self.request)
        upload_count = cache.get(user_ip)
        if upload_count is not None and upload_count >= 10:
            error(request, 'you cannot upload more then 10 images per-day/per-ip ')
            return redirect(reverse('image_handler_app:image-upload-view'))

        image_handler_form = ImageHandlerModelForm(self.request.POST, self.request.FILES, request=request)
        if image_handler_form.is_valid():
            image_handler_form.save()
            return redirect(reverse('image_handler_app:uploaded-image-details'))
        else:
            error(request, 'Form is not valid ')
            return redirect(reverse('image_handler_app:image-upload-view'))


class UploadedImageDetails(ListView):

    def get(self, request, *args, **kwargs):
        user_ip = get_client_ip(self.request)
        pk = kwargs.get('pk')
        if pk is not None:
            self.delete(pk, request)
        image_details = ImageHandlerModel.objects.filter(ip_address=user_ip)
        return render(request, 'image_details.html', context={"object_list": image_details})

    def delete(self, pk, request):
        try:
            ImageHandlerModel.objects.get(pk=pk).delete()
        except Exception as err:
            error(request, f"{err}")
        return redirect(reverse_lazy('image_handler_app:uploaded-image-details'))
