# LAPORAN PRAKTIKUM PEMROGRAMAN APLIKASI WEB
## MODUL 7 – CRUD DAN UPLOAD FILE PADA LARAVEL

**Nama Mahasiswa** : Ahmad Haris Dawaa'ul Qulub  
**NIM** : (Sesuaikan dengan NIM Anda)  
**Kelas** : IF / SI - 47 - PABW  
**Mata Kuliah** : Pemrograman Aplikasi Web (PABW)  
**Program Studi** : S1 Teknik Informatika / Sistem Informasi  
**Fakultas** : Fakultas Informatika, Universitas Telkom  
**Tahun Akademik** : 2026/2027  

---

## 1. Tujuan Praktikum
Setelah mengikuti dan menyelesaikan seluruh rangkaian praktikum Modul 7 ini, mahasiswa diharapkan:
1. Memahami konsep arsitektur **CRUD (Create, Read, Update, Delete)**, **Resource Controller**, serta penataan **Resource Route** bawaan framework Laravel secara komprehensif.
2. Memahami alur kerja pengunggahan berkas (**file upload**), mulai dari konfigurasi atribut formulir `enctype="multipart/form-data"`, validasi tipe MIME dan batas ukuran berkas, penyimpanan berkas pada disk public (`store()`), serta aktivasi tautan pintas publik (**symbolic link** via `php artisan storage:link`).
3. Mampu membangun sistem pengelolaan berkas menggunakan antarmuka modern, baik menggunakan **Laravel Breeze** maupun implementasi **Manual** berbasis layout Blade dan Bootstrap 5.
4. Menerapkan proteksi keamanan route menggunakan **Middleware Authentication** (`auth` & `guest`) sehingga data krusial hanya dapat dimanipulasi oleh pengguna atau petugas yang terverifikasi.
5. Menguasai manajemen berkas fisik di server storage, memastikan berkas lama terhapus otomatis saat data diperbarui atau dihapus menggunakan Facade `Storage::disk('public')->delete()`.
6. Menerapkan fitur CRUD dan upload berkas pada studi kasus nyata aplikasi pengaduan bencana **LaporBanjir** BPBD Kabupaten Bandung serta integrasi fitur unggah foto bukti insiden pada project Tugas Akhir **Smart Traffic Finder**.

---

## 2. Alat dan Bahan
- **Perangkat Keras**:
  - Laptop / PC dengan sistem operasi Windows 11 64-bit.
  - Processor Multi-Core (Intel / AMD), RAM 16 GB, SSD Storage.
- **Perangkat Lunak**:
  - Web Server & DBMS: **XAMPP v3.3.0** (Apache 2.4.58 & MariaDB 10.4.32, phpMyAdmin).
  - Runtime: **PHP v8.3.33** (CLI ZTS).
  - Dependency Manager: **Composer v2.8.x**.
  - Framework Backend: **Laravel Framework v11.x / v12.x**.
  - Frontend & Aset: Bootstrap 5.3.0 CDN, Tailwind CSS, Font Awesome 6.4.0.
  - Teks Editor: Visual Studio Code & PowerShell Terminal.
  - Browser Pengujian: Google Chrome & Selenium WebDriver Automation (Python 3.12).

---

## 3. Jawaban Tugas Pendahuluan

### 1. Apa yang dimaksud dengan CRUD? Jelaskan contoh penerapan setiap operasinya pada sebuah aplikasi web!
CRUD (*Create, Read, Update, Delete*) adalah empat operasi dasar dalam manipulasi persistensi data relasional:
- **Create (`INSERT`)**: Proses menambahkan rekaman data baru dari pengguna ke database. *Contoh*: Warga mengisi formulir pengaduan banjir lengkap dengan foto kondisi jalan lalu menekan tombol "Kirim Laporan".
- **Read (`SELECT`)**: Proses membaca dan menampilkan data dari tabel basis data ke antarmuka aplikasi. *Contoh*: Petugas BPBD melihat tabel daftar laporan banjir masuk yang dilengkapi thumbnail foto dan tombol pagination.
- **Update (`UPDATE`)**: Proses memperbarui rekaman data yang telah tersimpan. *Contoh*: Petugas memperbarui status penanganan laporan dari "Menunggu" menjadi "Diproses", atau mengganti foto bukti genangan air.
- **Delete (`DELETE`)**: Proses menghapus rekaman data dari basis data. *Contoh*: Petugas menghapus laporan palsu/duplikat, yang sekaligus memicu penghapusan berkas fisik fotonya dari direktori storage server.

### 2. Apa yang dimaksud dengan unggah berkas (file upload), dan bagaimana Laravel menanganinya dibandingkan dengan PHP murni?
Unggah berkas (*file upload*) adalah pengiriman berkas biner (gambar, dokumen arsip) dari perangkat klien ke server web melalui form HTTP POST.
- **PHP Murni**: Mengharuskan developer memproses variabel global `$_FILES` secara manual, memvalidasi ukuran dengan `$_FILES['file']['size']`, mengekstrak ekstensi dengan `pathinfo()`, melakukan sanitasi string nama file acak secara manual, dan memindahkan file dengan `move_uploaded_file()`. Hal ini rentan kesalahan logika dan celah keamanan.
- **Laravel**: Menyediakan API abstraksi yang sangat ringkas, aman, dan berstandar industri. Validasi dilakukan mudah lewat `$request->validate(['foto' => 'required|image|mimes:jpg,png|max:2048'])`. Penyimpanan dilakukan instan melalui `$request->file('foto')->store('folder', 'public')` yang secara otomatis meng-generate nama acak hash unik anti-tabrakan (*collision-free*).

### 3. Mengapa form untuk unggah berkas wajib menggunakan atribut `enctype="multipart/form-data"`?
Secara default, tag `<form>` menggunakan tipe enkripsi `application/x-www-form-urlencoded` yang hanya mampu mengirimkan pasangan data teks biasa. Apabila formulir menyertakan input `<input type="file">` tanpa atribut `enctype="multipart/form-data"`, browser hanya akan mengirimkan string nama berkasnya saja tanpa mengirimkan aliran byte biner aslinya. Akibatnya di sisi backend Laravel, `$request->file('...')` bernilai `null` dan validasi berkas akan selalu gagal.

### 4. Apa perbedaan menyimpan berkas di server (`storage/app/public`) dengan menyimpan path berkas di database? Mengapa keduanya diperlukan?
- **Penyimpanan Berkas di Server (`storage/app/public`)**: Berkas biner membutuhkan memori besar (ratusan KB hingga MB). Menyimpannya pada filesystem disk sistem operasi memungkinkan web server (Apache/Nginx) melakukan pengiriman (*streaming*) dan *caching* secara efisien tanpa membebani memori kerja database.
- **Penyimpanan Path di Database**: Tabel database hanya menyimpan path penunjuk relatif berupa teks singkat (contoh: `foto_banjir/hash.jpg`). Hal ini menjaga tabel tetap ramping, query pencarian tetap cepat, menghemat memori *buffer pool* database, serta memudahkan relasi data.

### 5. Mengapa validasi jenis dan ukuran file penting dilakukan sebelum berkas disimpan di server?
- **Keamanan (Security)**: Mencegah eksekusi *Remote Code Execution* (RCE). Tanpa validasi MIME type ketat di server, penyerang dapat menyusupkan skrip backdoor PHP berkedok foto yang dapat membahayakan server.
- **Ketersediaan & Stabilitas (Availability)**: Menghindari serangan *Denial of Service* (DoS) akibat pengisian kapasitas harddisk server secara sewenang-wenang (*Disk Exhaustion*) menggunakan unggahan berkas raksasa.

---

## 4. Langkah-Langkah Praktikum

### 4.1 Pengerjaan Tugas 1: Aplikasi LaporBanjir BPBD Kabupaten Bandung
Aplikasi dikembangkan menggunakan pendekatan **Manual (Blade Layout & Bootstrap 5)** dengan alasan:
1. **Kebutuhan Akses Publik**: Warga dapat melaporkan kejadian banjir secara cepat tanpa keharusan mendaftar/login terlebih dahulu.
2. **Kemandirian Dependensi**: Bootstrap 5 dimuat via CDN, sehingga ringan, cepat, dan tidak memerlukan proses kompilasi Node.js/NPM saat dijalankan.
3. **Fleksibilitas Arsitektur**: Struktur controller, middleware auth petugas, dan form publik dapat diatur secara mandiri dan transparan.

#### Tahap 1: Konfigurasi Database dan Environment
Project dibuat di dalam folder `E:\Kuliah\PABW\praktikum7\laporbanjir` dan dikoneksikan ke MySQL database `db_laporbanjir`:
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=db_laporbanjir
DB_USERNAME=root
DB_PASSWORD=
```

#### Tahap 2: Pembuatan Migration dan Model Laporan
Dibuat model `Laporan` beserta migrasi skema tabelnya:
```bash
php artisan make:model Laporan -m
```
Skema tabel pada file migrasi memuat kolom wajib:
```php
Schema::create('laporans', function (Blueprint $table) {
    $table->id();
    $table->string('nama_pelapor');
    $table->string('no_hp', 20);
    $table->string('lokasi');
    $table->string('kecamatan');
    $table->integer('tinggi_air'); // dalam cm
    $table->text('keterangan')->nullable();
    $table->string('foto'); // path berkas foto bukti
    $table->enum('status', ['Menunggu', 'Diproses', 'Selesai'])->default('Menunggu');
    $table->timestamps();
});
```

#### Tahap 3: Pembuatan Symbolic Link Storage
Agar file di folder `storage/app/public` dapat diakses dari browser:
```bash
php artisan storage:link
```

#### Tahap 4: Implementasi Controller (CRUD & Logika Upload File)
Dibuat `LaporanController` dan `AuthController`. Pada method `store()` laporan baru:
```php
$validated = $request->validate([
    'nama_pelapor' => 'required|string|max:255',
    'no_hp'        => 'required|string|max:20',
    'lokasi'       => 'required|string|max:255',
    'kecamatan'    => 'required|string|max:100',
    'tinggi_air'   => 'required|integer|min:1|max:1000',
    'keterangan'   => 'nullable|string',
    'foto'         => 'required|image|mimes:jpg,jpeg,png|max:2048',
]);

if ($request->hasFile('foto')) {
    $validated['foto'] = $request->file('foto')->store('foto_banjir', 'public');
}

$validated['status'] = 'Menunggu';
Laporan::create($validated);
```

Pada method `update()` dan `destroy()`, foto lama dihapus dari storage fisik:
```php
// Menghapus foto lama saat foto baru diunggah
if ($request->hasFile('foto')) {
    if ($laporan->foto && Storage::disk('public')->exists($laporan->foto)) {
        Storage::disk('public')->delete($laporan->foto);
    }
    $validated['foto'] = $request->file('foto')->store('foto_banjir', 'public');
}

// Menghapus foto fisik saat laporan dihapus
if ($laporan->foto && Storage::disk('public')->exists($laporan->foto)) {
    Storage::disk('public')->delete($laporan->foto);
}
$laporan->delete();
```

#### Tahap 5: Pengaturan Route & Proteksi Middleware Auth Petugas
File `routes/web.php` mengatur akses formulir warga secara terbuka, sementara dashboard manajemen laporan dikunci di balik middleware `auth`:
```php
Route::get('/', fn() => redirect()->route('laporans.create'));
Route::get('/lapor', [LaporanController::class, 'create'])->name('laporans.create');
Route::post('/lapor', [LaporanController::class, 'store'])->name('laporans.store');

Route::middleware('guest')->group(function () {
    Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
    Route::post('/login', [AuthController::class, 'login']);
    Route::get('/register', [AuthController::class, 'showRegister'])->name('register');
    Route::post('/register', [AuthController::class, 'register']);
});

Route::middleware('auth')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout'])->name('logout');
    Route::resource('laporans', LaporanController::class)->except(['create', 'store']);
});
```

---

### 4.2 Penerapan pada Project Tugas Akhir (Smart Traffic Finder)
Pada aplikasi Tugas Akhir **Smart Traffic Finder** (`E:\Kuliah\PABW\PABW`), fitur CRUD laporan insiden lalu lintas disempurnakan dengan standar pengujian Modul 7:
1. Validasi berkas diperketat pada batas maksimal 2 MB (2048 KB) serta dukungan format gambar jpg, jpeg, png.
2. Penyimpanan berkas menggunakan disk `public` Laravel (`foto_laporan/`) yang terhubung langsung melalui symbolic link `public/storage`.
3. Pada method `update()` dan `destroy()`, ditambahkan validasi keberadaan berkas lama melalui `Storage::disk('public')->delete()` agar direktori server bebas dari penumpukan berkas yang tidak terpakai.
4. Halaman kelola laporan diproteksi menggunakan middleware `auth`.

---

## 5. Hasil dan Dokumentasi Program

Seluruh tangkapan layar pengujian antarmuka dan basis data tersimpan di folder `screenshots/`:

| No | Nama Gambar | Keterangan & Analisis Hasil |
|---|---|---|
| 1 | `01_laporbanjir_form_warga.png` | **Form Lapor Banjir Warga**: Halaman publik berisi input nama, no HP, kecamatan, ketinggian genangan air, alamat, keterangan, dan input berkas foto bukti. |
| 2 | `02_laporbanjir_validasi_error.png` | **Validasi Galat File**: Pesan kesalahan merah muncul saat pengguna mencoba mengunggah berkas non-gambar (`.txt`). |
| 3 | `03_laporbanjir_lapor_sukses.png` | **Pengiriman Berhasil**: Laporan sukses dikirim dengan foto format JPG, data masuk ke database dan notifikasi sukses hijau tampil. |
| 4 | `04_laporbanjir_middleware_redirect.png` | **Proteksi Auth**: Akses rute `/laporans` tanpa login otomatis dialihkan oleh middleware ke form Login Petugas BPBD. |
| 5 | `05_laporbanjir_register_petugas.png` | **Registrasi Petugas**: Form pendaftaran akun staf/petugas BPBD dengan validasi password confirmation. |
| 6 | `06_laporbanjir_kelola_daftar.png` | **Daftar Laporan (Petugas)**: Menampilkan tabel laporan masuk lengkap dengan thumbnail gambar, badge status, info waktu, dan tombol aksi. |
| 7 | `07_laporbanjir_detail.png` | **Detail Laporan**: Rincian informasi banjir dan pratinjau gambar bukti lapangan dalam ukuran penuh. |
| 8 | `08_laporbanjir_form_edit.png` | **Edit Laporan & Status**: Petugas memperbarui data, mengubah status penanganan menjadi 'Diproses', dan memilih foto pengganti. |
| 9 | `09_laporbanjir_setelah_update.png` | **Hasil Update**: Status penanganan dan thumbnail foto diperbarui, file lama telah dihapus dari storage. |
| 10 | `10_laporbanjir_detail_foto_baru.png` | **Detail dengan Foto Baru**: Tampilan foto hasil pembaruan regu tanggap darurat di lapangan. |
| 11 | `11_tubes_daftar_laporan.png` | **Tubes - Smart Traffic Finder**: Halaman data laporan insiden jalan raya perkotaan. |
| 12 | `12_tubes_form_tambah_foto.png` | **Tubes - Upload Foto Bukti**: Form tambah laporan dengan unggah foto bukti kemacetan langsung dari lokasi. |
| 13 | `13_tubes_daftar_setelah_tambah.png` | **Tubes - Data Tersimpan**: Laporan lalu lintas baru beserta foto berhasil tersimpan di sistem. |

---

## 6. Analisis dan Pembahasan
1. **Efektivitas Resource Controller**: Penerapan resource controller memangkas duplikasi kode routing dan memudahkan pemeliharaan arsitektur kode (*maintainability*).
2. **Pemisahan Filesystem dan DBMS**: Menempatkan berkas fisik di `storage/app/public` dan hanya menyimpan string path di basis data menghasilkan efisiensi memori InnoDB buffer pool yang optimal dan mempercepat waktu *response time* aplikasi.
3. **Pentingnya Validasi MIME Server-Side**: Validasi sisi klien tidak menjamin keamanan sistem; validasi `mimes:jpg,jpeg,png|max:2048` di sisi controller adalah garda utama penangkal serangan RCE dan DoS.
4. **Pembersihan Berkas Otomatis**: Penggunaan `Storage::disk('public')->delete()` berhasil mencegah penumpukan file *orphan* di server saat data diperbarui atau dihapus.

---

## 7. Kesimpulan
1. Praktikum Modul 7 berhasil diselesaikan dengan mengimplementasikan seluruh operasi CRUD dan upload berkas pada Laravel secara sempurna.
2. Aplikasi **LaporBanjir** BPBD Kabupaten Bandung dan integrasi fitur unggah bukti kejadian pada project Tugas Akhir **Smart Traffic Finder** telah berfungsi penuh, aman, responsif, dan terproteksi middleware authentication.
3. Seluruh pengujian fitur, validasi galat, pengalihan otentikasi, serta pengujian otomatis (*automated test*) berjalan sukses (*passed*).

---

## 8. Lampiran Link Repositori GitHub
Seluruh kode sumber (source code) aplikasi LaporBanjir dan integrasi fitur CRUD file upload pada Tugas Akhir telah dikelola menggunakan Git Version Control dan dihubungkan ke akun GitHub resmi:

| No | Nama Repositori / Proyek | Tautan Repositori GitHub Resmi |
|---|---|---|
| 1 | **Praktikum Modul 7 (Aplikasi LaporBanjir & CRUD)** | [https://github.com/HarisDawa/praktikum7-laporbanjir.git](https://github.com/HarisDawa/praktikum7-laporbanjir.git) |
| 2 | **Tugas Akhir PABW (Smart Traffic Finder)** | [https://github.com/HarisDawa/PABW_TA.git](https://github.com/HarisDawa/PABW_TA.git) |

### Perintah Push ke GitHub untuk Mahasiswa:
Untuk mem-push commit repositori `praktikum7-laporbanjir` yang sudah disiapkan ke GitHub pribadi:
```bash
cd E:\Kuliah\PABW\praktikum7
git push -u origin main
```
Untuk mem-push commit pembaruan pada repositori Tugas Akhir (`PABW_TA`):
```bash
cd E:\Kuliah\PABW\PABW
git push origin main
```
