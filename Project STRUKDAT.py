import heapq
import itertools

# membuat fungsi graph
class Graph:
    def __init__(self):
        self.graph = {}

    def tambah_kota(self, nama_kota):
        # """Menambahkan kota (vertex) jika belum ada"""
        if nama_kota not in self.graph:
            self.graph[nama_kota] = []

    def tambah_jalan(self, kota1, kota2, jarak):
        # """Menambahkan jalan (edge) dua arah antara dua kota"""
        if kota1 not in self.graph:
            self.tambah_kota(kota1)
        if kota2 not in self.graph:
            self.tambah_kota(kota2)

        # Cek apakah edge sudah ada agar tidak duplikat
        if (kota2, jarak) not in self.graph[kota1]:
            self.graph[kota1].append((kota2, jarak))
        if (kota1, jarak) not in self.graph[kota2]:
            self.graph[kota2].append((kota1, jarak))

    def masuk_data_awal(self, data_awal):
        # """Mengisi graph dari data adjacency list"""
        for kota in data_awal:
            for tujuan, jarak in data_awal[kota]:
                self.tambah_jalan(kota, tujuan, jarak)
    
    # Memberikan daftar nama kota yang sudah tersimpan dalam graph, agar Bisa ditampilkan ke pengguna (misalnya dalam menu interaktif)
    def daftar_kota(self):
        return list(self.graph.keys())
    
    # Algoritma Djikistra
    def dijkstra(self, asal, tujuan):
        jarak = {kota: float('inf') for kota in self.graph}
        jarak[asal] = 0
        prioritas = [(0, asal, [])]

        while prioritas:
            dist, sekarang, path = heapq.heappop(prioritas)
            if sekarang == tujuan:
                return path + [sekarang], dist

            for tetangga, bobot in self.graph[sekarang]:
                total = dist + bobot
                if total < jarak[tetangga]:
                    jarak[tetangga] = total
                    heapq.heappush(prioritas, (total, tetangga, path + [sekarang]))
        return None, float('inf')
    
    # Algoritma TSP Brute-Force
    def tsp_brute_force(self, kota_awal):
        kota_lain = [k for k in self.graph if k != kota_awal]
        rute_terbaik = None
        jarak_terpendek = float('inf')

        for perm in itertools.permutations(kota_lain):
            total_jarak = 0
            rute = [kota_awal] + list(perm)
            valid = True
            for i in range(len(rute) - 1):
                nexts = dict(self.graph[rute[i]])
                if rute[i+1] not in nexts:
                    valid = False
                    break
                total_jarak += nexts[rute[i+1]]
            if valid and total_jarak < jarak_terpendek:
                jarak_terpendek = total_jarak
                rute_terbaik = rute

        return rute_terbaik, jarak_terpendek
    

# menyusun graph dan menyimpannya dalam adjacency list
data_graph = {
    'Bojonegoro': [('Ngawi', 50), ('Nganjuk', 70), ('Malang', 90),('Lamongan', 45), ('Mojokerto', 70), ('Gresik', 55)],
    'Ngawi': [('Bojonegoro', 50), ('Nganjuk', 40), ('Lamongan', 60), ('Malang', 100), ('Gresik', 75)],
    'Nganjuk': [('Ngawi', 40), ('Bojonegoro', 70), ('Lamongan', 58), ('Mojokerto', 65), ('Pasuruan', 65), ('Malang', 75)],
    'Lamongan': [('Bojonegoro', 45), ('Ngawi', 60), ('Nganjuk', 58), ('Gresik', 30), ('Mojokerto', 52), ('Surabaya', 40), ('Sidoarjo', 50)],
    'Gresik': [('Lamongan', 30), ('Surabaya', 18), ('Bojonegoro', 55), ('Ngawi', 75), ('Mojokerto', 38)],
    'Surabaya': [('Gresik', 18), ('Lamongan', 40), ('Mojokerto', 45), ('Sidoarjo', 27), ('Pasuruan', 55)],
    'Mojokerto': [('Bojonegoro', 70), ('Gresik', 38), ('Nganjuk', 65), ('Lamongan', 52),('Surabaya', 45), ('Sidoarjo', 33), ('Pasuruan', 42), ('Malang', 60)],
    'Sidoarjo': [('Surabaya', 27), ('Mojokerto', 33), ('Pasuruan', 40), ('Malang', 50), ('Lamongan', 50)],
    'Pasuruan': [('Sidoarjo', 40), ('Mojokerto', 42), ('Malang', 45), ('Surabaya', 55), ('Nganjuk', 65)],
    'Malang': [('Ngawi', 100), ('Mojokerto', 60), ('Sidoarjo', 50), ('Pasuruan', 45), ('Bojonegoro', 90), ('Nganjuk', 75)]
}

# memasukkan data_graph yang berupa adjacency list kedalam fungsi graph
g = Graph()
g.masuk_data_awal(data_graph)

def main():
    print("\n=== SIMULASI GPS UNTUK MODA TRANSPORTASI MOBIL DI JAWA TIMUR ===")
    print("Daftar Kota:")
    kota_list = g.daftar_kota()
    for kota in kota_list:
        print(f"- {kota}")

    # Buat dictionary map nama kota lowercase ke nama kota sebenarnya untuk validasi input
    kota_dict = {k.lower(): k for k in kota_list}

    while True:
        asal_input = input("\nMasukkan nama kota ASAL: ").strip().lower()
        if asal_input in kota_dict:
            kota_asal = kota_dict[asal_input]
            break
        else:
            print("Nama kota asal tidak ditemukan, coba lagi.")

    while True:
        tujuan_input = input("Masukkan nama kota TUJUAN: ").strip().lower()
        if tujuan_input in kota_dict:
            kota_tujuan = kota_dict[tujuan_input]
            break
        else:
            print("Nama kota tujuan tidak ditemukan, coba lagi.")

    # Dijkstra
    jalur, jarak = g.dijkstra(kota_asal, kota_tujuan)
    print(f"\n[Dijkstra] Jalur tercepat dari {kota_asal} ke {kota_tujuan}:")
    print(" -> ".join(jalur))
    print(f"Total jarak: {jarak} KM")

    # TSP
    print(f"\n[TSP] Menghitung rute terbaik dari {kota_asal} ke semua kota...")
    rute, total = g.tsp_brute_force(kota_asal)
    print(" -> ".join(rute))
    print(f"Total jarak keliling semua kota: {total} KM")
    print("\nAnggota Kelompok \nGathan Yandino Putra Suwandik (24091397026) \nTesa Dwi Sasalbiil (24091397015) \nMuhammad Khairul Anam (24091397002) \nKhabibi Al Munif (24091397004)")

if __name__ == "__main__":
    main()

