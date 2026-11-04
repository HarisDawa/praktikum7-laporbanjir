@extends('layouts.app')
@section('title', 'Edit Laporan Banjir #' . $laporan->id)

@section('content')
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card shadow-sm border-0 mb-4">
            <div class="card-header bg-warning text-dark py-3">
                <h5 class="mb-0 fw-bold"><i class="fas fa-edit me-2"></i>Edit Data & Status Penanganan Laporan Banjir</h5>
                <small class="text-dark-50">Petugas dapat memperbarui data laporan, mengganti foto bukti, serta memperbarui status penanganan.</small>
            </div>
            <div class="card-body p-4">
                <form action="{{ route('laporans.update', $laporan) }}" method="POST" enctype="multipart/form-data">
                    @csrf
                    @method('PUT')

                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="nama_pelapor" class="form-label fw-semibold">Nama Lengkap Pelapor <span class="text-danger">*</span></label>
                            <input type="text" id="nama_pelapor" name="nama_pelapor"
                                value="{{ old('nama_pelapor', $laporan->nama_pelapor) }}"
                                class="form-control @error('nama_pelapor') is-invalid @enderror" required>
                            @error('nama_pelapor') <div class="invalid-feedback">{{ $message }}</div> @enderror
                        </div>

                        <div class="col-md-6 mb-3">
                            <label for="no_hp" class="form-label fw-semibold">Nomor WhatsApp / HP <span class="text-danger">*</span></label>
                            <input type="text" id="no_hp" name="no_hp"
                                value="{{ old('no_hp', $laporan->no_hp) }}"
                                class="form-control @error('no_hp') is-invalid @enderror" required>
                            @error('no_hp') <div class="invalid-feedback">{{ $message }}</div> @enderror
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-4 mb-3">
                            <label for="kecamatan" class="form-label fw-semibold">Kecamatan <span class="text-danger">*</span></label>
                            <select id="kecamatan" name="kecamatan" class="form-select @error('kecamatan') is-invalid @enderror" required>
                                @foreach (['Baleendah', 'Dayeuhkolot', 'Bojongsoang', 'Rancaekek', 'Majalaya', 'Ciparay', 'Lainnya'] as $kec)
                                    <option value="{{ $kec }}" {{ old('kecamatan', $laporan->kecamatan) == $kec ? 'selected' : '' }}>{{ $kec }}</option>
                                @endforeach
                            </select>
                            @error('kecamatan') <div class="invalid-feedback">{{ $message }}</div> @enderror
                        </div>

                        <div class="col-md-4 mb-3">
                            <label for="tinggi_air" class="form-label fw-semibold">Ketinggian Air (cm) <span class="text-danger">*</span></label>
                            <div class="input-group">
                                <input type="number" id="tinggi_air" name="tinggi_air"
                                    value="{{ old('tinggi_air', $laporan->tinggi_air) }}"
                                    class="form-control @error('tinggi_air') is-invalid @enderror" min="1" max="1000" required>
                                <span class="input-group-text">cm</span>
                                @error('tinggi_air') <div class="invalid-feedback">{{ $message }}</div> @enderror
                            </div>
                        </div>

                        <div class="col-md-4 mb-3">
                            <label for="status" class="form-label fw-semibold">Status Penanganan <span class="text-danger">*</span></label>
                            <select id="status" name="status" class="form-select @error('status') is-invalid @enderror" required>
                                <option value="Menunggu" {{ old('status', $laporan->status) == 'Menunggu' ? 'selected' : '' }}>Menunggu</option>
                                <option value="Diproses" {{ old('status', $laporan->status) == 'Diproses' ? 'selected' : '' }}>Diproses</option>
                                <option value="Selesai" {{ old('status', $laporan->status) == 'Selesai' ? 'selected' : '' }}>Selesai</option>
                            </select>
                            @error('status') <div class="invalid-feedback">{{ $message }}</div> @enderror
                        </div>
                    </div>

                    <div class="mb-3">
                        <label for="lokasi" class="form-label fw-semibold">Detail Alamat / Lokasi Kejadian <span class="text-danger">*</span></label>
                        <input type="text" id="lokasi" name="lokasi"
                            value="{{ old('lokasi', $laporan->lokasi) }}"
                            class="form-control @error('lokasi') is-invalid @enderror" required>
                        @error('lokasi') <div class="invalid-feedback">{{ $message }}</div> @enderror
                    </div>

                    <div class="mb-3">
                        <label for="keterangan" class="form-label fw-semibold">Keterangan / Situasi Terkini</label>
                        <textarea id="keterangan" name="keterangan" rows="3"
                            class="form-control @error('keterangan') is-invalid @enderror">{{ old('keterangan', $laporan->keterangan) }}</textarea>
                        @error('keterangan') <div class="invalid-feedback">{{ $message }}</div> @enderror
                    </div>

                    <div class="mb-4">
                        <label class="form-label fw-semibold d-block">Foto Bukti Saat Ini</label>
                        @if ($laporan->foto)
                            <div class="d-flex align-items-center mb-2 p-2 bg-light rounded border">
                                <img src="{{ asset('storage/' . $laporan->foto) }}" alt="Foto Lama"
                                    class="rounded me-3 border" width="100" height="75" style="object-fit: cover;">
                                <div>
                                    <div class="small fw-semibold text-muted">File: {{ basename($laporan->foto) }}</div>
                                    <a href="{{ asset('storage/' . $laporan->foto) }}" target="_blank" class="small text-decoration-none">
                                        <i class="fas fa-external-link-alt me-1"></i>Lihat foto saat ini
                                    </a>
                                </div>
                            </div>
                        @else
                            <p class="text-muted small">Belum ada foto yang tersimpan.</p>
                        @endif

                        <label for="foto" class="form-label fw-semibold mt-2">Ganti Foto (Kosongkan jika tidak ingin mengubah)</label>
                        <input type="file" id="foto" name="foto" accept="image/jpeg,image/png,image/jpg"
                            class="form-control @error('foto') is-invalid @enderror">
                        <div class="form-text text-muted">Format: JPG, JPEG, PNG. Maksimal 2 MB (2048 KB). Foto lama akan otomatis dihapus jika Anda memilih file baru.</div>
                        @error('foto') <div class="invalid-feedback">{{ $message }}</div> @enderror
                    </div>

                    <div class="d-flex justify-content-between align-items-center">
                        <a href="{{ route('laporans.index') }}" class="btn btn-secondary">
                            <i class="fas fa-times me-1"></i>Batal
                        </a>
                        <button type="submit" class="btn btn-warning px-4 fw-semibold text-dark">
                            <i class="fas fa-save me-1"></i>Perbarui Laporan
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
@endsection
