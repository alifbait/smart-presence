"""
URL configuration for smart_presence project.

Gaya koding di bawah ini dibuat dengan dokumentasi bahasa Indonesia
agar sangat mudah dipahami oleh pemula.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from smart_presence import views

urlpatterns = [
    # Rute ke Admin Panel bawaan Django
    path('admin/', admin.site.urls),
    
    # Rute halaman utama (landing page)
    path('', views.home_view, name='home'),
    
    # Rute Autentikasi
    path('masuk/', views.login_view, name='login'),
    path('keluar/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Rute Manajemen Karyawan
    path('karyawan/', include('karyawan.urls')),
    
    # Rute Presensi / Absensi Pegawai
    path('presensi/', include('presensi.urls')),
    
    # Rute Pengajuan Izin / Sakit / Cuti
    path('izin/', include('presensi.urls_izin')),
]

# Konfigurasi tambahan agar file media dan static bisa diakses di mode pengembangan (DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
