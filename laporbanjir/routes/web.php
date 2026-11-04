<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\LaporanController;

// Halaman utama langsung ke form Lapor Banjir (Akses Publik / Warga)
Route::get('/', function () {
    return redirect()->route('laporans.create');
});

// Route publik: Form input laporan warga & submit laporan
Route::get('/lapor', [LaporanController::class, 'create'])->name('laporans.create');
Route::post('/lapor', [LaporanController::class, 'store'])->name('laporans.store');

// Route Guest: Login & Register Petugas BPBD
Route::middleware('guest')->group(function () {
    Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
    Route::post('/login', [AuthController::class, 'login']);
    Route::get('/register', [AuthController::class, 'showRegister'])->name('register');
    Route::post('/register', [AuthController::class, 'register']);
});

// Route Auth: Pengelolaan Laporan Banjir oleh Petugas
Route::middleware('auth')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

    // Pengelolaan CRUD Laporan (index, show, edit, update, destroy)
    Route::get('/laporans', [LaporanController::class, 'index'])->name('laporans.index');
    Route::get('/laporans/{laporan}', [LaporanController::class, 'show'])->name('laporans.show');
    Route::get('/laporans/{laporan}/edit', [LaporanController::class, 'edit'])->name('laporans.edit');
    Route::put('/laporans/{laporan}', [LaporanController::class, 'update'])->name('laporans.update');
    Route::delete('/laporans/{laporan}', [LaporanController::class, 'destroy'])->name('laporans.destroy');
});
