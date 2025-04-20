import pandas as pd
import os


DATASET_FILE = "https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/export?format=csv&gid=743838712"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    try:
        df = pd.read_csv(DATASET_FILE)
        df.columns = [col.strip() for col in df.columns]
        df.fillna("-", inplace=True)
        return df
    except Exception as e:
        print(f"Gagal memuat data: {e}")
        exit()

def linear_search(df, column, keyword):
    try:
        results = df[df[column].astype(str).str.contains(keyword, case=False, na=False)]
        return results
    except KeyError:
        print(f"Kolom '{column}' tidak ditemukan!")
        print("Kolom tersedia:", df.columns.tolist())
        return pd.DataFrame()

def binary_search(df, column, keyword):
    try:
        df_sorted = df.sort_values(by=column, key=lambda col: col.astype(str))
        df_sorted = df_sorted.reset_index(drop=False)  
        low, high = 0, len(df_sorted) - 1
        result = []

        while low <= high:
            mid = (low + high) // 2
            value = str(df_sorted.at[mid, column]).lower()

            if keyword.lower() in value:
                i = mid
                while i >= 0 and keyword.lower() in str(df_sorted.at[i, column]).lower():
                    result.append(df_sorted.iloc[i])
                    i -= 1
                i = mid + 1
                while i < len(df_sorted) and keyword.lower() in str(df_sorted.at[i, column]).lower():
                    result.append(df_sorted.iloc[i])
                    i += 1
                break
            elif keyword.lower() < value:
                high = mid - 1
            else:
                low = mid + 1

        return pd.DataFrame(result)
    except KeyError:
        print(f"Kolom '{column}' tidak ditemukan!")
        print("Kolom tersedia:", df.columns.tolist())
        return pd.DataFrame()

def tampilkan_hasil(results, tampilkan_detail=True):
    if results.empty:
        print("Tidak ditemukan hasil yang sesuai.")
        return

    for i, row in results.iterrows():
        print("="*60)
        print(f"#{row['index'] + 1}" if 'index' in row else f"#{i + 1}")

        print(f"\nJudul Paper\t: {row.get('Judul Paper', '-')}")
        
        tahun = row.get('Tahun Terbit', '-')
        if isinstance(tahun, (float, int)):
            tahun = str(int(float(tahun)))
        print(f"\nTahun Terbit\t: {tahun}")

        print(f"\nNama Penulis\t: {row.get('Nama Penulis', '-')}")

        if tampilkan_detail:
            
            abstrak_col = [col for col in row.index if 'abstrak' in col.lower()]
            kesimpulan_col = [col for col in row.index if 'kesimpulan' in col.lower()]

            abstrak = row.get(abstrak_col[0], '-') if abstrak_col else '-'
            kesimpulan = row.get(kesimpulan_col[0], '-') if kesimpulan_col else '-'

            print("\nAbstrak\t\t:", abstrak or "-")
            print("\nKesimpulan\t:", kesimpulan or "-")

        print(f"\n  Link\t\t: {row.get('Link Paper', '-')}")
    print("="*60)

def main():
    data = load_data()

    kolom_mapping = {
        '1': 'Judul Paper',
        '2': 'Tahun Terbit',
        '3': 'Nama Penulis',
    }

    while True:
        clear_screen()
        print("=~=~ SEARCH MENU ~=~=")
        print("1. Linear Search")
        print("2. Binary Search")
        print("0. Keluar")
        metode = input("Pilih metode pencarian: ")

        if metode == '0':
            print("Keluar Program. :D")
            break

        print("\nPilih kategori:")
        print("1. Judul Paper")
        print("2. Tahun Terbit")
        print("3. Nama Penulis")
        kategori = input("Pilih: ")

        if kategori not in kolom_mapping:
            print("Kategori tidak valid.")
            input("Tekan ENTER untuk lanjut...")
            continue

        
        if kategori == '1':
            keyword = input("Masukkan judul paper: ")
        elif kategori == '2':
            keyword = input("Masukkan tahun terbit: ")
        elif kategori == '3':
            keyword = input("Masukkan nama penulis: ")
        else:
            keyword = input("Masukkan kata kunci pencarian: ")

        
        show_detail = input("Apakah ingin menampilkan abstrak dan kesimpulan? (y/n): ").strip().lower()
        tampilkan_detail = (show_detail == 'y')

        
        if metode == '1':
            hasil = linear_search(data, kolom_mapping[kategori], keyword)
        elif metode == '2':
            hasil = binary_search(data, kolom_mapping[kategori], keyword)
        else:
            print("Metode tidak valid.")
            input("Tekan ENTER untuk lanjut...")
            continue

        
        if kategori != '1':
            print(f"\n({keyword}) total : {len(hasil)}\n")

        tampilkan_hasil(hasil, tampilkan_detail)

        ulang = input("\nIngin mengulang(y/n)? ").lower()
        if ulang != 'y':
            print("Keluar Program. :D")
            break

if __name__ == "__main__":
    main()
