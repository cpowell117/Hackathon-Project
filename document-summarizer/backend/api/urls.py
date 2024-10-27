from django.urls import path
from .views import FileUploadView, InDepthAnalyticsView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('in-depth-analytics/', InDepthAnalyticsView.as_view(), name='in-depth-analytics')
]
