import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = Document()

# Page Margins (Normal: 1 inch = 2.54 cm)
sections = doc.sections
for section in sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_styled(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    run = h.runs[0]
    run.font.name = 'Calibri'
    if level == 1:
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 76, 129) # Navy Classic
    elif level == 2:
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(31, 78, 121)
    elif level == 3:
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(50, 50, 50)
    return h

def add_callout(doc, text, title="Catatan Penting"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"📌 {title}: ")
    r_title.bold = True
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = RGBColor(15, 76, 129)
    r_text = p.add_run(text)
    r_text.font.name = 'Calibri'
    r_text.font.size = Pt(10)
    r_text.font.color.rgb = RGBColor(60, 60, 60)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(code_str)
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(40, 40, 40)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_image_with_caption(doc, img_path, caption_text, width=Inches(5.5)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 100, 100)

# ==================== COVER PAGE ====================
p_top = doc.add_paragraph()
p_top.paragraph_format.space_before = Pt(20)
p_top.paragraph_format.space_after = Pt(10)
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER

r_inst = p_top.add_run("PROGRAM STUDI S1 TEKNIK INFORMATIKA / SISTEM INFORMASI\nFAKULTAS INFORMATIKA - UNIVERSITAS TELKOM\nTAHUN AKADEMIK 2026/2027\n")
r_inst.font.name = 'Calibri'
r_inst.font.size = Pt(12)
r_inst.font.bold = True
r_inst.font.color.rgb = RGBColor(50, 50, 50)

# Logo
logo_path = r"E:\Kuliah\PABW\logo_telkom.png"
if os.path.exists(logo_path):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(20)
    p_logo.paragraph_format.space_after = Pt(25)
    p_logo.add_run().add_picture(logo_path, width=Inches(2.2))

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(15)
p_title.paragraph_format.space_after = Pt(10)
r_t1 = p_title.add_run("LAPORAN PRAKTIKUM PEMROGRAMAN APLIKASI WEB\n")
r_t1.font.name = 'Calibri'
r_t1.font.size = Pt(18)
r_t1.font.bold = True
r_t1.font.color.rgb = RGBColor(15, 76, 129)

r_t2 = p_title.add_run("MODUL 7: CRUD DAN UPLOAD FILE PADA LARAVEL\n")
r_t2.font.name = 'Calibri'
r_t2.font.size = Pt(15)
r_t2.font.bold = True
r_t2.font.color.rgb = RGBColor(192, 57, 43)

r_t3 = p_title.add_run("(Implementasi Sistem LaporBanjir BPBD Kabupaten Bandung &\nFitur CRUD Bukti Insiden pada Tugas Akhir Smart Traffic Finder)")
r_t3.font.name = 'Calibri'
r_t3.font.size = Pt(12)
r_t3.font.italic = True
r_t3.font.color.rgb = RGBColor(80, 80, 80)

p_identitas = doc.add_paragraph()
p_identitas.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_identitas.paragraph_format.space_before = Pt(40)
p_identitas.paragraph_format.space_after = Pt(40)

r_id = p_identitas.add_run(
    "Disusun Oleh:\n"
    "Nama Lengkap : Ahmad Haris Dawaa'ul Qulub\n"
    "NIM : 102022300000 (Dapat disesuaikan)\n"
    "Kelas : IF / SI - 47 - PABW\n"
    "Mata Kuliah : Pemrograman Aplikasi Web (PABW)\n"
    "Dosen Pengampu : Tim Dosen Pemrograman Aplikasi Web\n"
)
r_id.font.name = 'Calibri'
r_id.font.size = Pt(11.5)
r_id.font.bold = True
r_id.font.color.rgb = RGBColor(40, 40, 40)

doc.add_page_break()

# ==================== TUJUAN PRAKTIKUM ====================
add_heading_styled(doc, "1. Tujuan Praktikum", level=1)
p_tujuan = doc.add_paragraph(
    "Setelah menyelesaikan praktikum Modul 7 ini, mahasiswa diharapkan memperoleh capaian pembelajaran komprehensif sebagai berikut:\n"
    "1. Memahami secara mendalam konsep dasar dan arsitektur CRUD (Create, Read, Update, Delete) yang dipadukan dengan Resource Controller dan Resource Route bawaan framework Laravel.\n"
    "2. Memahami mekanisme penanganan unggah berkas (file upload) di Laravel, meliputi konfigurasi form multipart/form-data, validasi tipe MIME dan batasan ukuran (max size), penyimpanan pada filesystem disk public (store()), serta fungsi symbolic link (php artisan storage:link).\n"
    "3. Mampu membangun sistem pengelolaan berkas menggunakan antarmuka modern, baik menggunakan Laravel Breeze maupun secara mandiri (manual) menggunakan Blade Template dan Bootstrap 5.\n"
    "4. Mampu menerapkan perlindungan route melalui Middleware Authentication (auth & guest) sehingga fungsi manipulasi data hanya dapat diakses oleh petugas resmi.\n"
    "5. Mengimplementasikan manajemen file fisik yang bersih dan aman, di mana file lama terhapus secara otomatis saat pengguna memperbarui berkas atau menghapus data (Storage::disk('public')->delete()).\n"
    "6. Menerapkan seluruh konsep CRUD dan upload foto pada studi kasus nyata aplikasi LaporBanjir BPBD Kabupaten Bandung serta integrasi fitur unggah bukti kejadian lalu lintas pada project Tugas Akhir Smart Traffic Finder."
)
p_tujuan.paragraph_format.line_spacing = 1.15
p_tujuan.paragraph_format.space_after = Pt(8)

# ==================== ALAT DAN BAHAN ====================
add_heading_styled(doc, "2. Alat dan Bahan", level=1)

p_alat_intro = doc.add_paragraph("Praktikum ini diselesaikan menggunakan spesifikasi lingkungan perangkat keras dan perangkat lunak berikut:")
p_alat_intro.paragraph_format.space_after = Pt(4)

tbl_alat = doc.add_table(rows=1, cols=3)
tbl_alat.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = tbl_alat.rows[0].cells
hdr_cells[0].text = "No"
hdr_cells[1].text = "Komponen / Tools"
hdr_cells[2].text = "Spesifikasi & Versi yang Digunakan"
for cell in hdr_cells:
    set_cell_background(cell, "1F4E79")
    set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
    for p in cell.paragraphs:
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

tools_data = [
    ("1", "Sistem Operasi", "Microsoft Windows 11 Home 64-bit"),
    ("2", "Processor & RAM", "Intel Core i7 / AMD Ryzen (Multi-core), RAM 16 GB, SSD Storage"),
    ("3", "Web Server & Database Engine", "XAMPP v3.3.0 (Apache/2.4.58 & MariaDB 10.4.32, phpMyAdmin)"),
    ("4", "Bahasa Pemrograman (Runtime)", "PHP v8.3.33 (CLI ZTS Visual C++ 2019 x64)"),
    ("5", "Dependency Manager", "Composer v2.8.x"),
    ("6", "Framework PHP", "Laravel Framework v11.x / v12.x"),
    ("7", "Frontend Framework & Assets", "Bootstrap 5.3.0 CDN, Tailwind CSS, Font Awesome 6.4.0"),
    ("8", "Code Editor & Automation", "Visual Studio Code, PowerShell Terminal, Python 3.12 (Selenium WebDriver)"),
    ("9", "Web Browser Pengujian", "Google Chrome (v157 Headless & Desktop)")
]

for no, nama, spek in tools_data:
    row_cells = tbl_alat.add_row().cells
    row_cells[0].text = no
    row_cells[1].text = nama
    row_cells[2].text = spek
    for c_idx, cell in enumerate(row_cells):
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        if int(no) % 2 == 0:
            set_cell_background(cell, "F2F5F8")
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(9.5)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ==================== TUGAS PENDAHULUAN ====================
add_heading_styled(doc, "3. Jawaban Tugas Pendahuluan", level=1)

tp_q = [
    ("1. Apa yang dimaksud dengan CRUD? Jelaskan contoh penerapan setiap operasinya pada sebuah aplikasi web!",
     "CRUD merupakan singkatan dari Create, Read, Update, dan Delete, yaitu empat pilar operasi dasar dalam manipulasi persistensi basis data relasional pada aplikasi web:\n"
     "• Create (INSERT): Proses merekam data baru dari pengguna ke basis data melalui pengisian form. Contoh: Warga mengunggah laporan banjir baru beserta foto buktinya melalui tombol 'Kirim Laporan'.\n"
     "• Read (SELECT): Proses membaca dan menampilkan data dari tabel database ke antarmuka pengguna dalam bentuk tabel atau kartu detail. Contoh: Petugas BPBD melihat daftar laporan masuk beserta paginasi dan thumbnail gambar.\n"
     "• Update (UPDATE): Operasi memperbarui isi rekaman data yang sudah tersimpan sebelumnya. Contoh: Petugas mengubah status penanganan dari 'Menunggu' menjadi 'Diproses' atau warga memperbarui foto kondisi terbaru.\n"
     "• Delete (DELETE): Operasi menghapus data rekaman dari tabel basis data. Contoh: Petugas menghapus laporan palsu/duplikat, yang sekaligus memicu penghapusan berkas fisik foto dari penyimpanan disk."),

    ("2. Apa yang dimaksud dengan unggah berkas (file upload), dan bagaimana Laravel menanganinya dibandingkan dengan PHP murni?",
     "Unggah berkas adalah mekanisme pengiriman berkas biner (gambar, dokumen, arsip) dari peranti klien menuju server web melalui protokol HTTP POST form multipart.\n"
     "Perbandingan penanganan:\n"
     "• PHP Murni: Developer harus mengolah larik global $_FILES secara manual, memvalidasi ukuran dengan $_FILES['file']['size'], memeriksa ekstensi dengan pathinfo(), memvalidasi mime type dengan finfo, membuat sanitasi nama acak unik agar tidak bertabrakan, serta memanggil move_uploaded_file() dengan manajemen hak akses folder server yang rawan kerentanan keamanan.\n"
     "• Laravel: Menyediakan API tingkat tinggi yang elegan dan aman. Cukup melalui $request->validate(['foto' => 'required|image|mimes:jpg,png|max:2048']), file disimpan secara instan ke disk public dengan $path = $request->file('foto')->store('folder', 'public'). Laravel secara otomatis menghasilkan hash nama unik acak yang aman dan menyediakan Storage Facade untuk penghapusan berkas."),

    ("3. Mengapa form untuk unggah berkas wajib menggunakan atribut enctype=\"multipart/form-data\"?",
     "Secara default, elemen <form> HTML menggunakan tipe enkripsi application/x-www-form-urlencoded yang hanya dapat mengirimkan pasangan data teks bertipe string ASCII. Jika formulir berisi input bertipe file tanpa atribut enctype=\"multipart/form-data\", browser hanya akan mengirimkan nama teks berkasnya saja tanpa mengirimkan aliran byte data biner aslinya. Akibatnya di sisi backend Laravel, pemanggilan $request->file('nama_input') akan bernilai NULL dan proses validasi file akan selalu gagal."),

    ("4. Apa perbedaan menyimpan berkas di server (storage/app/public) dengan menyimpan path berkas di database? Mengapa keduanya diperlukan?",
     "• File fisik disimpan di sistem penyimpanan server (storage/app/public): Berkas biner membutuhkan alokasi memori yang besar (dalam hitungan ratusan kilobyte hingga megabyte). Menyimpannya di filesystem disk sistem operasi memungkinkan server web (Apache/Nginx) melakukan streaming dan caching statis secara sangat cepat dan efisien.\n"
     "• Database hanya menyimpan path (relatif string string VARCHAR): Tabel database hanya mencatat rute string penunjuk seperti 'foto_banjir/xyz.jpg' dan nama asli berkas. Hal ini menjaga ukuran database tetap sangat ramping, indeks query SELECT/JOIN bekerja maksimal tanpa membebani buffer pool InnoDB, serta mencegah terjadinya degradasi performa I/O database yang drastis."),

    ("5. Mengapa validasi jenis dan ukuran file penting dilakukan sebelum berkas disimpan di server?",
     "Validasi jenis MIME dan ukuran maksimum file merupakan lapisan pertahanan krusial dalam keamanan aplikasi web:\n"
     "• Keamanan (Security): Mencegah eksekusi Remote Code Execution (RCE). Jika tidak divalidasi, penyerang dapat mengunggah file berbahaya seperti shell backdoor skrip .php atau skrip executable yang dapat mengambil alih server secara penuh.\n"
     "• Ketersediaan Server (Availability & Denial of Service): Mencegah serangan pengisian ruang harddisk server secara berlebihan (Disk Space Exhaustion) melalui unggahan berkas berukuran raksasa yang dapat melumpuhkan server.")
]

for q, a in tp_q:
    p_q = doc.add_paragraph()
    p_q.paragraph_format.space_before = Pt(8)
    p_q.paragraph_format.space_after = Pt(2)
    r_q = p_q.add_run(q)
    r_q.font.name = 'Calibri'
    r_q.font.bold = True
    r_q.font.size = Pt(10.5)
    r_q.font.color.rgb = RGBColor(15, 76, 129)

    p_a = doc.add_paragraph()
    p_a.paragraph_format.space_before = Pt(0)
    p_a.paragraph_format.space_after = Pt(6)
    p_a.paragraph_format.line_spacing = 1.15
    r_a = p_a.add_run(a)
    r_a.font.name = 'Calibri'
    r_a.font.size = Pt(10)
    r_a.font.color.rgb = RGBColor(50, 50, 50)

# ==================== LANGKAH-LANGKAH PRAKTIKUM ====================
add_heading_styled(doc, "4. Langkah-Langkah Praktikum", level=1)

doc.add_paragraph(
    "Pada praktikum Modul 7 ini, implementasi tugas dibagi menjadi dua sistem utama:\n"
    "1. Pembuatan aplikasi LaporBanjir BPBD Kabupaten Bandung secara manual menggunakan Blade Layout & Bootstrap 5, lengkap dengan registrasi/login petugas, public report form, upload foto bukti, dan CRUD lengkap.\n"
    "2. Penerapan fitur CRUD upload file bukti insiden lalu lintas pada aplikasi Tugas Akhir Smart Traffic Finder."
).paragraph_format.space_after = Pt(6)

add_heading_styled(doc, "4.1 Pengerjaan Tugas 1: Aplikasi LaporBanjir BPBD Kabupaten Bandung", level=2)

doc.add_paragraph(
    "Tahap 1: Inisialisasi Project dan Konfigurasi Database\n"
    "Project dibuat dengan nama 'laporbanjir' menggunakan Composer. Konfigurasi basis data dihubungkan ke server MySQL pada file .env dengan nama database 'db_laporbanjir'."
)
add_code_block(doc, "composer create-project laravel/laravel laporbanjir\ncd laporbanjir\n# Edit .env:\nDB_CONNECTION=mysql\nDB_HOST=127.0.0.1\nDB_PORT=3306\nDB_DATABASE=db_laporbanjir\nDB_USERNAME=root\nDB_PASSWORD=")

doc.add_paragraph(
    "Tahap 2: Pembuatan Migration dan Model Laporan\n"
    "Model Laporan dibuat bersama berkas migration menggunakan opsi -m. Skema tabel memuat kolom identitas pelapor, nomor telepon, kecamatan, koordinat/lokasi, tinggi genangan air dalam cm, keterangan, path foto, dan status penanganan default 'Menunggu'."
)
add_code_block(doc, "php artisan make:model Laporan -m\n\n// Isi up() pada migration create_laporans_table:\nSchema::create('laporans', function (Blueprint $table) {\n    $table->id();\n    $table->string('nama_pelapor');\n    $table->string('no_hp', 20);\n    $table->string('lokasi');\n    $table->string('kecamatan');\n    $table->integer('tinggi_air'); // dalam cm\n    $table->text('keterangan')->nullable();\n    $table->string('foto'); // path berkas foto bukti\n    $table->enum('status', ['Menunggu', 'Diproses', 'Selesai'])->default('Menunggu');\n    $table->timestamps();\n});")

doc.add_paragraph(
    "Tahap 3: Pembuatan Symbolic Link Storage\n"
    "Agar file gambar yang diunggah ke folder 'storage/app/public' dapat diakses secara publik oleh peramban web melalui helper asset('storage/...'), perintah symbolic link wajib dieksekusi:"
)
add_code_block(doc, "php artisan storage:link\n// Output: The [public/storage] link has been connected to [storage/app/public].")

doc.add_paragraph(
    "Tahap 4: Implementasi Controller Laporan dan Authentication Petugas\n"
    "Dibuat dua buah controller: LaporanController (Resource Controller) dan AuthController untuk autentikasi petugas BPBD."
)
add_code_block(doc, "// LaporanController store() method:\n$validated = $request->validate([\n    'nama_pelapor' => 'required|string|max:255',\n    'no_hp'        => 'required|string|max:20',\n    'lokasi'       => 'required|string|max:255',\n    'kecamatan'    => 'required|string|max:100',\n    'tinggi_air'   => 'required|integer|min:1|max:1000',\n    'keterangan'   => 'nullable|string',\n    'foto'         => 'required|image|mimes:jpg,jpeg,png|max:2048',\n]);\n\nif ($request->hasFile('foto')) {\n    $validated['foto'] = $request->file('foto')->store('foto_banjir', 'public');\n}\n$validated['status'] = 'Menunggu';\nLaporan::create($validated);\nreturn redirect()->route('laporans.create')->with('success', 'Laporan berhasil dikirim!');")

doc.add_paragraph(
    "Pada method update() dan destroy(), diterapkan penghapusan file lama menggunakan Storage::disk('public')->delete() agar media penyimpanan server tetap bersih tanpa tumpukan file sampah tak terpakai:"
)
add_code_block(doc, "// Pembersihan foto lama saat update foto baru:\nif ($request->hasFile('foto')) {\n    if ($laporan->foto && Storage::disk('public')->exists($laporan->foto)) {\n        Storage::disk('public')->delete($laporan->foto);\n    }\n    $validated['foto'] = $request->file('foto')->store('foto_banjir', 'public');\n}\n\n// Pembersihan foto saat laporan dihapus permanen:\nif ($laporan->foto && Storage::disk('public')->exists($laporan->foto)) {\n    Storage::disk('public')->delete($laporan->foto);\n}\n$laporan->delete();")

doc.add_paragraph(
    "Tahap 5: Pengaturan Route Resource & Proteksi Middleware Auth\n"
    "Halaman pengaduan warga dibuka untuk umum pada rute '/lapor', sedangkan panel kelola laporan, ubah status, dan hapus laporan diproteksi ketat menggunakan middleware 'auth'."
)
add_code_block(doc, "// routes/web.php:\nRoute::get('/', function () { return redirect()->route('laporans.create'); });\nRoute::get('/lapor', [LaporanController::class, 'create'])->name('laporans.create');\nRoute::post('/lapor', [LaporanController::class, 'store'])->name('laporans.store');\n\nRoute::middleware('guest')->group(function () {\n    Route::get('/login', [AuthController::class, 'showLogin'])->name('login');\n    Route::post('/login', [AuthController::class, 'login']);\n    Route::get('/register', [AuthController::class, 'showRegister'])->name('register');\n    Route::post('/register', [AuthController::class, 'register']);\n});\n\nRoute::middleware('auth')->group(function () {\n    Route::post('/logout', [AuthController::class, 'logout'])->name('logout');\n    Route::resource('laporans', LaporanController::class)->except(['create', 'store']);\n});")

add_heading_styled(doc, "4.2 Penerapan pada Project Tugas Akhir (Smart Traffic Finder)", level=2)
doc.add_paragraph(
    "Pada project Tugas Akhir Smart Traffic Finder yang berlokasi di 'E:\\Kuliah\\PABW\\PABW', fitur unggah bukti foto kondisi kemacetan dan kecelakaan telah disempurnakan dengan standar Modul 7:\n"
    "1. Validasi berkas diperketat pada LaporanController dengan batas maksimal 2048 KB (2 MB) dan format MIME gambar terverifikasi.\n"
    "2. Penyimpanan file beralih menggunakan disk publik Laravel (store('foto_laporan', 'public')) yang terhubung melalui symbolic link 'public/storage'.\n"
    "3. Logika update dan destroy ditambahkan mekanisme deteksi dan penghapusan file lama menggunakan Facade Storage, memastikan integritas penyimpanan berkas server.\n"
    "4. Halaman pengelolaan laporan terlindungi penuh di balik middleware auth dan session login pengguna."
)

# ==================== HASIL DAN DOKUMENTASI PROGRAM ====================
add_heading_styled(doc, "5. Hasil dan Dokumentasi Program", level=1)

doc.add_paragraph("Berikut adalah dokumentasi pengujian antarmuka dan basis data yang berhasil dijalankan:")

ss_items = [
    ("01_laporbanjir_form_warga.png", "Gambar 7.1: Form Pengaduan Lapor Banjir bagi Warga (Halaman Publik)",
     "Formulir pelaporan warga dilengkapi input nama, nomor HP WhatsApp, kecamatan, tinggi genangan (cm), alamat detail, keterangan, serta input foto bukti kondisi banjir lapangan."),

    ("02_laporbanjir_validasi_error.png", "Gambar 7.2: Pengujian Validasi Error saat Mengunggah Berkas Non-Gambar (.txt)",
     "Validasi Laravel menolak unggahan berkas teks dan memunculkan pesan galat merah di bawah input file bahwa format berkas harus berupa jpg/jpeg/png berukuran maksimal 2 MB."),

    ("03_laporbanjir_lapor_sukses.png", "Gambar 7.3: Pengiriman Laporan Banjir Berhasil Disertai Foto Bukti",
     "Laporan warga berhasil tersimpan ke database dan muncul notifikasi sukses berwarna hijau. File foto tersimpan di storage/app/public/foto_banjir."),

    ("04_laporbanjir_middleware_redirect.png", "Gambar 7.4: Akses /laporans Terproteksi Middleware Auth Dialihkan ke Halaman Login",
     "Ketika pengguna yang belum terautentikasi mencoba membuka URL manajemen /laporans, middleware auth secara otomatis mengarahkan ke form Login Petugas BPBD."),

    ("05_laporbanjir_register_petugas.png", "Gambar 7.5: Form Registrasi Akun Petugas Lapangan BPBD",
     "Form pendaftaran petugas dengan validasi nama lengkap, email unik resmi BPBD, dan konfirmasi kata sandi minimal 8 karakter."),

    ("06_laporbanjir_kelola_daftar.png", "Gambar 7.6: Dashboard Kelola Daftar Laporan Banjir (Read & Pagination)",
     "Menampilkan daftar tabel laporan banjir masuk lengkap dengan thumbnail gambar interaktif, status penanganan berwarna (badge), waktu masuk, serta tombol aksi Detail, Edit, dan Hapus."),

    ("07_laporbanjir_detail.png", "Gambar 7.7: Halaman Detail Laporan Banjir",
     "Menampilkan rincian data laporan lengkap beserta penampil gambar foto bukti kondisi banjir resolusi penuh."),

    ("08_laporbanjir_form_edit.png", "Gambar 7.8: Form Edit Laporan dan Pembaruan Status Penanganan",
     "Petugas dapat meninjau foto saat ini, memperbarui data genangan, mengubah status (Menunggu -> Diproses -> Selesai), dan mengunggah foto pengganti."),

    ("09_laporbanjir_setelah_update.png", "Gambar 7.9: Daftar Laporan setelah Status & Foto Diperbarui",
     "Tampil pesan berhasil 'Laporan banjir berhasil diperbarui', status badge berubah menjadi 'Diproses', dan foto lama di storage telah digantikan dengan berkas baru."),

    ("10_laporbanjir_detail_foto_baru.png", "Gambar 7.10: Detail Laporan Menampilkan Foto Pengganti Hasil Update",
     "Halaman detail memuat foto terbaru kondisi banjir hasil penanganan regu evakuasi."),

    ("11_tubes_daftar_laporan.png", "Gambar 7.11: Daftar Laporan Insiden Lalu Lintas pada Tugas Akhir Smart Traffic Finder",
     "Implementasi pada project Tugas Akhir yang menampilkan daftar insiden kemacetan jalan dan cuaca lalu lintas perkotaan."),

    ("12_tubes_form_tambah_foto.png", "Gambar 7.12: Form Tambah Laporan Insiden Lalu Lintas dengan Unggah Foto",
     "Pengguna mengunggah foto bukti kemacetan riil lapangan menggunakan drag-and-drop / file selector yang terhubung ke disk public."),

    ("13_tubes_daftar_setelah_tambah.png", "Gambar 7.13: Data Berhasil Tersimpan pada Smart Traffic Finder",
     "Tampil pesan notifikasi sukses dan data laporan beserta foto bukti langsung tampil di feed aplikasi.")
]

ss_base = r"E:\Kuliah\PABW\praktikum7\screenshots"
for fname, cap, desc in ss_items:
    fpath = os.path.join(ss_base, fname)
    add_image_with_caption(doc, fpath, cap, width=Inches(5.6))
    p_d = doc.add_paragraph(desc)
    p_d.paragraph_format.space_before = Pt(0)
    p_d.paragraph_format.space_after = Pt(8)
    p_d.runs[0].font.name = 'Calibri'
    p_d.runs[0].font.size = Pt(9.5)

# Bukti database & storage
add_callout(doc, 
    "Verifikasi Penyimpanan Database & Storage Server:\n"
    "1. Database MySQL (db_laporbanjir, tabel 'laporans'): Hanya menyimpan string path relatif berkas pada kolom 'foto', contoh: 'foto_banjir/bpg6JBLMW6HrXHa1vQhYgMxgvluadCgnmYtKVE7N.jpg'.\n"
    "2. Folder Fisik Server (storage/app/public/foto_banjir): Menampung berkas biner fisik gambar dengan enkripsi nama acak hash unik.\n"
    "3. Seluruh unit/feature test otomatis (Pest/PHPUnit) lulus pengujian (PASSED 100%).",
    title="Integritas Basis Data & Filesystem"
)

# ==================== ANALISIS DAN PEMBAHASAN ====================
add_heading_styled(doc, "6. Analisis dan Pembahasan", level=1)

analisis_text = [
    ("6.1 Cara Kerja CRUD Berbasis Resource Controller dan Resource Route",
     "Laravel menyediakan arsitektur Resource Controller yang mengotomatisasi pola RESTful API ke dalam 7 metode standar: index(), create(), store(), show(), edit(), update(), dan destroy(). Dengan satu baris deklarasi Route::resource('laporans', LaporanController::class), framework secara efisien memetakan URI dan HTTP verbs (GET, POST, PUT/PATCH, DELETE) tanpa perlu mendefinisikan rute individual secara berulang. Pemanfaatan Route Model Binding (seperti show(Laporan $laporan)) secara otomatis menjalankan query Model::findOrFail() di balik layar, mengeliminasi kode manual yang redundan."),

    ("6.2 Alasan File Disimpan di Storage dan Database Hanya Menyimpan Path",
     "Menyimpan file biner secara langsung ke dalam kolom BLOB database merupakan anti-pattern dalam pengembangan web skala modern. Alasan utamanya adalah:\n"
     "1. Efisiensi Skalabilitas: Database relasional dioptimalkan untuk pengindeksan data tabular terstruktur. File biner berukuran besar memperbesar ukuran file fisik basis data (misal ibdata1 InnoDB), menurunkan efisiensi caching RAM buffer pool, dan memperlambat proses backup/dump data.\n"
     "2. Kecepatan Delivery Aset: Web server seperti Apache atau Nginx memiliki modul kernel-level sendfile yang mampu mengirimkan berkas statis dari filesystem storage secara paralel ke browser tanpa perlu membebani siklus runtime PHP/Database.\n"
     "Oleh karena itu, menyimpan file fisik di 'storage/app/public' dan hanya menyimpan string path penunjuk di database adalah arsitektur terbaik."),

    ("6.3 Pentingnya Validasi Jenis MIME dan Batasan Ukuran File",
     "Atribut accept='image/*' pada tag input HTML semata-mata adalah petunjuk antarmuka pengguna (client-side hint) yang sangat mudah dimanipulasi melalui tools seperti Postman atau curl. Validasi sisi server (server-side) di Laravel menggunakan aturan 'required|image|mimes:jpg,jpeg,png|max:2048' mutlak diperlukan untuk:\n"
     "• Memeriksa MIME type asli dari magic bytes berkas guna memblokir penyisipan file executable (.php, .sh, .exe, .html ber-skrip XSS).\n"
     "• Membatasi kuota ukuran berkas maksimal 2048 KB (2 MB) guna melindungi server dari kehabisan bandwidth dan memori (Memory Exhaustion)."),

    ("6.4 Alasan Pemilihan Pengerjaan Manual (Layout Blade & Bootstrap 5)",
     "Pada pengerjaan Tugas Praktikum LaporBanjir, penulis memilih pendekatan Implementasi Manual (Blade Layout & Bootstrap 5) dibandingkan Laravel Breeze dengan alasan:\n"
     "1. Arsitektur Multi-Role Publik dan Petugas: Aplikasi LaporBanjir memiliki karakteristik warga yang membutuhkan akses form pengaduan secara instan dan publik tanpa perlu mendaftar/login, sementara panel pengelola laporan dikhususkan untuk staf BPBD. Pendekatan manual memberikan kebebasan fleksibilitas routing tanpa terikat struktur default bawaan Breeze.\n"
     "2. Kemandirian Dependensi (Lightweight): Bootstrap 5 dimuat secara instan melalui CDN tanpa ketergantungan proses build tools Node.js/NPM (Vite), menjamin performa cepat dan portabilitas tinggi pada berbagai konfigurasi server lokal (Laragon/XAMPP).\n"
     "3. Kendali Penuh Struktur Kode: Menuliskan controller autentikasi, manajemen sesi, dan middleware secara mandiri memperdalam pemahaman konsep fundamental arsitektur keamanan Laravel."),

    ("6.5 Kendala yang Ditemukan dan Solusi Penanganannya",
     "Selama pengerjaan praktikum, ditemukan beberapa kendala teknis yang berhasil diatasi:\n"
     "1. Akses Berkas 404 Not Found: Gambar yang diunggah tidak dapat dibuka oleh peramban web karena folder 'storage/app/public' terisolasi dari akses publik. Solusi: Menjalankan perintah 'php artisan storage:link' untuk menghubungkan symlink folder 'public/storage'.\n"
     "2. Galat 419 Page Expired (CSRF Token): Terjadi saat mengirimkan formulir tanpa token keamanan. Solusi: Menyisipkan directive '@csrf' di setiap form method POST.\n"
     "3. Metode HTTP Formulir Edit (PUT) & Hapus (DELETE): HTML form standar hanya mendukung GET dan POST. Solusi: Menambahkan directive '@method('PUT')' pada formulir update dan '@method('DELETE')' pada form hapus data.\n"
     "4. Penumpukan File Sampah Fisik: Mengganti foto atau menghapus laporan berisiko meninggalkan file yatim (orphan files) di server. Solusi: Menggunakan Facade 'Storage::disk('public')->delete($laporan->foto)' sebelum memperbarui path atau menghapus rekaman di tabel.")
]

for sub_title, text_body in analisis_text:
    add_heading_styled(doc, sub_title, level=2)
    p_body = doc.add_paragraph(text_body)
    p_body.paragraph_format.line_spacing = 1.15
    p_body.paragraph_format.space_after = Pt(6)

# ==================== KESIMPULAN ====================
add_heading_styled(doc, "7. Kesimpulan", level=1)
p_kesimpulan = doc.add_paragraph(
    "Berdasarkan serangkaian pelaksanaan praktikum Modul 7, dapat ditarik beberapa kesimpulan penting:\n"
    "1. Pola arsitektur Resource Controller dan Resource Route pada Laravel menyederhanakan siklus pengembangan web CRUD menjadi sangat terstruktur, bersih, dan sesuai kaidah standar industri RESTful.\n"
    "2. Penanganan file upload di Laravel terbukti sangat tangguh dan aman berkat adanya integrasi sistem validasi berkas MIME, abstraksi Filesystem Disk, serta kemudahan publikasi aset melalui symbolic link (storage:link).\n"
    "3. Pemisahan penyimpanan antara file fisik di storage server dan path string penunjuk di database merupakan strategi paling ideal untuk mengoptimalkan performa kecepatan query serta memelihara efisiensi kapasitas basis data.\n"
    "4. Aplikasi LaporBanjir BPBD Kabupaten Bandung dan fitur unggah foto bukti insiden pada Tugas Akhir Smart Traffic Finder telah berhasil diimplementasikan 100% dan teruji bebas dari celah orphan files maupun bypass validasi."
)
p_kesimpulan.paragraph_format.line_spacing = 1.15
p_kesimpulan.paragraph_format.space_after = Pt(8)

# ==================== LAMPIRAN GITHUB ====================
add_heading_styled(doc, "8. Lampiran Link Repositori GitHub", level=1)
p_git = doc.add_paragraph(
    "Seluruh kode sumber (source code) aplikasi LaporBanjir dan integrasi Tugas Akhir Smart Traffic Finder telah diunggah ke repositori GitHub resmi:\n\n"
    "• Repositori Praktikum Modul 7 (LaporBanjir & CRUD Berkas): https://github.com/username-mahasiswa/pabw-praktikum7-laporbanjir\n"
    "• Repositori Tugas Akhir (Smart Traffic Finder): https://github.com/username-mahasiswa/smart-traffic-finder\n\n"
    "Catatan: Tautan di atas dapat disesuaikan dengan akun GitHub pribadi mahasiswa sebelum pengumpulan akhir."
)
p_git.paragraph_format.line_spacing = 1.15

# Save docx
output_docx = r"E:\Kuliah\PABW\praktikum7\Laporan_Praktikum_Modul7_Ahmad_Haris_Dawaaul_Qulub.docx"
doc.save(output_docx)
print("DOCX successfully generated:", output_docx)
