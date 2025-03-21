def aktarma_sayisi_hesapla(istasyon_listesi):
    """Bir rotada kaç aktarma olduğunu hesapla - hat değişimi sayısı"""
    aktarma = 0
    for i in range(1, len(istasyon_listesi)):
        if istasyon_listesi[i].hat != istasyon_listesi[i-1].hat:
            aktarma += 1
    return aktarma

def rota_suresi_hesapla(self, istasyon_listesi):
    """İstasyonlar arası geçiş sürelerini toplayarak rota süresini hesapla"""
    toplam_sure = 0
    for i in range(len(istasyon_listesi)-1):
        mevcut = istasyon_listesi[i]
        sonraki = istasyon_listesi[i+1]
        
        # Komsular arasında süreyi bul
        for komsu, sure in mevcut.komsular:
            if komsu.idx == sonraki.idx:
                toplam_sure += sure
                break
                
    return toplam_sure