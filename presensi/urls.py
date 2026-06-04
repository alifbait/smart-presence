from django.urls import path
from presensi import views

urlpatterns = [
    # Rute Absensi Utama & Harian
    path('', views.presensi_harian, name='presensi_harian'),
    path('masuk/', views.presensi_masuk, name='presensi_masuk'),
    path('pulang/', views.presensi_pulang, name='presensi_pulang'),
    path('riwayat/', views.presensi_riwayat, name='presensi_riwayat'),

    # Rute Laporan & Ekspor Data
    path('laporan/', views.laporan_presensi, name='laporan_presensi'),
    path('laporan/excel/', views.export_excel, name='export_excel'),
    path('laporan/pdf/', views.export_pdf, name='export_pdf'),

    # Internal Holiday Service API
    path('api/hari-libur/', views.api_hari_libur, name='api_hari_libur'),
]
