import os
import pandas as pd
import qrcode
import webbrowser
from datetime import datetime
import subprocess

DATA_FILE = 'inventaris.csv'
QR_FOLDER = 'qrcodes'
os.makedirs(QR_FOLDER, exist_ok=True)

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            'ID', 'Nama Barang', 'Kode Inventaris',
            'Tanggal Pembelian', 'Lokasi', 'Detail',
            'QR Code Path', 'Terakhir Update'
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'Update inventaris'], check=False)
    subprocess.run(['git', 'push'], check=False)

def generate_qr(item_data):
    qr_data = f"""
    INVENTARIS DATA
    ID: {item_data['ID']}
    Nama: {item_data['Nama Barang']}
    Kode: {item_data['Kode Inventaris']}
    Tanggal Beli: {item_data['Tanggal Pembelian']}
    Lokasi: {item_data['Lokasi']}
    Detail: {item_data['Detail']}
    Update: {item_data['Terakhir Update']}
    """

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=4
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = f"{QR_FOLDER}/{item_data['Kode Inventaris']}.png"
    img.save(qr_path)
    return qr_path

def add_item():
    df = load_data()
    item_data = {
        'ID': len(df),
        'Nama Barang': input("Nama Barang: "),
        'Kode Inventaris': input("Kode Inventaris: "),
        'Tanggal Pembelian': input("Tanggal Pembelian (YYYY-MM-DD): "),
        'Lokasi': input("Lokasi: "),
        'Detail': input("Detail Spesifikasi: "),
        'Terakhir Update': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    qr_path = generate_qr(item_data)
    item_data['QR Code Path'] = qr_path
    df = df.append(item_data, ignore_index=True)
    save_data(df)

    print(f"✔️ Data berhasil ditambahkan! QR: {qr_path}")
    webbrowser.open(qr_path)

def view_items():
    df = load_data()
    if df.empty:
        print("📂 Inventaris masih kosong.")
    else:
        print(df[['ID', 'Nama Barang', 'Kode Inventaris', 'Lokasi']])

def main_menu():
    while True:
        print("\n=== QR INVENTARIS (GitHub Sync) ===")
        print("1. Tambah Barang")
        print("2. Lihat Inventaris")
        print("3. Keluar")
        choice = input("Pilih menu: ")

        if choice == '1':
            add_item()
        elif choice == '2':
            view_items()
        elif choice == '3':
            print("Selesai.")
            break
        else:
            print("Pilihan tidak valid!")

def edit_item():
    df = load_data()
    if df.empty:
        print("📂 Tidak ada data untuk diedit.")
        return

    view_items()
    try:
        item_id = int(input("Masukkan ID yang ingin diedit: "))
        if item_id not in df['ID'].values:
            print("❌ ID tidak ditemukan.")
            return

        item_index = df[df['ID'] == item_id].index[0]
        item = df.loc[item_index]

        print("\nData saat ini:")
        for i, col in enumerate(['Nama Barang', 'Kode Inventaris', 'Tanggal Pembelian', 'Lokasi', 'Detail'], start=1):
            print(f"{i}. {col}: {item[col]}")

        field_num = int(input("Pilih nomor field yang ingin diedit (1-5): "))
        if field_num not in range(1, 6):
            print("❌ Pilihan tidak valid.")
            return

        fields = ['Nama Barang', 'Kode Inventaris', 'Tanggal Pembelian', 'Lokasi', 'Detail']
        field = fields[field_num - 1]

        new_value = input(f"Masukkan nilai baru untuk {field}: ")
        df.at[item_index, field] = new_value
        df.at[item_index, 'Terakhir Update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Hapus QR lama kalau kode diubah
        if field == 'Kode Inventaris':
            old_path = df.at[item_index, 'QR Code Path']
            if os.path.exists(old_path):
                os.remove(old_path)

        # Buat QR baru
        new_qr_path = generate_qr(df.loc[item_index])
        df.at[item_index, 'QR Code Path'] = new_qr_path

        save_data(df)
        print("✔️ Data berhasil diperbarui!")

    except ValueError:
        print("❌ Input tidak valid.")
        
if __name__ == '__main__':
    main_menu()
def main_menu():
    while True:
        print("\n=== QR INVENTARIS (GitHub Sync) ===")
        print("1. Tambah Barang")
        print("2. Lihat Inventaris")
        print("3. Edit Barang")
        print("4. Keluar")
        choice = input("Pilih menu: ")

        if choice == '1':
            add_item()
        elif choice == '2':
            view_items()
        elif choice == '3':
            edit_item()
        elif choice == '4':
            print("Selesai.")
            break
        else:
            print("Pilihan tidak valid!")
