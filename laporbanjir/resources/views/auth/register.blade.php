@extends('layouts.app')
@section('title', 'Registrasi Petugas BPBD')

@section('content')
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow-sm border-0 mb-4">
            <div class="card-header bg-primary text-white py-3 text-center">
                <i class="fas fa-id-card fa-2x mb-2 d-block"></i>
                <h5 class="mb-0 fw-bold">Registrasi Petugas BPBD</h5>
                <small class="text-white-50">Daftarkan akun resmi untuk staf/petugas lapangan BPBD</small>
            </div>
            <div class="card-body p-4">
                <form action="{{ route('register') }}" method="POST">
                    @csrf

                    <div class="mb-3">
                        <label for="name" class="form-label fw-semibold">Nama Lengkap & Gelar</label>
                        <input type="text" id="name" name="name" value="{{ old('name') }}"
                            class="form-control @error('name') is-invalid @enderror" placeholder="Contoh: Ahmad Haris Dawaa'ul Qulub" required autofocus>
                        @error('name') <div class="invalid-feedback">{{ $message }}</div> @enderror
                    </div>

                    <div class="mb-3">
                        <label for="email" class="form-label fw-semibold">Alamat Email Resmi</label>
                        <input type="email" id="email" name="email" value="{{ old('email') }}"
                            class="form-control @error('email') is-invalid @enderror" placeholder="haris@bpbd.bandungkab.go.id" required>
                        @error('email') <div class="invalid-feedback">{{ $message }}</div> @enderror
                    </div>

                    <div class="mb-3">
                        <label for="password" class="form-label fw-semibold">Password (Minimal 8 Karakter)</label>
                        <input type="password" id="password" name="password"
                            class="form-control @error('password') is-invalid @enderror" placeholder="••••••••" required>
                        @error('password') <div class="invalid-feedback">{{ $message }}</div> @enderror
                    </div>

                    <div class="mb-4">
                        <label for="password_confirmation" class="form-label fw-semibold">Konfirmasi Password</label>
                        <input type="password" id="password_confirmation" name="password_confirmation"
                            class="form-control" placeholder="Ulangi password di atas" required>
                    </div>

                    <div class="d-grid gap-2 mb-3">
                        <button type="submit" class="btn btn-primary fw-semibold py-2">
                            <i class="fas fa-user-check me-1"></i>Daftarkan Akun Petugas
                        </button>
                    </div>

                    <div class="text-center small text-muted">
                        Sudah memiliki akun? <a href="{{ route('login') }}" class="text-decoration-none fw-semibold">Masuk di sini</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
@endsection
