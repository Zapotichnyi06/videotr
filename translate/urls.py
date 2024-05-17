from django.urls import path
from .views import process_video_view, index

urlpatterns = [
    path('', index, name='index'),
    path('process/', process_video_view, name='process_video_view'),
]