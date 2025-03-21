from tkinter import messagebox
import networkx as nx

def animasyon_etkinlestir(self, event):
    """Animasyon özelliğini etkinleştirir veya devre dışı bırakır"""
    self.animasyon_etkin = not self.animasyon_etkin

def animasyon_baslat(self, rota):
    """Rota animasyonunu başlatır"""
    # Animasyon için ara noktaları hazırla
    self.animasyon_noktalari = self.ara_noktalari_olustur(rota)
    
    # Animasyon değişkenlerini ayarla
    self.anim_idx = 0
    self.animasyon_aktif = True
    
    # Temizlik işlemi - mevcut çizimleri güvenli bir şekilde kaldır
    self.temizle_animasyon_nesneleri()
    
    # Animasyonu başlat - tkinter after metoduyla güvenli şekilde
    self.animasyon_adimi()
        
def animasyon_baslat_durdur(self, event):
    """Animasyon butonunun işlevi - artık kullanılmıyor ama eski referanslar için bıraktım"""
    if self.animasyon_aktif:
        self.animasyon_durdur()
        return
        
    # Rota seçili değilse uyarı ver
    if not self.son_rota_tipi:
        messagebox.showerror("Hata", "Lütfen önce bir rota seçin (En Az Aktarma veya En Hızlı)!")
        return
        
    # İlgili rotayı al ve başlat
    if self.son_rota_tipi == "en_az":
        rota = self.metro_agi.en_az_aktarma_bul(self.baslangic_istasyon, self.bitis_istasyon)
        if rota:
            self.animasyon_baslat(rota)
    else:  # "en_hizli"
        sonuc = self.metro_agi.en_hizli_rota_bul(self.baslangic_istasyon, self.bitis_istasyon)
        if sonuc:
            rota, _ = sonuc
            self.animasyon_baslat(rota)

def ara_noktalari_olustur(self, rota):
    """Rota üzerinde animasyon için ara noktalar oluşturur"""
    ara_noktalar = []
    pos = nx.get_node_attributes(self.G, 'pos')
    
    for i in range(len(rota)-1):
        # İki istasyon arasındaki çizgiyi kademeli olarak çizmek için ara noktalar oluştur
        baslangic = pos[rota[i].idx]
        bitis = pos[rota[i+1].idx]
        aralik_sayisi = 10  # Kademeli geçiş için ara nokta sayısı
        
        # İstasyonlar arası geçiş süresini bul
        gecis_suresi = 0
        for komsu, sure in rota[i].komsular:
            if komsu.idx == rota[i+1].idx:
                gecis_suresi = sure
                break
        
        # Aktarma noktası olup olmadığını kontrol et
        aktarma_mi = (i < len(rota)-1) and (rota[i].hat != rota[i+1].hat)
        
        # Her bir ara nokta için bilgileri tut
        for j in range(aralik_sayisi + 1):
            x = baslangic[0] + (bitis[0] - baslangic[0]) * j / aralik_sayisi
            y = baslangic[1] + (bitis[1] - baslangic[1]) * j / aralik_sayisi
            
            # [x, y, istasyon_mu, aktarma_mi, istasyon_adi, hat, sure]
            if j == 0:
                # Başlangıç istasyonu
                ara_noktalar.append([x, y, True, aktarma_mi, rota[i].ad, rota[i].hat, gecis_suresi])
            elif j == aralik_sayisi:
                # Bitiş istasyonu (rotadaki sonraki istasyon)
                sonraki_aktarma = False
                if i+1 < len(rota)-1:
                    sonraki_aktarma = rota[i+1].hat != rota[i+2].hat
                ara_noktalar.append([x, y, True, sonraki_aktarma, rota[i+1].ad, rota[i+1].hat, 0])
            else:
                # Ara nokta (istasyon değil)
                ara_noktalar.append([x, y, False, False, "", rota[i].hat, 0])
    
    return ara_noktalar

def temizle_animasyon_nesneleri(self):
    """Animasyon nesnelerini güvenli bir şekilde temizler"""
    # Tren markeri temizle
    if hasattr(self, 'tren_marker') and self.tren_marker is not None:
        try:
            # İlk olarak koleksiyonda olup olmadığını kontrol et
            if self.tren_marker in self.ax.collections:
                self.tren_marker.remove()
        except (ValueError, AttributeError):
            pass  # Eğer bir hata olursa sessizce devam et
        self.tren_marker = None
        
    # Bilgi metni temizle
    if hasattr(self, 'bilgi_text') and self.bilgi_text is not None:
        try:
            if self.bilgi_text in self.ax.texts:
                self.bilgi_text.remove()
        except (ValueError, AttributeError):
            pass
        self.bilgi_text = None
        
    # Aktarma efektini temizle
    if hasattr(self, 'aktarma_efekt') and self.aktarma_efekt is not None:
        try:
            if self.aktarma_efekt in self.ax.collections:
                self.aktarma_efekt.remove()
        except (ValueError, AttributeError):
            pass
        self.aktarma_efekt = None

def animasyon_adimi(self):
    """Animasyonun bir adımını çalıştırır - Tkinter after metodu ile çağrılır"""
    if not self.animasyon_aktif or self.anim_idx >= len(self.animasyon_noktalari):
        self.animasyon_durdur()
        return
    
    # Güncel noktanın bilgilerini al
    nokta = self.animasyon_noktalari[self.anim_idx]
    x, y = nokta[0], nokta[1]
    istasyon_mu = nokta[2]
    aktarma_mi = nokta[3]
    istasyon_adi = nokta[4]
    hat = nokta[5]
    
    # Önceki çizimleri temizle
    self.temizle_animasyon_nesneleri()
        
    # Hat rengine göre tren rengini belirle
    renk = self.hat_renkleri.get(hat, "#333333") if hat else "#333333"
    
    # Tren sembolü çiz
    marker_stil = 'o' if not istasyon_mu else 's'
    marker_size = 100 if not istasyon_mu else 200
    
    self.tren_marker = self.ax.scatter(x, y, 
                                    s=marker_size, 
                                    color=renk,
                                    marker=marker_stil,
                                    edgecolor='white',
                                    linewidth=2,
                                    alpha=0.9,
                                    zorder=10)
    
    # İstasyon bilgisi göster
    if istasyon_mu:
        self.bilgi_text = self.ax.text(x, y+0.3, 
                                    istasyon_adi, 
                                    fontsize=12,
                                    ha='center',
                                    va='bottom',
                                    bbox=dict(facecolor='white', 
                                            alpha=0.8,
                                            boxstyle="round,pad=0.3"),
                                    zorder=11)
        
        # Eğer aktarma noktasıysa, özel efekt ekle
        if aktarma_mi:
            self.aktarma_efekt = self.ax.scatter(x, y, s=400, color='yellow', alpha=0.3, zorder=9)
    
    # Çizimi güncelle
    self.fig.canvas.draw()
    
    # Sonraki adıma geç
    self.anim_idx += 1
    
    # Bekleme süresi belirle (istasyonlarda daha uzun bekle)
    bekleme_suresi = 1000 if istasyon_mu else 200  # milisaniye
    
    # Yeni timer ile bir sonraki adımı planla
    if self.animasyon_aktif:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        if isinstance(self.fig.canvas, FigureCanvasTkAgg):
            tkcanvas = self.fig.canvas.get_tk_widget()
            if tkcanvas.winfo_exists():
                self.timer_id = tkcanvas.after(bekleme_suresi, self.animasyon_adimi)
        
def animasyon_durdur(self):
    """Animasyonu durdurur ve temizler"""
    self.animasyon_aktif = False
    
    # Timer'ı iptal et
    if self.timer_id is not None:
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        if isinstance(self.fig.canvas, FigureCanvasTkAgg):
            tkcanvas = self.fig.canvas.get_tk_widget()
            if tkcanvas.winfo_exists():
                try:
                    tkcanvas.after_cancel(self.timer_id)
                except:
                    pass  # Timer zaten iptal edilmiş olabilir
        self.timer_id = None
    
    # Animasyon nesnelerini temizle
    self.temizle_animasyon_nesneleri()
        
    # Çizimi güncelle
    self.fig.canvas.draw()