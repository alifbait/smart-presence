from django.urls import path
from karyawan import views

urlpatterns = [
    # Rute Manajemen Pegawai (CRUD)
    path('', views.pegawai_list, name='pegawai_list'),
    path('tambah/', views.pegawai_create, name='pegawai_create'),
    path('edit/<int:pk>/', views.pegawai_update, name='pegawai_update'),
    path('hapus/<int:pk>/', views.pegawai_delete, name='pegawai_delete'),
]
