@extends('layouts.app')
@section('title', 'Daftar Laporan Banjir - Petugas BPBD')

@section('content')
<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h3 class="fw-bold text-gray-800 mb-0"><i class="fas fa-clipboard-list text-primary me-2"></i>Daftar Laporan Bencana Banjir</h3>
        <p class="text-muted small mb-0">Kelola validasi, foto bukti, dan status tanggap darurat laporan banjir masuk.</p>
    </div>
    <a href="{{ route('laporans.create') }}" class="btn btn-outline-primary">
        <i class="fas fa-plus me-1"></i>Input Laporan Baru
    </a>
</div>

<div class="card shadow-sm border-0">
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="table table-hover table-bordered align-middle mb-0">
                <thead class="table-primary text-nowrap">
                    <tr>
                        <th class="text-center" width="5%">No</th>
                        <th class="text-center" width="12%">Foto Bukti</th>
                        <th>Pelapor & Kontak</th>
                        <th>Kecamatan & Lokasi</th>
                        <th class="text-center">Tinggi Air</th>
                        <th class="text-center">Status</th>
                        <th class="text-center">Waktu Masuk</th>
                        <th class="text-center" width="18%">Aksi Petugas</th>
                    </tr>
                </thead>
                <tbody>
                    @forelse ($laporans as $laporan)
                    <tr>
                        <td class="text-center fw-bold">{{ $laporans->firstItem() + $loop->index }}</td>
                        <td class="text-center">
                            @if ($laporan->foto)
                                <a href="{{ asset('storage/' . $laporan->foto) }}" target="_blank">
                                    <img src="{{ asset('storage/' . $laporan->foto) }}" alt="Foto Banjir"
                                        class="rounded shadow-sm border object-fit-cover" width="80" height="60">
                                </a>
                            @else
                                <span class="badge bg-secondary">Tidak Ada Foto</span>
                            @endif
                        </td>
                        <td>
                            <div class="fw-bold">{{ $laporan->nama_pelapor }}</div>
                            <small class="text-muted"><i class="fab fa-whatsapp text-success me-1"></i>{{ $laporan->no_hp }}</small>
                        </td>
                        <td>
                            <span class="badge bg-info text-dark mb-1">{{ $laporan->kecamatan }}</span>
                            <div class="small text-secondary">{{ Str::limit($laporan->lokasi, 45) }}</div>
                        </td>
                        <td class="text-center">
                            <span class="badge {{ $laporan->tinggi_air >= 100 ? 'bg-danger' : ($laporan->tinggi_air >= 50 ? 'bg-warning text-dark' : 'bg-primary') }} px-2 py-1">
                                {{ $laporan->tinggi_air }} cm
                            </span>
                        </td>
                        <td class="text-center">
                            @if ($laporan->status == 'Menunggu')
                                <span class="badge badge-menunggu px-2 py-1"><i class="fas fa-clock me-1"></i>Menunggu</span>
                            @elseif ($laporan->status == 'Diproses')
                                <span class="badge badge-diproses px-2 py-1"><i class="fas fa-spinner fa-spin me-1"></i>Diproses</span>
                            @else
                                <span class="badge badge-selesai px-2 py-1"><i class="fas fa-check-circle me-1"></i>Selesai</span>
                            @endif
                        </td>
                        <td class="text-center small text-muted">
                            {{ $laporan->created_at->format('d/m/Y') }}<br>
                            <span class="fw-semibold">{{ $laporan->created_at->format('H:i') }} WIB</span>
                        </td>
                        <td class="text-center text-nowrap">
                            <a href="{{ route('laporans.show', $laporan) }}" class="btn btn-sm btn-info text-white" title="Detail">
                                <i class="fas fa-eye"></i> Detail
                            </a>
                            <a href="{{ route('laporans.edit', $laporan) }}" class="btn btn-sm btn-warning text-dark" title="Edit">
                                <i class="fas fa-edit"></i> Edit
                            </a>
                            <form action="{{ route('laporans.destroy', $laporan) }}" method="POST" class="d-inline">
                                @csrf
                                @method('DELETE')
                                <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('Apakah Anda yakin ingin menghapus laporan ini? Data dan file foto akan dihapus permanen.')" title="Hapus">
                                    <i class="fas fa-trash-alt"></i> Hapus
                                </button>
                            </form>
                        </td>
                    </tr>
                    @empty
                    <tr>
                        <td colspan="8" class="text-center py-4 text-muted">
                            <i class="fas fa-info-circle me-2 fa-2x d-block mb-2 text-secondary"></i>
                            Belum ada laporan banjir yang masuk.
                        </td>
                    </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
    </div>
    @if ($laporans->hasPages())
    <div class="card-footer bg-white border-top py-3">
        <div class="d-flex justify-content-end">
            {{ $laporans->links() }}
        </div>
    </div>
    @endif
</div>
@endsection
