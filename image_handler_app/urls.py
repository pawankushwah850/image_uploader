from django.urls import path
from .views import ImageUploadView, UploadedImageDetails

app_name = "image_handler_app"

urlpatterns = [
    path('', ImageUploadView.as_view(), name="image-upload-view"),
    path('image_details/', UploadedImageDetails.as_view(), name="uploaded-image-details"),
    path('image_details/<int:pk>', UploadedImageDetails.as_view(), name="uploaded-image-details"),
]
