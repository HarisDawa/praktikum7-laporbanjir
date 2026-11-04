@extends('layouts.app')
@section('title', 'Detail Laporan Banjir #' . $laporan->id)

@section('content')
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card shadow-sm border-0 mb-4">
            <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center py-3">
                <h5 class="mb-0 fw-bold"><i class="fas fa-info-circle me-2"></i>Detail Laporan Banjir #{{ $laporan->id }}</h5>
                <span class="badge {{ $laporan->status == 'Selesai' ? 'bg-success' : ($laporan->status == 'Diproses' ? 'bg-info' : 'bg-warning text-dark') }} fs-6">
                    Status: {{ $laporan->status }}
                </span>
            </div>
            <div class="card-body p-4">
                <div class="row mb-4">
                    <div class="col-md-7">
                        <table class="table table-borderless">
                            <tr>
                                <th width="35%" class="text-muted"><i class="fas fa-user me-2"></i>Nama Pelapor</th>
                                <td class="fw-bold">: {{ $laporan->nama_pelapor }}</td>
                            </tr>
                            <tr>
                                <th class="text-muted"><i class="fab fa-whatsapp me-2"></i>Nomor HP</th>
                                <td>: <a href="https://wa.me/{{ preg_replace('/[^0-9]/', '', $laporan->no_hp) }}" target="_blank" class="text-decoration-none">{{ $laporan->no_hp }}</a></td>
                            </tr>
                            <tr>
                                <th class="text-muted"><i class="fas fa-map-marker-alt me-2"></i>Kecamatan</th>
                                <td>: <span class="badge bg-secondary">{{ $laporan->kecamatan }}</span></td>
                            </tr>
                            <tr>
                                <th class="text-muted"><i class="fas fa-location-arrow me-2"></i>Alamat/Lokasi</th>
                                <td>: {{ $laporan->lokasi }}</td>
                            </tr>
                            <tr>
                                <th class="text-muted"><i class="fas fa-ruler-vertical me-2"></i>Ketinggian Air</th>
                                <td>: <strong class="text-danger fs-5">{{ $laporan->tinggi_air }} cm</strong></td>
                            </tr>
                            <tr>
                                <th class="text-muted"><i class="fas fa-clock me-2"></i>Waktu Dilaporkan</th>
                                <td>: {{ $laporan->created_at->format('d F Y, H:i') }} WIB ({{ $laporan->created_at->diffForHumans() }})</td>
                            </tr>
                            <tr>
                                <th class="text-muted"><i class="fas fa-align-left me-2"></i>Keterangan</th>
                                <td>: {{ $laporan->keterangan ?? '-' }}</td>
                            </tr>
                        </table>
                    </div>
                    <div class="col-md-5 text-center">
                        <label class="fw-semibold text-muted mb-2 d-block">Foto Bukti Lapangan</label>
                        @if ($laporan->foto)
                            <a href="{{ asset('storage/' . $laporan->foto) }}" target="_blank">
                                <img src="{{ asset('storage/' . $laporan->foto) }}" alt="Foto Bukti Banjir"
                                    class="img-fluid rounded shadow border" style="max-height: 240px; object-fit: cover;">
                            </a>
                            <div class="mt-2">
                                <a href="{{ asset('storage/' . $laporan->foto) }}" target="_blank" class="btn btn-outline-secondary btn-sm">
                                    <i class="fas fa-external-link-alt me-1"></i>Buka Resolusi Penuh
                                </a>
                            </div>
                        @else
                            <div class="p-4 bg-light rounded border text-muted">Tidak ada foto bukti.</div>
                        @endif
                    </div>
                </div>

                <div class="d-flex justify-content-between pt-3 border-top">
                    <a href="{{ route('laporans.index') }}" class="btn btn-secondary">
                        <i class="fas fa-arrow-left me-1"></i>Kembali ke Daftar
                    </a>
                    <div>
                        <a href="{{ route('laporans.edit', $laporan) }}" class="btn btn-warning text-dark me-2">
                            <i class="fas fa-edit me-1"></i>Perbarui Laporan / Status
                        </a>
                        <form action="{{ route('laporans.destroy', $laporan) }}" method="POST" class="d-inline">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-danger" onclick="return confirm('Apakah Anda yakin ingin menghapus laporan ini beserta file fotonya?')">
                                <i class="fas fa-trash-alt me-1"></i>Hapus
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
