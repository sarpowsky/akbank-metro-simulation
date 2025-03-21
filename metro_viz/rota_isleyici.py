import matplotlib.pyplot as plt
import networkx as nx
from tkinter import messagebox

def temizle_highlight_edges(self):
    # Tüm vurgulanan yolları temizle
    for line in self.highlight_edges:
        if line in self.ax.lines:
            line.remove()
    self.highlight_edges = []

def en_az_goster(self, event):
    # Eğer başlangıç veya bitiş istasyonu seçilmemişse hata ver
    if not self.baslangic_istasyon or not self.bitis_istasyon:
        messagebox.showerror("Hata", "Lütfen önce başlangıç ve bitiş istasyonlarını seçin!")
        return
    
    # Önceki animasyonu durdur
    self.animasyon_durdur()
    
    # En az aktarmalı rotayı bul
    en_az_aktarma = self.metro_agi.en_az_aktarma_bul(self.baslangic_istasyon, self.bitis_istasyon)
    if en_az_aktarma:
        # Önce tüm highlight edilmiş yolları temizle
        self.temizle_highlight_edges()
        self.ciz()
        
        # Aktarma sayısını ve süreyi hesapla
        aktarma_sayisi = self.aktarma_sayisi_hesapla(en_az_aktarma)
        sure = self.rota_suresi_hesapla(en_az_aktarma)
        
        # Bilgiyi güncelle
        self.rota_info.set_text(f"En Az Aktarmalı Rota: {aktarma_sayisi} aktarma, {sure} dk ({' → '.join(i.ad for i in en_az_aktarma)})")
        
        # Rotayı çiz - yeşil renkte
        pos = nx.get_node_attributes(self.G, 'pos')
        edges = []
        for i in range(len(en_az_aktarma) - 1):
            edges.append((en_az_aktarma[i].idx, en_az_aktarma[i+1].idx))
            
        for u, v in edges:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            line = plt.Line2D([x0, x1], [y0, y1], 
                            color='#27ae60',  # Yeşil renk
                            linewidth=4,
                            alpha=0.9,
                            solid_capstyle='round',
                            zorder=3)
            self.ax.add_line(line)
            self.highlight_edges.append(line)
            
        self.son_rota_tipi = "en_az"
        self.fig.canvas.draw()
        
        # Animasyon etkinse, rotayı animasyonlu göster
        if self.animasyon_etkin:
            self.animasyon_baslat(en_az_aktarma)

def en_hizli_goster(self, event):
    # Eğer başlangıç veya bitiş istasyonu seçilmemişse hata ver
    if not self.baslangic_istasyon or not self.bitis_istasyon:
        messagebox.showerror("Hata", "Lütfen önce başlangıç ve bitiş istasyonlarını seçin!")
        return
    
    # Önceki animasyonu durdur
    self.animasyon_durdur()
    
    # En hızlı rotayı bul
    en_hizli_sonuc = self.metro_agi.en_hizli_rota_bul(self.baslangic_istasyon, self.bitis_istasyon)
    if en_hizli_sonuc:
        en_hizli_rota, sure = en_hizli_sonuc
        
        # Önce tüm highlight edilmiş yolları temizle
        self.temizle_highlight_edges()
        self.ciz()
        
        # Aktarma sayısını hesapla
        aktarma_sayisi = self.aktarma_sayisi_hesapla(en_hizli_rota)
        
        # Bilgiyi güncelle
        self.rota_info.set_text(f"En Hızlı Rota: {aktarma_sayisi} aktarma, {sure} dk ({' → '.join(i.ad for i in en_hizli_rota)})")
        
        # Rotayı çiz - kırmızı renkte
        pos = nx.get_node_attributes(self.G, 'pos')
        edges = []
        for i in range(len(en_hizli_rota) - 1):
            edges.append((en_hizli_rota[i].idx, en_hizli_rota[i+1].idx))
            
        for u, v in edges:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            line = plt.Line2D([x0, x1], [y0, y1], 
                            color='#c0392b',  # Koyu kırmızı renk
                            linewidth=4,
                            alpha=0.9,
                            solid_capstyle='round',
                            zorder=3)
            self.ax.add_line(line)
            self.highlight_edges.append(line)
            
        self.son_rota_tipi = "en_hizli"
        self.fig.canvas.draw()
        
        # Animasyon etkinse, rotayı animasyonlu göster
        if self.animasyon_etkin:
            self.animasyon_baslat(en_hizli_rota)

def rotalari_bul(self, event):
    """F5 tuşu için eklenen, her iki rotayı da gösteren yardımcı fonksiyon"""
    if not self.baslangic_istasyon or not self.bitis_istasyon:
        messagebox.showerror("Hata", "Lütfen önce başlangıç ve bitiş istasyonlarını seçin!")
        return
        
    # Önce en hızlı rotayı gösterelim
    self.en_hizli_goster(None)
    
    # Sonra en az aktarmalı rotayı da gösterelim (öncekini silip)
    self.en_az_goster(None)