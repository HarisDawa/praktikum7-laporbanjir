@extends('layouts.app')
@section('title', 'Login Petugas BPBD')

@section('content')
<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card shadow-sm border-0 mb-4">
            <div class="card-header bg-primary text-white py-3 text-center">
                <i class="fas fa-user-shield fa-2x mb-2 d-block"></i>
                <h5 class="mb-0 fw-bold">Login Petugas BPBD</h5>
                <small class="text-white-50">Masuk untuk mengelola dan memverifikasi laporan banjir warga</small>
            </div>
            <div class="card-body p-4">
                <form action="{{ route('login') }}" method="POST">
                    @csrf

                    <div class="mb-3">
                        <label for="email" class="form-label fw-semibold">Alamat Email</label>
                        <div class="input-group">
                            <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                            <input type="email" id="email" name="email" value="{{ old('email') }}"
                                class="form-control @error('email') is-invalid @enderror" placeholder="petugas@bpbd.go.id" required autofocus>
                        </div>
                        @error('email') <div class="text-danger small mt-1">{{ $message }}</div> @enderror
                    </div>

                    <div class="mb-3">
                        <label for="password" class="form-label fw-semibold">Password</label>
                        <div class="input-group">
                            <span class="input-group-text"><i class="fas fa-lock"></i></span>
                            <input type="password" id="password" name="password"
                                class="form-control @error('password') is-invalid @enderror" placeholder="••••••••" required>
                        </div>
                        @error('password') <div class="text-danger small mt-1">{{ $message }}</div> @enderror
                    </div>

                    <div class="mb-3 form-check">
                        <input type="checkbox" id="remember" name="remember" class="form-check-input">
                        <label for="remember" class="form-check-label text-muted small">Ingat saya pada perangkat ini</label>
                    </div>

                    <div class="d-grid gap-2 mb-3">
                        <button type="submit" class="btn btn-primary fw-semibold py-2">
                            <i class="fas fa-sign-in-alt me-1"></i>Masuk Sekarang
                        </button>
                    </div>

                    <div class="text-center small text-muted">
                        Belum punya akun petugas? <a href="{{ route('register') }}" class="text-decoration-none fw-semibold">Daftar Akun Baru</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
@endsection
