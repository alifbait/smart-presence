from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from karyawan.decorators import get_user_role

def home_view(request):
    """
    Halaman Beranda Utama.
    Jika pengguna sudah login, arahkan langsung ke dashboard.
    Jika belum, tampilkan halaman perkenalan awal.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    konteks = {
        'judul_halaman': 'Beranda | Smart Presence',
        'status_koneksi': 'Sukses terhubung ke database MySQL!',
    }
    return render(request, 'base.html', konteks)


def login_view(request):
    """
    Menangani proses masuk (login) pengguna.
    Jika pengguna sudah masuk, akan langsung diarahkan ke dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Selamat datang kembali, {user.first_name or user.username}! Anda berhasil masuk.")
                user_role = get_user_role(user)
                if user_role == 'superuser':
                    return redirect('/admin/')
                return redirect('dashboard')
        else:
            messages.error(request, "Nama pengguna atau kata sandi salah. Silakan periksa kembali.")
    else:
        form = AuthenticationForm()
        
    konteks = {
        'judul_halaman': 'Masuk ke Sistem | Smart Presence',
        'form': form
    }
    return render(request, 'login.html', konteks)


def logout_view(request):
    """
    Menangani proses keluar (logout) pengguna dari sistem.
    """
    logout(request)
    messages.info(request, "Anda telah berhasil keluar dari sistem. Sampai jumpa kembali!")
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    Halaman Utama Pengguna setelah berhasil masuk.
    Halaman ini diproteksi menggunakan dekorator @login_required.
    """
    from presensi.models import Presensi, PengajuanIzin
    
    # Deteksi profil pegawai secara aman untuk menghindari RelatedObjectDoesNotExist
    pegawai = getattr(request.user, 'pegawai', None)
    is_admin = request.user.is_superuser or request.user.is_staff
    
    if is_admin:
        pending_count = PengajuanIzin.objects.filter(status_persetujuan='Pending').count()
        recent_izin = PengajuanIzin.objects.all().order_by('-dibuat_pada')[:5]
    elif pegawai:
        pending_count = PengajuanIzin.objects.filter(pegawai=pegawai, status_persetujuan='Pending').count()
        recent_izin = PengajuanIzin.objects.filter(pegawai=pegawai).order_by('-dibuat_pada')[:5]
    else:
        pending_count = 0
        recent_izin = []

    if pegawai:
        # Hitung statistik kehadiran real-time dari database
        hadir = Presensi.objects.filter(pegawai=pegawai, status_kehadiran='Hadir').count()
        terlambat = Presensi.objects.filter(pegawai=pegawai, status_kehadiran='Terlambat').count()
        izin = Presensi.objects.filter(pegawai=pegawai, status_kehadiran='Izin').count()
        alpa = Presensi.objects.filter(pegawai=pegawai, status_kehadiran='Alpa').count()
        
        # Asumsikan total hari kerja bulan ini adalah 21 hari
        total_kerja = 21
        total_masuk = hadir + terlambat
        persentase = int((total_masuk / total_kerja) * 100) if total_kerja > 0 else 0
        if persentase > 100:
            persentase = 100
            
        kehadiran_stats = {
            'hadir': hadir,
            'terlambat': terlambat,
            'izin': izin,
            'alpa': alpa,
            'persentase_kehadiran': persentase
        }
    else:
        # Default statistik aman jika profil belum terdaftar
        kehadiran_stats = {
            'hadir': 0,
            'terlambat': 0,
            'izin': 0,
            'alpa': 0,
            'persentase_kehadiran': 0
        }
    
    # Ambil 5 absensi terbaru secara global (atau milik pegawai sendiri jika bukan superuser/staff)
    if request.user.is_superuser or request.user.is_staff:
        db_checkins = Presensi.objects.select_related('pegawai').order_by('-tanggal', '-jam_masuk')[:5]
    elif pegawai:
        db_checkins = Presensi.objects.filter(pegawai=pegawai).order_by('-tanggal', '-jam_masuk')[:5]
    else:
        db_checkins = []
        
    recent_checkins = []
    for c in db_checkins:
        waktu_str = f"{c.jam_masuk.strftime('%H:%M')} WIB" if c.jam_masuk else "-"
        status_class = 'success' if c.status_kehadiran == 'Hadir' else ('warning' if c.status_kehadiran == 'Terlambat' else 'info')
        tipe_icon = 'check-circle-fill' if c.status_kehadiran == 'Hadir' else ('exclamation-circle-fill' if c.status_kehadiran == 'Terlambat' else 'info-circle-fill')
        
        recent_checkins.append({
            'nama': c.pegawai.nama_lengkap,
            'waktu': waktu_str,
            'status': c.status_kehadiran,
            'status_class': status_class,
            'tipe_icon': tipe_icon
        })
        
    # Format tanggal hari ini dalam bahasa Indonesia
    hari_ini = timezone.now().strftime('%A, %d %B %Y')
    # Sederhana mengganti nama hari ke Indonesia
    hari_map = {
        'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu', 
        'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
    }
    bulan_map = {
        'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
        'April': 'April', 'May': 'Mei', 'June': 'Juni', 'July': 'Juli',
        'August': 'Agustus', 'September': 'September', 'October': 'Oktober',
        'November': 'November', 'December': 'Desember'
    }
    
    current_day = timezone.now().strftime('%A')
    current_month = timezone.now().strftime('%B')
    
    tanggal_formatted = timezone.now().strftime('%d %Y')
    hari_indo = hari_map.get(current_day, current_day)
    bulan_indo = bulan_map.get(current_month, current_month)
    
    tanggal_lengkap = f"{hari_indo}, {timezone.now().day} {bulan_indo} {timezone.now().year}"

    konteks = {
        'judul_halaman': 'Dashboard Utama | Smart Presence',
        'kehadiran_stats': kehadiran_stats,
        'recent_checkins': recent_checkins,
        'tanggal_lengkap': tanggal_lengkap,
        'pending_count': pending_count,
        'recent_izin': recent_izin,
        'is_admin': is_admin,
    }
    return render(request, 'dashboard.html', konteks)
