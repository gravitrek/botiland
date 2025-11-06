"""
URL patterns for qrcodes app.
"""
from django.urls import path
from .views import (
    QRCodeListCreateView,
    QRCodeDetailView,
    QRCodeDownloadView,
    BulkQRCodeCreateView,
    TagListCreateView,
    QRTemplateListView,
)

app_name = 'qrcodes'

urlpatterns = [
    path('', QRCodeListCreateView.as_view(), name='qr_list_create'),
    path('<uuid:pk>/', QRCodeDetailView.as_view(), name='qr_detail'),
    path('<uuid:pk>/download/', QRCodeDownloadView.as_view(), name='qr_download'),
    path('bulk/', BulkQRCodeCreateView.as_view(), name='qr_bulk_create'),
    path('tags/', TagListCreateView.as_view(), name='tag_list_create'),
    path('templates/', QRTemplateListView.as_view(), name='template_list'),
]
