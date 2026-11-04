<?php

namespace App\Http\Controllers;

use App\Models\Laporan;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class LaporanController extends Controller
{
    /**
     * READ: Menampilkan daftar seluruh laporan banjir (untuk Petugas / Admin)
     */
    public function index()
    {
        $laporans = Laporan::latest()->paginate(5);
        return view('laporans.index', compact('laporans'));
    }

    /**
     * CREATE: Menampilkan form lapor banjir bagi warga
     */
    public function create()
    {
        return view('laporans.create');
    }

    /**
     * STORE: Memvalidasi & menyimpan laporan baru beserta upload foto bukti
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'nama_pelapor' => 'required|string|max:255',
            'no_hp'        => 'required|string|max:20',
            'lokasi'       => 'required|string|max:255',
            'kecamatan'    => 'required|string|max:100',
            'tinggi_air'   => 'required|integer|min:1|max:1000',
            'keterangan'   => 'nullable|string',
            'foto'         => 'required|image|mimes:jpg,jpeg,png|max:2048', // maks 2 MB
        ]);

        if ($request->hasFile('foto')) {
            $validated['foto'] = $request->file('foto')->store('foto_banjir', 'public');
        }

        $validated['status'] = 'Menunggu';

        Laporan::create($validated);

        return redirect()->route('laporans.create')->with('success', 'Laporan banjir Anda berhasil dikirim! Petugas BPBD akan segera menindaklanjuti.');
    }

    /**
     * SHOW: Menampilkan detail laporan tertentu
     */
    public function show(Laporan $laporan)
    {
        return view('laporans.show', compact('laporan'));
    }

    /**
     * EDIT: Menampilkan form update laporan & status penanganan
     */
    public function edit(Laporan $laporan)
    {
        return view('laporans.edit', compact('laporan'));
    }

    /**
     * UPDATE: Menyimpan perubahan data, mengganti foto (opsional), & status penanganan
     */
    public function update(Request $request, Laporan $laporan)
    {
        $validated = $request->validate([
            'nama_pelapor' => 'required|string|max:255',
            'no_hp'        => 'required|string|max:20',
            'lokasi'       => 'required|string|max:255',
            'kecamatan'    => 'required|string|max:100',
            'tinggi_air'   => 'required|integer|min:1|max:1000',
            'keterangan'   => 'nullable|string',
            'status'       => 'required|in:Menunggu,Diproses,Selesai',
            'foto'         => 'nullable|image|mimes:jpg,jpeg,png|max:2048',
        ]);

        if ($request->hasFile('foto')) {
            // Hapus foto lama jika ada
            if ($laporan->foto && Storage::disk('public')->exists($laporan->foto)) {
                Storage::disk('public')->delete($laporan->foto);
            }
            $validated['foto'] = $request->file('foto')->store('foto_banjir', 'public');
        }

        $laporan->update($validated);

        return redirect()->route('laporans.index')->with('success', 'Laporan banjir berhasil diperbarui.');
    }

    /**
     * DESTROY: Menghapus laporan banjir & foto fisik terkait
     */
    public function destroy(Laporan $laporan)
    {
        if ($laporan->foto && Storage::disk('public')->exists($laporan->foto)) {
            Storage::disk('public')->delete($laporan->foto);
        }

        $laporan->delete();

        return redirect()->route('laporans.index')->with('success', 'Laporan berhasil dihapus beserta foto bukti.');
    }
}
