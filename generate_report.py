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
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    run = h.runs[0]
    run.font.name = 'Calibri'
    if level == 1:
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 76, 129) # Deep Navy
    elif level == 2:
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(31, 78, 121)
    elif level == 3:
        run.font.size = Pt(11)
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
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(90, 90, 90)

# ==================== COVER PAGE ====================
p_top = doc.add_paragraph()
p_top.paragraph_format.space_before = Pt(15)
p_top.paragraph_format.space_after = Pt(10)
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER

r_inst = p_top.add_run("PROGRAM STUDI S1 TEKNIK INFORMATIKA / SISTEM INFORMASI\nFAKULTAS INFORMATIKA - UNIVERSITAS TELKOM\nTAHUN AKADEMIK 2026/2027\n")
r_inst.font.name = 'Calibri'
r_inst.font.size = Pt(12)
r_inst.font.bold = True
r_inst.font.color.rgb = RGBColor(50, 50, 50)

# Logo Telkom
logo_path = r"E:\Kuliah\PABW\logo_telkom.png"
if os.path.exists(logo_path):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(15)
    p_logo.paragraph_format.space_after = Pt(20)
    p_logo.add_run().add_picture(logo_path, width=Inches(2.1))

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(10)
p_title.paragraph_format.space_after = Pt(10)
r_t1 = p_title.add_run("LAPORAN PRAKTIKUM PEMROGRAMAN APLIKASI WEB\n")
r_t1.font.name = 'Calibri'
r_t1.font.size = Pt(17)
r_t1.font.bold = True
r_t1.font.color.rgb = RGBColor(15, 76, 129)

r_t2 = p_title.add_run("MODUL 7: CRUD DAN UPLOAD FILE PADA LARAVEL\n")
r_t2.font.name = 'Calibri'
r_t2.font.size = Pt(14.5)
r_t2.font.bold = True
r_t2.font.color.rgb = RGBColor(192, 57, 43)

r_t3 = p_title.add_run("(Implementasi Sistem LaporBanjir BPBD Kabupaten Bandung &\nFitur CRUD Bukti Insiden pada Tugas Akhir Smart Traffic Finder)")
r_t3.font.name = 'Calibri'
r_t3.font.size = Pt(11.5)
r_t3.font.italic = True
r_t3.font.color.rgb = RGBColor(80, 80, 80)

p_identitas = doc.add_paragraph()
p_identitas.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_identitas.paragraph_format.space_before = Pt(35)
p_identitas.paragraph_format.space_after = Pt(35)

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
    "Setelah mengikuti dan menyelesaikan seluruh materi praktikum Modul 7 ini, mahasiswa diharapkan:\n"
    "1. Memahami konsep arsitektur CRUD (Create, Read, Update, Delete) yang dipadukan dengan Resource Controller dan Resource Route pada framework Laravel secara terstruktur.\n"
    "2. Memahami alur kerja pengunggahan berkas (file upload), konfigurasi atribut form multipart/form-data, validasi tipe MIME dan batas ukuran berkas, penyimpanan berkas pada disk public (store()), serta fungsi symbolic link (php artisan storage:link).\n"
    "3. Mampu membangun sistem pengelolaan berkas menggunakan antarmuka modern, baik menggunakan Laravel Breeze maupun implementasi mandiri (manual) berbasis layout Blade dan Bootstrap 5.\n"
    "4. Menerapkan proteksi keamanan rute menggunakan Middleware Authentication (auth & guest) sehingga fungsi manipulasi data krusial hanya dapat diakses oleh pengguna atau petugas yang terverifikasi.\n"
    "5. Menguasai manajemen berkas fisik di server storage, memastikan berkas lama terhapus otomatis saat data diperbarui atau dihapus menggunakan Facade Storage::disk('public')->delete().\n"
    "6. Menerapkan fitur CRUD dan upload berkas pada studi kasus nyata aplikasi pengaduan bencana LaporBanjir BPBD Kabupaten Bandung serta integrasi fitur unggah foto bukti insiden pada project Tugas Akhir Smart Traffic Finder."
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
    ("2", "Processor & RAM", "Intel Core i7 / AMD Ryzen (Multi-core), RAM 16 GB, SSD"),
    ("3", "Web Server & DBMS", "XAMPP v3.3.0 (Apache 2.4.58 & MariaDB 10.4.32, phpMyAdmin)"),
    ("4", "Bahasa Pemrograman (Runtime)", "PHP v8.3.33 (CLI ZTS Visual C++ 2019 x64)"),
    ("5", "Dependency Manager", "Composer v2.8.x"),
    ("6", "Framework PHP", "Laravel Framework v11.x / v12.x"),
    ("7", "Frontend Framework & Assets", "Bootstrap 5.3.0 CDN, Tailwind CSS, Font Awesome 6.4.0"),
    ("8", "Code Editor & Automation", "Visual Studio Code, PowerShell Terminal, Python 3.12 (Selenium WebDriver & Pygments)"),
    ("9", "Web Browser Pengujian", "Google Chrome (Desktop & Headless)")
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

# ==================== LANGKAH-LANGKAH PRAKTIKUM (DENGAN CODESNAP) ====================
add_heading_styled(doc, "4. Langkah-Langkah Praktikum (Implementasi CodeSnap)", level=1)

doc.add_paragraph(
    "Pada bagian ini diuraikan tahapan teknis implementasi fitur CRUD dan unggah berkas (file upload) "
    "lengkap dengan potongan kode sumber yang disajikan menggunakan format visual modern bergaya CodeSnap (Dark IDE theme)."
).paragraph_format.space_after = Pt(6)

add_heading_styled(doc, "4.1 Perancangan Skema Database dan Migrasi Tabel Laporan", level=2)
doc.add_paragraph(
    "Tahap awal pengerjaan aplikasi LaporBanjir adalah menyusun skema tabel database `laporans` melalui Migration Laravel. "
    "Tabel ini memuat kolom nama pelapor, nomor telepon WhatsApp, kecamatan di Kabupaten Bandung, estimasi tinggi genangan air (cm), "
    "keterangan detail, path lokasi foto bukti di folder storage, serta status penanganan darurat (nilai bawaan: 'Menunggu')."
)

# CodeSnap 1: Migration
cs_dir = r"E:\Kuliah\PABW\praktikum7\codesnaps"
add_image_with_caption(doc, os.path.join(cs_dir, "01_migration_laporans.png"), 
                       "CodeSnap 1: File Migration create_laporans_table.php", width=Inches(5.6))

add_heading_styled(doc, "4.2 Pembuatan Model Eloquent Laporan", level=2)
doc.add_paragraph(
    "Model Eloquent `Laporan` dibuat untuk menjembatani interaksi aplikasi dengan tabel `laporans`. "
    "Properti `$fillable` dikonfigurasi untuk mengizinkan operasi *Mass Assignment* secara aman pada kolom-kolom laporan."
)
# CodeSnap 2: Model
add_image_with_caption(doc, os.path.join(cs_dir, "02_model_laporan.png"), 
                       "CodeSnap 2: Model Eloquent Laporan (app/Models/Laporan.php)", width=Inches(5.4))

add_heading_styled(doc, "4.3 Logika Upload Berkas dan Validasi Input Warga (Store Method)", level=2)
doc.add_paragraph(
    "Pada method `store()`, sistem memvalidasi kelayakan berkas gambar (wajib bertipe jpg/jpeg/png dengan batas maksimal 2048 KB) "
    "serta kelengkapan data administratif warga. Berkas yang lolos verifikasi disimpan ke folder `storage/app/public/foto_banjir` "
    "menggunakan fungsi `$file->store('foto_banjir', 'public')` yang menghasilkan hash nama unik acak."
)
# CodeSnap 3: Store Method
add_image_with_caption(doc, os.path.join(cs_dir, "03_store_laporan_upload.png"), 
                       "CodeSnap 3: Logika Validasi dan Penyimpanan Foto Berkas pada LaporanController (store)", width=Inches(5.6))

add_heading_styled(doc, "4.4 Pembersihan Berkas Fisik saat Pembaruan Data dan Penghapusan Laporan", level=2)
doc.add_paragraph(
    "Untuk mencegah terjadinya penumpukan berkas sampah fisik (*orphan files*) pada kapasitas harddisk server, "
    "metode `update()` dan `destroy()` dilengkapi logika pembersihan berkas lama secara otomatis menggunakan Facade `Storage`."
)
# CodeSnap 4: Update & Destroy Storage Cleanup
add_image_with_caption(doc, os.path.join(cs_dir, "04_update_destroy_storage.png"), 
                       "CodeSnap 4: Logika Pembersihan Berkas Lama di Storage Server (update & destroy)", width=Inches(5.6))

add_heading_styled(doc, "4.5 Konfigurasi Routing dan Proteksi Middleware Authentication", level=2)
doc.add_paragraph(
    "Sistem membedakan akses publik untuk formulir aduan masyarakat dengan panel pengelolaan laporan oleh staf BPBD. "
    "Rute aduan warga dibuka secara umum, sedangkan pengelolaan tabel laporan dan penghapusan data dikunci di balik middleware `auth`."
)
# CodeSnap 5: Routes Web
add_image_with_caption(doc, os.path.join(cs_dir, "05_routes_web.png"), 
                       "CodeSnap 5: Konfigurasi Rute Resource dan Middleware pada routes/web.php", width=Inches(5.6))

add_heading_styled(doc, "4.6 Controller Autentikasi Petugas BPBD Mandiri (Manual Auth)", level=2)
doc.add_paragraph(
    "Autentikasi staf BPBD dibangun secara mandiri menggunakan `AuthController` dengan metode login, regenerasi session, "
    "dan proteksi logout POST CSRF."
)
# CodeSnap 6: AuthController
add_image_with_caption(doc, os.path.join(cs_dir, "06_auth_controller.png"), 
                       "CodeSnap 6: Logika Autentikasi Mandiri Petugas (app/Http/Controllers/AuthController.php)", width=Inches(5.6))

add_heading_styled(doc, "4.7 Implementasi Standar Upload File pada Tugas Akhir Smart Traffic Finder", level=2)
doc.add_paragraph(
    "Pada project Tugas Akhir Smart Traffic Finder, mekanisme unggah foto bukti kemacetan/kecelakaan diperbarui dengan "
    "standar validasi Modul 7, penyimpanan disk public, dan pembersihan berkas fisik secara otomatis."
)
# CodeSnap 7: Tubes Laporan Controller
add_image_with_caption(doc, os.path.join(cs_dir, "07_tubes_laporan_controller.png"), 
                       "CodeSnap 7: Standardisasi Upload Berkas & Clean-up Storage pada Smart Traffic Finder", width=Inches(5.6))

# ==================== HASIL DAN DOKUMENTASI PROGRAM ====================
add_heading_styled(doc, "5. Hasil dan Dokumentasi Program", level=1)

doc.add_paragraph(
    "Berikut merupakan dokumentasi visual pengujian antarmuka aplikasi, pesan galat validasi, "
    "pengelolaan basis data, dan verifikasi berkas fisik pada storage server:"
)

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
    add_image_with_caption(doc, fpath, cap, width=Inches(5.5))
    p_d = doc.add_paragraph(desc)
    p_d.paragraph_format.space_before = Pt(0)
    p_d.paragraph_format.space_after = Pt(8)
    p_d.runs[0].font.name = 'Calibri'
    p_d.runs[0].font.size = Pt(9.5)

# Bukti database & storage callout
add_callout(doc, 
    "Verifikasi Penyimpanan Database & Filesystem Storage:\n"
    "1. Basis Data MySQL (db_laporbanjir, tabel 'laporans'): Menyimpan path relatif string berkas pada kolom 'foto', contoh: 'foto_banjir/bpg6JBLMW6HrXHa1vQhYgMxgvluadCgnmYtKVE7N.jpg'.\n"
    "2. Folder Fisik Server (storage/app/public/foto_banjir): Menampung file gambar biner hasil fungsi store() dengan penamaan acak unik anti-tabrakan.\n"
    "3. Pengujian Otomatis (PHPUnit/Pest Feature Test): Seluruh assertions uji coba rute dan upload berkas berstatus PASSED (100%).",
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

# ==================== LAMPIRAN GITHUB RESMI ====================
add_heading_styled(doc, "8. Lampiran Link Repositori GitHub", level=1)
p_git = doc.add_paragraph(
    "Seluruh kode sumber (source code) aplikasi LaporBanjir dan integrasi fitur CRUD file upload pada Tugas Akhir "
    "telah dikelola menggunakan Git Version Control dan dihubungkan ke akun GitHub resmi:\n"
)
p_git.paragraph_format.line_spacing = 1.15

tbl_git = doc.add_table(rows=1, cols=3)
tbl_git.alignment = WD_TABLE_ALIGNMENT.CENTER
g_hdr = tbl_git.rows[0].cells
g_hdr[0].text = "No"
g_hdr[1].text = "Nama Repositori / Proyek"
g_hdr[2].text = "Tautan Repositori GitHub Resmi"
for cell in g_hdr:
    set_cell_background(cell, "1F4E79")
    set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
    for p in cell.paragraphs:
        for r in p.runs:
            r.font.name = 'Calibri'
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

git_links = [
    ("1", "Praktikum Modul 7 (Aplikasi LaporBanjir & CRUD)", "https://github.com/HarisDawa/praktikum7-laporbanjir.git"),
    ("2", "Tugas Akhir PABW (Smart Traffic Finder)", "https://github.com/HarisDawa/PABW_TA.git")
]

for no, nama, url in git_links:
    row_cells = tbl_git.add_row().cells
    row_cells[0].text = no
    row_cells[1].text = nama
    row_cells[2].text = url
    for c_idx, cell in enumerate(row_cells):
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = 'Calibri'
                r.font.size = Pt(10)
                if c_idx == 2:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(15, 76, 129)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Save updated docx
output_docx = r"E:\Kuliah\PABW\praktikum7\Laporan_Praktikum_Modul7_Ahmad_Haris_Dawaaul_Qulub_CodeSnap.docx"
doc.save(output_docx)
print("UPDATED DOCX WITH CODESNAPS AND GITHUB LINKS GENERATED:", output_docx)
