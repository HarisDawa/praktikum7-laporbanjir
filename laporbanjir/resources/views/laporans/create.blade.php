@extends('layouts.app')
@section('title', 'Form Lapor Banjir - Warga')

@section('content')
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card shadow-sm border-0 mb-4">
            <div class="card-header bg-primary text-white py-3">
                <h5 class="mb-0 fw-bold"><i class="fas fa-bullhorn me-2"></i>Form Pengaduan Bencana Banjir Warga</h5>
                <small class="text-white-50">Silakan isi formulir di bawah ini dengan informasi akurat beserta foto bukti kondisi lapangan.</small>
            </div>
            <div class="card-body p-4">
                <form action="{{ route('laporans.store') }}" method="POST" enctype="multipart/form-data">
                    @csrf

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="nama_pelapor" class="form-label fw-semibold">Nama Lengkap Pelapor <span class="text-danger">*</span></label>
                            <input type="text" id="nama_pelapor" name="nama_pelapor" value="{{ old('nama_pelapor') }}"
                                class="form-control @error('nama_pelapor') is-invalid @enderror" placeholder="Contoh: Budi Santoso" required>
                            @error('nama_pelapor') <div class="invalid-feedback">{{ $message }}</div> @enderror
                        </div>

                        <div class="col-md-6 mb-3">
                            <label for="no_hp" class="form-label fw-semibold">Nomor WhatsApp / HP <span class="text-danger">*</span></label>
                            <input type="text" id="no_hp" name="no_hp" value="{{ old('no_hp') }}"
                                class="form-control @error('no_hp') is-invalid @enderror" placeholder="Contoh: 081234567890" required>
                            @error('no_hp') <div class="invalid-feedback">{{ $message }}</div> @enderror
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="kecamatan" class="form-label fw-semibold">Kecamatan <span class="text-danger">*</span></label>
                            <select id="kecamatan" name="kecamatan" class="form-select @error('kecamatan') is-invalid @enderror" required>
                                <option value="" disabled {{ old('kecamatan') ? '' : 'selected' }}>Pilih Kecamatan...</option>
                                <option value="Baleendah" {{ old('kecamatan') == 'Baleendah' ? 'selected' : '' }}>Baleendah</option>
                                <option value="Dayeuhkolot" {{ old('kecamatan') == 'Dayeuhkolot' ? 'selected' : '' }}>Dayeuhkolot</option>
                                <option value="Bojongsoang" {{ old('kecamatan') == 'Bojongsoang' ? 'selected' : '' }}>Bojongsoang</option>
                                <option value="Rancaekek" {{ old('kecamatan') == 'Rancaekek' ? 'selected' : '' }}>Rancaekek</option>
                                <option value="Majalaya" {{ old('kecamatan') == 'Majalaya' ? 'selected' : '' }}>Majalaya</option>
                                <option value="Ciparay" {{ old('kecamatan') == 'Ciparay' ? 'selected' : '' }}>Ciparay</option>
                                <option value="Lainnya" {{ old('kecamatan') == 'Lainnya' ? 'selected' : '' }}>Lainnya</option>
                            </select>
                            @error('kecamatan') <div class="invalid-feedback">{{ $message }}</div> @enderror
                        </div>

                        <div class="col-md-6 mb-3">
                            <label for="tinggi_air" class="form-label fw-semibold">Estimasi Ketinggian Air (cm) <span class="text-danger">*</span></label>
                            <div class="input-group">
                                <input type="number" id="tinggi_air" name="tinggi_air" value="{{ old('tinggi_air') }}"
                                    class="form-control @error('tinggi_air') is-invalid @enderror" placeholder="Contoh: 80" min="1" max="1000" required>
                                <span class="input-group-text">cm</span>
                                @error('tinggi_air') <div class="invalid-feedback">{{ $message }}</div> @enderror
                            </div>
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="lokasi" class="form-label fw-semibold">Detail Alamat / Lokasi Kejadian <span class="text-danger">*</span></label>
                        <input type="text" id="lokasi" name="lokasi" value="{{ old('lokasi') }}"
                            class="form-control @error('lokasi') is-invalid @enderror" placeholder="Contoh: Jl. Raya Dayeuhkolot No. 45, RT 02/RW 04" required>
                        @error('lokasi') <div class="invalid-feedback">{{ $message }}</div> @enderror
                    </div>

                    <div class="mb-3">
                        <label for="keterangan" class="form-label fw-semibold">Keterangan / Situasi Terkini</label>
                        <textarea id="keterangan" name="keterangan" rows="3"
                            class="form-control @error('keterangan') is-invalid @enderror"
                            placeholder="Deskripsikan kondisi terkini, akses jalan terputus, bantuan mendesak, dll.">{{ old('keterangan') }}</textarea>
                        @error('keterangan') <div class="invalid-feedback">{{ $message }}</div> @enderror
                    </div>

                    <div class="mb-4">
                        <label for="foto" class="form-label fw-semibold">Foto Bukti Banjir <span class="text-danger">*</span></label>
                        <input type="file" id="foto" name="foto" accept="image/jpeg,image/png,image/jpg"
                            class="form-control @error('foto') is-invalid @enderror" required>
                        <div class="form-text text-muted">Format: JPG, JPEG, PNG. Maksimal ukuran file: 2 MB (2048 KB).</div>
                        @error('foto') <div class="invalid-feedback">{{ $message }}</div> @enderror
                    </div>

                    <div class="d-flex justify-content-between align-items-center">
                        <button type="submit" class="btn btn-primary px-4 py-2 fw-semibold">
                            <i class="fas fa-paper-plane me-2"></i>Kirim Laporan Banjir
                        </button>
                        <span class="text-muted small">Tanda <span class="text-danger">*</span> wajib diisi</span>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
@endsection
