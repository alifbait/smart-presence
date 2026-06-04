"""
Decorator dan helper untuk sistem role Smart Presence.
Tersedia tiga role: superuser, admin, pegawai.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def get_user_role(user):
    """
    Mengembalikan role string dari user yang sedang login.
    - 'superuser'  : user.is_superuser = True
    - 'admin'      : user.is_staff = True, is_superuser = False, role='admin'
    - 'pegawai'    : user biasa dengan profil pegawai
    - None         : user belum login atau tidak punya profil
    """
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return 'superuser'
    pegawai = getattr(user, 'pegawai', None)
    if pegawai:
        return pegawai.role
    # Fallback: is_staff tanpa profil pegawai → admin
    if user.is_staff:
        return 'admin'
    return None


def role_required(*roles):
    """
    Decorator: hanya izinkan user dengan role tertentu.
    Contoh: @role_required('admin', 'superuser')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            user_role = get_user_role(request.user)
            if user_role in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "Akses ditolak: Anda tidak memiliki izin untuk halaman ini.")
            return redirect('dashboard')
        return _wrapped
    return decorator


def admin_or_superuser_required(view_func):
    """
    Decorator: hanya admin dan superuser yang boleh mengakses.
    Shortcut untuk @role_required('admin', 'superuser').
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        user_role = get_user_role(request.user)
        if user_role in ('admin', 'superuser'):
            return view_func(request, *args, **kwargs)
        messages.error(request, "Akses ditolak: Area khusus administrator.")
        return redirect('dashboard')
    return _wrapped


def pegawai_only(view_func):
    """
    Decorator: hanya pegawai biasa (bukan admin/superuser).
    Tidak memblokir admin, hanya memastikan ada profil pegawai.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        pegawai = getattr(request.user, 'pegawai', None)
        if not pegawai:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped
