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
