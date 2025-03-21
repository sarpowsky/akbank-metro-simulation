import matplotlib.pyplot as plt
import networkx as nx
from .cizim import grafik_olustur, ciz
from .olaylar import on_click, temizle, yardim_goster
from .rota_isleyici import en_az_goster, en_hizli_goster, rotalari_bul, temizle_highlight_edges
from .animasyon import (animasyon_baslat, animasyon_durdur, animasyon_adimi, animasyon_baslat_durdur, 
                       ara_noktalari_olustur, temizle_animasyon_nesneleri, animasyon_etkinlestir)
from .yardimcilar import aktarma_sayisi_hesapla, rota_suresi_hesapla

class MetroGorselleştirme:
    def __init__(self, metro_agi):
        self.metro_agi = metro_agi
        self.G = nx.Graph()
        
        # Koyu tema fena olmadı, gerçi tkinterla nasıl yaparım bilemedim daha bu şekil
        self.fig = plt.figure(figsize=(12, 8), facecolor='#333333')
        self.ax = self.fig.add_subplot(111)
        
        # Figure içinde elemanları düzgün yerleştirmek için margin ayarı
        self.fig.subplots_adjust(bottom=0.25, top=0.85, left=0.05, right=0.95)
        
        # İstasyon seçimleri için değişkenler
        self.baslangic_istasyon = None
        self.bitis_istasyon = None
        
        # Hat renkleri - gerçek metro hattı renklerine yakın seçtim
        self.hat_renkleri = {
            "Kırmızı Hat": "#e74c3c",
            "Mavi Hat": "#3498db",
            "Turuncu Hat": "#f39c12"
        }
        
        # Aktarma noktaları için özel konumlar, bu kısmı yapmakta biraz zorlandım 
        # Çünkü aynı istasyonun farklı hatlar için farklı konumda olması gerekiyor
        self.ozel_konumlar = {
            "K1": (2, 0),    # Kızılay (Kırmızı)
            "M2": (2, -0.5), # Kızılay (Mavi)
            "K3": (4, 0),    # Demetevler (Kırmızı)
            "T2": (4, -0.5), # Demetevler (Turuncu)
            "M4": (6, -2),   # Gar (Mavi)
            "T3": (6, -2.5)  # Gar (Turuncu)
        }
        
        # İstasyon konumları, kenar vurgulamaları ve diğer görsel değişkenler
        self.istasyon_konumlari = {}
        self.highlight_edges = []
        self.son_rota_tipi = None
        self.node_labels = {}
        self.edge_labels = {}
        
        # Animasyon değişkenleri
        self.animasyon_aktif = False
        self.anim_idx = 0
        self.animasyon_noktalari = []
        self.tren_marker = None
        self.bilgi_text = None
        self.aktarma_efekt = None
        self.timer_id = None  # Tkinter timer id
        self.animasyon_etkin = True  # Animasyon özelliğinin etkin olup olmadığını belirten değişken
        
        # Sol üstte gösterilen bilgilendirme kutucukları
        self.baslangic_text = self.fig.text(0.15, 0.93, "", fontsize=11, ha='left', va='top',
                                  bbox=dict(boxstyle="round,pad=0.3", facecolor='#abebc6', 
                                          edgecolor='#27ae60', alpha=0.8))
        self.bitis_text = self.fig.text(0.15, 0.88, "", fontsize=11, ha='left', va='top',
                                    bbox=dict(boxstyle="round,pad=0.3", facecolor='#f5b7b1', 
                                                edgecolor='#c0392b', alpha=0.8))
        
        # Alt kısımda gösterilen rota bilgisi
        self.rota_info = self.fig.text(0.5, 0.05, "", fontsize=11, ha='center', va='bottom',
                                      bbox=dict(boxstyle="round,pad=0.3", facecolor='#d4e6f1', 
                                               edgecolor='#3498db', alpha=0.8))
        
        # Köşeye bir imza çakmak istedim :)
        self.imza = self.fig.text(0.95, 0.02, "by _sarpowsky", fontsize=10, ha='right', va='bottom',
                                color='white', alpha=0.8, fontweight='bold')
        
        # Grafiği oluşturalım
        self.grafik_olustur()
        
    def grafik_olustur(self):
        return grafik_olustur(self)
        
    def ciz(self):
        return ciz(self)
    
    def on_click(self, event):
        return on_click(self, event)
    
    def en_az_goster(self, event):
        return en_az_goster(self, event)
    
    def en_hizli_goster(self, event):
        return en_hizli_goster(self, event)
    
    def rotalari_bul(self, event):
        return rotalari_bul(self, event)
    
    def temizle(self, event):
        return temizle(self, event)
    
    def temizle_highlight_edges(self):
        return temizle_highlight_edges(self)
    
    def yardim_goster(self, event):
        return yardim_goster(self, event)
    
    def aktarma_sayisi_hesapla(self, istasyon_listesi):
        return aktarma_sayisi_hesapla(istasyon_listesi)
    
    def rota_suresi_hesapla(self, istasyon_listesi):
        return rota_suresi_hesapla(self, istasyon_listesi)
    
    def animasyon_baslat(self, rota):
        return animasyon_baslat(self, rota)
    
    def animasyon_baslat_durdur(self, event):
        return animasyon_baslat_durdur(self, event)
    
    def ara_noktalari_olustur(self, rota):
        return ara_noktalari_olustur(self, rota)
    
    def temizle_animasyon_nesneleri(self):
        return temizle_animasyon_nesneleri(self)
    
    def animasyon_adimi(self):
        return animasyon_adimi(self)
    
    def animasyon_durdur(self):
        return animasyon_durdur(self)
    
    def animasyon_etkinlestir(self, event):
        return animasyon_etkinlestir(self, event)
    
    def goster(self):
        plt.show()