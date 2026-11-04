import os
import pygments
from pygments.lexers import PhpLexer, BashLexer, HtmlLexer
from pygments.formatters import HtmlFormatter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

OUTPUT_DIR = r"E:\Kuliah\PABW\praktikum7\codesnaps"
os.makedirs(OUTPUT_DIR, exist_ok=True)

codesnap_items = [
    {
        "filename": "01_migration_laporans.png",
        "title": "database/migrations/..._create_laporans_table.php",
        "lexer": PhpLexer(),
        "code": """public function up(): void
{
    Schema::create('laporans', function (Blueprint $table) {
        $table->id();
        $table->string('nama_pelapor');
        $table->string('no_hp', 20);
        $table->string('lokasi');
        $table->string('kecamatan');
        $table->integer('tinggi_air'); // dalam cm
        $table->text('keterangan')->nullable();
        $table->string('foto'); // path berkas foto di storage
        $table->enum('status', ['Menunggu', 'Diproses', 'Selesai'])->default('Menunggu');
        $table->timestamps();
    });
}"""
    },
    {
        "filename": "02_model_laporan.png",
        "title": "app/Models/Laporan.php",
        "lexer": PhpLexer(),
        "code": """<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Laporan extends Model
{
    protected $table = 'laporans';

    protected $fillable = [
        'nama_pelapor',
        'no_hp',
        'lokasi',
        'kecamatan',
        'tinggi_air',
        'keterangan',
        'foto',
        'status',
    ];
}"""
    },
    {
        "filename": "03_store_laporan_upload.png",
        "title": "app/Http/Controllers/LaporanController.php - store()",
        "lexer": PhpLexer(),
        "code": """public function store(Request $request)
{
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

    return redirect()->route('laporans.create')
        ->with('success', 'Laporan banjir Anda berhasil dikirim! Petugas BPBD akan segera menindaklanjuti.');
}"""
    },
    {
        "filename": "04_update_destroy_storage.png",
        "title": "app/Http/Controllers/LaporanController.php - update() & destroy()",
        "lexer": PhpLexer(),
        "code": """public function update(Request $request, Laporan $laporan)
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
        if ($laporan->foto && Storage::disk('public')->exists($laporan->foto)) {
            Storage::disk('public')->delete($laporan->foto); // Hapus foto lama
        }
        $validated['foto'] = $request->file('foto')->store('foto_banjir', 'public');
    }

    $laporan->update($validated);
    return redirect()->route('laporans.index')->with('success', 'Laporan banjir berhasil diperbarui.');
}

public function destroy(Laporan $laporan)
{
    if ($laporan->foto && Storage::disk('public')->exists($laporan->foto)) {
        Storage::disk('public')->delete($laporan->foto); // Hapus foto fisik
    }
    $laporan->delete();
    return redirect()->route('laporans.index')->with('success', 'Laporan berhasil dihapus beserta foto bukti.');
}"""
    },
    {
        "filename": "05_routes_web.png",
        "title": "routes/web.php",
        "lexer": PhpLexer(),
        "code": """// Route Publik (Pengaduan Warga)
Route::get('/', fn() => redirect()->route('laporans.create'));
Route::get('/lapor', [LaporanController::class, 'create'])->name('laporans.create');
Route::post('/lapor', [LaporanController::class, 'store'])->name('laporans.store');

// Route Guest (Petugas Login & Register)
Route::middleware('guest')->group(function () {
    Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
    Route::post('/login', [AuthController::class, 'login']);
    Route::get('/register', [AuthController::class, 'showRegister'])->name('register');
    Route::post('/register', [AuthController::class, 'register']);
});

// Route Auth (Pengelolaan Laporan Bencana oleh Petugas)
Route::middleware('auth')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout'])->name('logout');
    Route::resource('laporans', LaporanController::class)->except(['create', 'store']);
});"""
    },
    {
        "filename": "06_auth_controller.png",
        "title": "app/Http/Controllers/AuthController.php",
        "lexer": PhpLexer(),
        "code": """public function login(Request $request): RedirectResponse
{
    $credentials = $request->validate([
        'email'    => 'required|string|email',
        'password' => 'required|string',
    ]);

    if (Auth::attempt($credentials, $request->boolean('remember'))) {
        $request->session()->regenerate();
        return redirect()->intended(route('laporans.index'))
            ->with('success', 'Login berhasil. Selamat datang kembali!');
    }

    return back()->withErrors(['email' => 'Email atau password salah.'])->onlyInput('email');
}

public function logout(Request $request): RedirectResponse
{
    Auth::logout();
    $request->session()->invalidate();
    $request->session()->regenerateToken();
    return redirect()->route('login')->with('success', 'Anda berhasil logout.');
}"""
    },
    {
        "filename": "07_tubes_laporan_controller.png",
        "title": "Tubes: app/Http/Controllers/LaporanController.php - Upload & Cleanup",
        "lexer": PhpLexer(),
        "code": """// Validasi & Simpan Upload Berkas pada Tugas Akhir
$request->validate([
    'lokasi'    => 'required|string|max:255',
    'deskripsi' => 'required|string',
    'foto'      => 'nullable|image|mimes:jpeg,png,jpg,gif|max:2048',
]);

$foto_path = null;
if ($request->hasFile('foto')) {
    $foto_path = $request->file('foto')->store('foto_laporan', 'public');
}

// Pembersihan Foto Fisik Saat Diperbarui (Update)
if ($request->hasFile('foto')) {
    if ($laporan->foto && Storage::disk('public')->exists($laporan->foto)) {
        Storage::disk('public')->delete($laporan->foto);
    }
    $foto_path = $request->file('foto')->store('foto_laporan', 'public');
}"""
    }
]

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--window-size=1400,1200')
driver = webdriver.Chrome(options=opts)

temp_html = os.path.join(OUTPUT_DIR, "temp_render.html")

try:
    for idx, item in enumerate(codesnap_items):
        formatter = HtmlFormatter(style='monokai', linenos=True, cssclass='source')
        highlighted = pygments.highlight(item["code"], item["lexer"], formatter)
        css = formatter.get_style_defs('.source')

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<style>
body {{
    background: transparent;
    padding: 30px;
    margin: 0;
    display: inline-block;
    font-family: 'Consolas', 'Courier New', monospace;
}}
.window {{
    background: #1e1e2e;
    border-radius: 12px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.65), 0 0 0 1px rgba(255,255,255,0.1);
    overflow: hidden;
    min-width: 720px;
    max-width: 880px;
}}
.header {{
    background: #181825;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}}
.dots {{
    display: flex;
    gap: 8px;
}}
.dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
}}
.dot-red {{ background: #ff5f56; }}
.dot-yellow {{ background: #ffbd2e; }}
.dot-green {{ background: #27c93f; }}
.title {{
    color: #cdd6f4;
    font-size: 13px;
    font-weight: 600;
    margin: 0 auto;
    letter-spacing: 0.5px;
}}
.content {{
    padding: 22px 26px;
    font-size: 13.5px;
    line-height: 1.6;
    color: #f8f8f2;
}}
{css}
.source {{ background: transparent !important; }}
.source table {{ border-spacing: 0; width: 100%; }}
.source td.linenos {{
    padding-right: 20px;
    color: #585b70;
    user-select: none;
    text-align: right;
    width: 35px;
}}
.source pre {{ margin: 0; }}
</style>
</head>
<body>
<div class='window' id='captureWindow'>
    <div class='header'>
        <div class='dots'>
            <div class='dot dot-red'></div>
            <div class='dot dot-yellow'></div>
            <div class='dot dot-green'></div>
        </div>
        <div class='title'>{item["title"]}</div>
    </div>
    <div class='content'>
        {highlighted}
    </div>
</div>
</body>
</html>"""

        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html)

        driver.get(f"file:///{temp_html.replace(os.sep, '/')}")
        elem = driver.find_element('id', 'captureWindow')
        out_path = os.path.join(OUTPUT_DIR, item["filename"])
        elem.screenshot(out_path)
        print(f"Generated CodeSnap: {item['filename']}")

finally:
    driver.quit()
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print("ALL CODESNAPS GENERATED SUCCESSFULLY.")
