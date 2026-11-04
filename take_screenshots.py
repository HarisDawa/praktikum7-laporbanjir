import os
import time
from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

BASE_DIR = r"E:\Kuliah\PABW\praktikum7"
SS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SS_DIR, exist_ok=True)

img1_path = os.path.join(BASE_DIR, "sample_banjir_1.jpg")
img2_path = os.path.join(BASE_DIR, "sample_banjir_2.jpg")
txt_path = os.path.join(BASE_DIR, "sample_dokumen.txt")

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1280,1000")

driver = webdriver.Chrome(options=options)

def js_click(elem):
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", elem)

try:
    # 01: Form Lapor Banjir
    driver.get("http://127.0.0.1:8001/lapor")
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "01_laporbanjir_form_warga.png"))
    print("01 OK")

    # 02: Validasi Error Form Lapor
    driver.find_element(By.ID, "nama_pelapor").send_keys("Ahmad Haris Dawaa'ul Qulub")
    driver.find_element(By.ID, "no_hp").send_keys("081234567890")
    Select(driver.find_element(By.ID, "kecamatan")).select_by_value("Dayeuhkolot")
    driver.find_element(By.ID, "tinggi_air").send_keys("75")
    driver.find_element(By.ID, "lokasi").send_keys("Jl. Dayeuhkolot No. 12")
    driver.find_element(By.ID, "keterangan").send_keys("Genangan air setinggi paha menutup jalan.")
    driver.find_element(By.ID, "foto").send_keys(txt_path)
    btn_submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    js_click(btn_submit)
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "02_laporbanjir_validasi_error.png"))
    print("02 OK")

    # 03: Berhasil Lapor dengan Foto
    driver.get("http://127.0.0.1:8001/lapor")
    driver.find_element(By.ID, "nama_pelapor").send_keys("Ahmad Haris Dawaa'ul Qulub")
    driver.find_element(By.ID, "no_hp").send_keys("081234567890")
    Select(driver.find_element(By.ID, "kecamatan")).select_by_value("Dayeuhkolot")
    driver.find_element(By.ID, "tinggi_air").send_keys("80")
    driver.find_element(By.ID, "lokasi").send_keys("Jl. Raya Dayeuhkolot No. 45 RT 02/RW 04")
    driver.find_element(By.ID, "keterangan").send_keys("Akses kendaraan lumpuh total, dibutuhkan evakuasi lansia dan logistik makanan.")
    driver.find_element(By.ID, "foto").send_keys(img1_path)
    btn_submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    js_click(btn_submit)
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "03_laporbanjir_lapor_sukses.png"))
    print("03 OK")

    # 04: Akses /laporans saat belum login -> redirect login
    driver.get("http://127.0.0.1:8001/laporans")
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "04_laporbanjir_middleware_redirect.png"))
    print("04 OK")

    # 05: Form Register Petugas
    driver.get("http://127.0.0.1:8001/register")
    time.sleep(1)
    driver.find_element(By.ID, "name").send_keys("Ahmad Haris (Petugas BPBD)")
    driver.find_element(By.ID, "email").send_keys("haris@bpbd.go.id")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "password_confirmation").send_keys("password123")
    driver.save_screenshot(os.path.join(SS_DIR, "05_laporbanjir_register_petugas.png"))
    print("05 OK")

    # Submit Register
    btn_reg = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    js_click(btn_reg)
    time.sleep(1)

    # 06: Daftar Laporan Petugas
    driver.save_screenshot(os.path.join(SS_DIR, "06_laporbanjir_kelola_daftar.png"))
    print("06 OK")

    # 07: Detail Laporan Banjir
    driver.get("http://127.0.0.1:8001/laporans/1")
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "07_laporbanjir_detail.png"))
    print("07 OK")

    # 08: Form Edit Laporan (ganti foto & status)
    driver.get("http://127.0.0.1:8001/laporans/1/edit")
    time.sleep(1)
    Select(driver.find_element(By.ID, "status")).select_by_value("Diproses")
    driver.find_element(By.ID, "foto").send_keys(img2_path)
    driver.save_screenshot(os.path.join(SS_DIR, "08_laporbanjir_form_edit.png"))
    print("08 OK")

    # Submit Edit
    btn_edit = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    js_click(btn_edit)
    time.sleep(1)

    # 09: Daftar Laporan setelah diupdate
    driver.save_screenshot(os.path.join(SS_DIR, "09_laporbanjir_setelah_update.png"))
    print("09 OK")

    # 10: Detail Laporan setelah diganti foto
    driver.get("http://127.0.0.1:8001/laporans/1")
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "10_laporbanjir_detail_foto_baru.png"))
    print("10 OK")

    # --- TUBES: SMART TRAFFIC FINDER ---
    # 11: Tubes Login
    driver.get("http://127.0.0.1:8002/login")
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "11_tubes_login.png"))
    print("11 OK")

    # Try login as admin/haris on Tubes
    try:
        # Check users in db_smart_traffic / smart_traffic
        driver.find_element(By.ID, "email").send_keys("admin@gmail.com")
        driver.find_element(By.ID, "password").send_keys("admin123")
        btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        js_click(btn)
        time.sleep(1)
    except Exception as e:
        print("Tubes login form exception:", e)

    # 12: Tubes Daftar Laporan
    driver.get("http://127.0.0.1:8002/laporan")
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "12_tubes_daftar_laporan.png"))
    print("12 OK")

    # 13: Tubes Form Tambah Laporan dengan Upload Foto
    driver.get("http://127.0.0.1:8002/laporan/tambah")
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "13_tubes_form_tambah_foto.png"))
    print("13 OK")

    # 14: Tubes Detail Laporan
    driver.get("http://127.0.0.1:8002/laporan/detail/1")
    time.sleep(1)
    driver.save_screenshot(os.path.join(SS_DIR, "14_tubes_detail_laporan.png"))
    print("14 OK")

finally:
    driver.quit()
    print("ALL AUTOMATION COMPLETE.")
