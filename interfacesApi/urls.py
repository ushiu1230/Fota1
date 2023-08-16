from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('file_management', views.file_management, name="file_management"),
    path('ecu_info', views.ecu_info, name="ecu_info"),
    path('upload_file', views.upload_file, name="upload_file"),
    path('list_files', views.list_files, name="list_files"),
    path('delete_files', views.delete_files, name="delete_files"),
    path('get_diag_messages',views.get_diag_messages,name='get_diag_messages'),
    
]
