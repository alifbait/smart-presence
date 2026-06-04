from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from karyawan.models import Pegawai
from karyawan.forms import PegawaiForm
from karyawan.decorators import admin_or_superuser_required

@login_required
@admin_or_superuser_required
def pegawai_list(request):
    """
    Menampilkan daftar seluruh pegawai.
    Mendukung pencarian nama, jabatan, divisi, atau username.
    """
    pencarian = request.GET.get('q', '')
    if pencarian:
        daftar_pegawai = Pegawai.objects.filter(
            Q(nama_lengkap__icontains=pencarian) |
            Q(jabatan__icontains=pencarian) |
            Q(divisi__icontains=pencarian) |
            Q(user__username__icontains=pencarian)
        ).select_related('user')
    else:
        daftar_pegawai = Pegawai.objects.all().select_related('user')

    konteks = {
        'judul_halaman': 'Manajemen User | Smart Presence',
        'daftar_pegawai': daftar_pegawai,
        'pencarian': pencarian,
    }
    return render(request, 'karyawan/pegawai_list.html', konteks)


@login_required
@admin_or_superuser_required
def pegawai_create(request):
    """
    Menangani pembuatan data Pegawai baru beserta akun User Django.
    Menggunakan transaksi atomik agar kedua data konsisten masuk atau dibatalkan.
    """
    if request.method == 'POST':
        form = PegawaiForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Buat User Django baru
                    role_dipilih = form.cleaned_data.get('role', 'pegawai')
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'],
                        first_name=form.cleaned_data['nama_lengkap']
                    )
                    # Sync is_staff dan is_superuser berdasarkan role
                    user.is_staff = role_dipilih in ('admin', 'superuser')
                    user.is_superuser = (role_dipilih == 'superuser')
                    user.save()

                    # 2. Buat profil Pegawai baru yang terhubung ke User
                    pegawai = form.save(commit=False)
                    pegawai.user = user
                    pegawai.save()
                    
                messages.success(request, f"Pegawai {pegawai.nama_lengkap} berhasil ditambahkan ke sistem.")
                return redirect('pegawai_list')
            except Exception as e:
                messages.error(request, f"Terjadi kesalahan sistem saat menyimpan data: {e}")
        else:
            messages.error(request, "Gagal menambahkan pegawai. Silakan periksa kembali isian form Anda.")
    else:
        form = PegawaiForm()

    konteks = {
        'judul_halaman': 'Tambah Pegawai Baru | Smart Presence',
        'form': form,
        'is_edit': False
    }
    return render(request, 'karyawan/pegawai_form.html', konteks)


@login_required
@admin_or_superuser_required
def pegawai_update(request, pk):
    """
    Menangani pembaruan data Pegawai dan akun User.
    """
    pegawai = get_object_or_404(Pegawai, pk=pk)
    
    if request.method == 'POST':
        form = PegawaiForm(request.POST, instance=pegawai, is_edit=True)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Update data User
                    role_dipilih = form.cleaned_data.get('role', 'pegawai')
                    user = pegawai.user
                    user.username = form.cleaned_data['username']
                    user.first_name = form.cleaned_data['nama_lengkap']
                    
                    # Sync is_staff dan is_superuser berdasarkan role
                    user.is_staff = role_dipilih in ('admin', 'superuser')
                    user.is_superuser = (role_dipilih == 'superuser')

                    # Jika kolom password diisi, update password
                    password = form.cleaned_data.get('password')
                    if password:
                        user.set_password(password)
                        
                    user.save()
                    
                    # 2. Update data Pegawai
                    form.save()
                    
                messages.success(request, f"Data pegawai {pegawai.nama_lengkap} berhasil diperbarui.")
                return redirect('pegawai_list')
            except Exception as e:
                messages.error(request, f"Terjadi kesalahan sistem saat memperbarui data: {e}")
        else:
            messages.error(request, "Gagal memperbarui data. Silakan periksa kembali isian form Anda.")
    else:
        form = PegawaiForm(instance=pegawai, is_edit=True)

    konteks = {
        'judul_halaman': f"Ubah Data {pegawai.nama_lengkap} | Smart Presence",
        'form': form,
        'pegawai': pegawai,
        'is_edit': True
    }
    return render(request, 'karyawan/pegawai_form.html', konteks)


@login_required
@admin_or_superuser_required
def pegawai_delete(request, pk):
    """
    Menghapus data Pegawai dan akun User terkait.
    """
    pegawai = get_object_or_404(Pegawai, pk=pk)
    
    # Mencegah pengguna menghapus akunnya sendiri yang sedang aktif digunakan
    if pegawai.user == request.user:
        messages.error(request, "Anda tidak dapat menghapus akun Anda sendiri yang sedang aktif digunakan.")
        return redirect('pegawai_list')
        
    nama_pegawai = pegawai.nama_lengkap
    try:
        # Menghapus User akan memicu cascade delete pada profil Pegawai secara otomatis
        pegawai.user.delete()
        messages.success(request, f"Akun pegawai {nama_pegawai} berhasil dihapus dari sistem.")
    except Exception as e:
        messages.error(request, f"Gagal menghapus data pegawai: {e}")
        
    return redirect('pegawai_list')
