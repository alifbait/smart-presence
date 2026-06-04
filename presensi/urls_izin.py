from django.urls import path
from presensi import views

urlpatterns = [
    # Rute Pengajuan Izin Pegawai
    path('', views.riwayat_izin, name='riwayat_izin'),
    path('riwayat/', views.riwayat_izin, name='riwayat_izin_alias'),
    path('ajukan/', views.ajukan_izin, name='ajukan_izin'),
    
    # Rute Manajemen Admin untuk Persetujuan
    path('admin/', views.admin_izin, name='admin_izin'),
    path('setujui/<int:izin_id>/', views.setujui_izin, name='setujui_izin'),
    path('tolak/<int:izin_id>/', views.tolak_izin, name='tolak_izin'),
]
