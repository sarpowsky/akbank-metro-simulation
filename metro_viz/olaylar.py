import networkx as nx
from tkinter import messagebox

def on_click(self, event):
    # Eğer tıklama grafiğin dışındaysa işlem yapma
    if event.inaxes != self.ax:
        return
        
    # Tıklanan noktaya en yakın istasyonu bul
    pos = nx.get_node_attributes(self.G, 'pos')
    min_dist = float('inf')
    closest_node = None
    
    # Tüm istasyonlara olan uzaklığı hesaplayıp en yakınını bul
    for node, (x, y) in pos.items():
        dist = ((x - event.xdata) ** 2 + (y - event.ydata) ** 2) ** 0.5
        if dist < min_dist and dist < 0.5:  # 0.5 birim içindeki istasyonları seç
            min_dist = dist
            closest_node = node
    
    if closest_node:
        istasyon_adi = self.G.nodes[closest_node]['name']
        hat = self.G.nodes[closest_node]['hat']
        
        # İlk seçimse başlangıç istasyonu
        if not self.baslangic_istasyon:
            self.baslangic_istasyon = closest_node
            messagebox.showinfo("Seçim", f"Başlangıç istasyonu: {istasyon_adi} ({hat})")
        # İkinci seçimse bitiş istasyonu 
        elif not self.bitis_istasyon:
            if closest_node == self.baslangic_istasyon:
                messagebox.showwarning("Uyarı", "Başlangıç ve bitiş istasyonları aynı olamaz!")
                return
            self.bitis_istasyon = closest_node
            messagebox.showinfo("Seçim", f"Bitiş istasyonu: {istasyon_adi} ({hat})")
        # İki istasyon da zaten seçilmişse, değiştirmek istediğini sor
        else:
            secim = messagebox.askquestion("Seçim Değiştir", 
                                  "Başlangıç istasyonunu değiştirmek istiyor musunuz?\n" +
                                  "(Hayır'a basarsanız bitiş istasyonu değiştirilecek)")
            if secim == 'yes':
                self.baslangic_istasyon = closest_node
                if self.baslangic_istasyon == self.bitis_istasyon:
                    messagebox.showwarning("Uyarı", "Başlangıç ve bitiş istasyonları aynı olamaz!")
                    self.baslangic_istasyon = None
                    return
                messagebox.showinfo("Seçim", f"Başlangıç istasyonu güncellendi: {istasyon_adi} ({hat})")
            else:
                self.bitis_istasyon = closest_node
                if self.bitis_istasyon == self.baslangic_istasyon:
                    messagebox.showwarning("Uyarı", "Başlangıç ve bitiş istasyonları aynı olamaz!")
                    self.bitis_istasyon = None
                    return
                messagebox.showinfo("Seçim", f"Bitiş istasyonu güncellendi: {istasyon_adi} ({hat})")
        
        # Eğer daha önce rota gösteriliyorsa, sıfırla
        self.temizle_highlight_edges()
        self.son_rota_tipi = None
        self.rota_info.set_text("")
        
        self.ciz()

def temizle(self, event):
    # Tüm seçimleri ve rotaları sıfırla
    self.baslangic_istasyon = None
    self.bitis_istasyon = None
    self.temizle_highlight_edges()
    self.son_rota_tipi = None
    self.rota_info.set_text("")
    self.animasyon_durdur()
    self.ciz()
    messagebox.showinfo("Temizle", "Seçimler temizlendi.")

def yardim_goster(self, event):
    """Kullanıcıya basit bir yardım penceresi göster"""
    messagebox.showinfo("Metro Simülasyonu Yardım", 
                      "Metro Simülasyonu Kullanımı:\n\n" +
                      "1. Haritada istasyonlara tıklayarak önce başlangıç sonra bitiş istasyonu seçin\n" +
                      "2. 'En Az Aktarma' veya 'En Hızlı' butonlarıyla rota seçeneklerini görüntüleyin\n" +
                      "3. 'Animasyon Etkin' kutucuğu ile animasyonu açıp kapatabilirsiniz\n" +
                      "4. 'Temizle' butonuyla seçimleri ve rotaları sıfırlayın\n\n" + 
                      "Özellikler:\n" +
                      "• Aktarma istasyonları daha büyük gösterilir\n" +
                      "• Her hat kendi renginde görüntülenir\n" +
                      "• Aktarma hatları kesikli çizgi ile gösterilir\n" +
                      "• Rota animasyonu ile yolculuğu gerçek zamanlı izleyebilirsiniz\n\n" +
                      "Klavye Kısayolları:\n" +
                      "• F5: Rotaları Bul\n" +
                      "• Ctrl+R: Temizle\n" +
                      "• Ctrl+Q: Çıkış")