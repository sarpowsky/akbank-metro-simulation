from collections import defaultdict
import heapq
from typing import Dict, List, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:  # 'id' yerine 'idx' kullandım burada
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """Burada fonskyion BFS'in aksine Dijkstra algoritması ile en az aktarmalı rotayı bulur.
        
        Denemelerim sonucunda mavi hattaki Gar durağından kırmızı hattaki Demetevler durağına giderken
        algoritmanın tek aktarmalı kızılay aktarması rotası yerine en hızlı rota ile aynı yolu seçtiğini farkettim.
        bu sorunu çözmek için araştırma yaptığımda Dijkstra algoritmasıyla karşılaştım ve implemente ettim.

        Hat değişimlerine çok yüksek ağırlık vererek, öncelikle hat değişimlerini,
        sonra istasyon sayısını minimize eden rotayı bulur.
        
        Bu algoritma biraz karmaşık ama arayüz için gerekli olduğundan bu şekilde bıraktım.
        """
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        # Mesafeler ve önceki düğümler - klasik Dijkstra için gerekli
        mesafeler = {istasyon_id: float('infinity') for istasyon_id in self.istasyonlar}
        mesafeler[baslangic_id] = 0
        onceki = {istasyon_id: None for istasyon_id in self.istasyonlar}
        aktarma_hatlari = {istasyon_id: None for istasyon_id in self.istasyonlar}
        aktarma_hatlari[baslangic_id] = baslangic.hat
        
        # Dijkstra'nın öncelikli kuyruğu - en düşük maliyetli rotaları önce işliyecek
        kuyruk = [(0, id(baslangic), baslangic_id)]  # (maliyet, id, istasyon_id)
        
        while kuyruk:
            maliyet, _, simdiki_id = heapq.heappop(kuyruk)
            
            if simdiki_id == hedef_id:
                break
            
            if maliyet > mesafeler[simdiki_id]:
                continue
            
            simdiki = self.istasyonlar[simdiki_id]
            simdiki_hat = aktarma_hatlari[simdiki_id]
            
            for komsu, _ in simdiki.komsular:
                # Hat değişimi maliyeti - burada maliyetler üzerinden bir çözüm yaptım
                ek_maliyet = 1  # İstasyon geçişi maliyeti
                if komsu.hat != simdiki_hat:
                    ek_maliyet = 1000  # Hat değişimi çok maliyetli - böylece aktarmayı minimize ediyoruz
                
                yeni_maliyet = mesafeler[simdiki_id] + ek_maliyet
                
                if yeni_maliyet < mesafeler[komsu.idx]:
                    mesafeler[komsu.idx] = yeni_maliyet
                    onceki[komsu.idx] = simdiki_id
                    aktarma_hatlari[komsu.idx] = komsu.hat
                    heapq.heappush(kuyruk, (yeni_maliyet, id(komsu), komsu.idx))
        
        # Rotayı oluştur - hedeften başlangıca doğru gidip sonra ters çevireceğiz
        if onceki[hedef_id] is None:
            return None
        
        rota = []
        simdiki_id = hedef_id
        while simdiki_id is not None:
            rota.append(self.istasyonlar[simdiki_id])
            simdiki_id = onceki[simdiki_id]
        
        # Rotayı tersine çevir (başlangıçtan hedefe) - bu kısmı unutmamak önemliydi
        rota.reverse()
        return rota

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """En kısa süren rotayı bulan fonksiyon.
        
        A* algoritması kullanarak en hızlı rotayı arar. 
        Biraz karışık ama öğrenmek için fırsat olmuş oldu. Sanırım farklı senaryolarda
        yine Dijkstra kullanabilirdik anladığım kadarıyla, ama projede A* istediği için nolur nolmaz onu implemente ettim.
        """
        # önce istasyonların var olduğundan emin olalım
        if baslangic_id not in self.istasyonlar:
            return None
        if hedef_id not in self.istasyonlar:  # ayrı ayrı kontrol etmem gerekmiyor ama daha okunabilir
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        # gördüğüm istasyonları hatırlamam lazım
        ziyaret_edildi = set()  
        
        # A* algoritması için öncelik kuyruğu - en düşük süreli rotaları önce işleyecek
        # (toplam_sure, id, istasyon, rota, şimdiye_kadarki_sure)
        pq = []  # priority queue 
        # öncelik kuyruğuna ilk elemanı ekleyelim
        heapq.heappush(pq, (0, id(baslangic), baslangic, [baslangic], 0))
        
        while pq:  # kuyruk boşalana kadar
            # en az süreli yolu al
            toplam, _, curr, rota, gecen_sure = heapq.heappop(pq)
            
            # eğer bulduysan dön
            if curr == hedef:
                return (rota, gecen_sure)
            
            # eğer bu noktayı daha önce ziyaret ettiysen geç
            if curr in ziyaret_edildi:
                continue
                
            # istasyonu ziyaret ettik
            ziyaret_edildi.add(curr)
            
            # bütün komşuları deneyelim
            for komsu, komsu_sure in curr.komsular:
                if komsu in ziyaret_edildi:  # zaten ziyaret edildiyse geç
                    continue
                    
                # toplam süre hesabı
                total_sure = gecen_sure + komsu_sure
                
                # yeni rota oluştur - en basit yoldan
                yeni_rota = rota + [komsu]
                
                # A* öncelik kuyruğuna ekle
                # burada A* için aslında bir sezgisel fonk. (heuristic) ekleyebilirdim
                # ama bu örnekte sezgisel fonk. yerine sadece geçen süreyi kullandım
                heapq.heappush(pq, (total_sure, id(komsu), komsu, yeni_rota, total_sure))
        
        # yol bulunamadı :(
        return None

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))