import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button, CheckButtons

def grafik_olustur(self):
    # Her hat için ofset değerleri - hatları dikey olarak ayırmak için
    hat_konum_ofsetleri = {
        "Kırmızı Hat": (0, 0), 
        "Mavi Hat": (0, -2), 
        "Turuncu Hat": (0, -4)
    }
    
    # Hat bazlı istasyon konumları oluşturalım
    for hat_adi, istasyonlar in self.metro_agi.hatlar.items():
        offset_x, offset_y = hat_konum_ofsetleri[hat_adi]
        for i, istasyon in enumerate(istasyonlar):
            # Özel konum tanımlanmış istasyonlar (aktarma noktaları)
            if istasyon.idx in self.ozel_konumlar:
                x, y = self.ozel_konumlar[istasyon.idx]
                self.istasyon_konumlari[istasyon.idx] = (x, y)
            # Zaten konum atanmış aktarma istasyonları
            elif istasyon.idx in self.istasyon_konumlari:
                continue
            else:
                # Hat boyunca yatay yerleştir
                x = i + offset_x + 2 # +2 ekleyerek solda boşluk bırakalım
                y = offset_y
                self.istasyon_konumlari[istasyon.idx] = (x, y)
            
            # İstasyon türünü belirle (aktarma istasyonu mu?)
            istasyon_turu = "aktarma" if any(k.hat != istasyon.hat for k, _ in istasyon.komsular) else "normal"
            self.G.add_node(istasyon.idx, pos=self.istasyon_konumlari[istasyon.idx], 
                           name=istasyon.ad, hat=istasyon.hat, turu=istasyon_turu)
    
    # İstasyonlar arası bağlantıları ekleyelim
    for istasyon_id, istasyon in self.metro_agi.istasyonlar.items():
        for komsu, sure in istasyon.komsular:
            hat1 = istasyon.hat
            hat2 = komsu.hat
            # Aynı hat içindeyse veya aktarma ise farklı renk ve stil kullan
            if hat1 == hat2:
                renk = self.hat_renkleri[hat1]
                kalinlik = 2.5
                stil = 'solid'
            else:
                renk = "#7f8c8d"  # Aktarma bağlantıları için gri
                kalinlik = 1.8
                stil = 'dashed'
            
            self.G.add_edge(istasyon.idx, komsu.idx, weight=sure, color=renk, 
                           width=kalinlik, style=stil)
    
    # Grafiği çiz
    self.ciz()
    
    # Tıklama olayını ekle - istasyon seçimi için
    self.fig.canvas.mpl_connect('button_press_event', self.on_click)
    
    # Butonlar için konum ayarları
    ax_en_az = plt.axes([0.75, 0.1, 0.15, 0.075])
    self.en_az_butonu = Button(ax_en_az, 'En Az Aktarma', color='#27ae60', hovercolor='#219d54')
    self.en_az_butonu.on_clicked(self.en_az_goster)
    self.en_az_butonu.label.set_color('white')
    
    ax_en_hizli = plt.axes([0.57, 0.1, 0.15, 0.075])
    self.en_hizli_butonu = Button(ax_en_hizli, 'En Hızlı', color='#c0392b', hovercolor='#a93226')
    self.en_hizli_butonu.on_clicked(self.en_hizli_goster)
    self.en_hizli_butonu.label.set_color('white')
    
    ax_temizle = plt.axes([0.1, 0.1, 0.12, 0.075])
    self.temizle_butonu = Button(ax_temizle, 'Temizle', color='#e67e22', hovercolor='#d35400')
    self.temizle_butonu.on_clicked(self.temizle)
    self.temizle_butonu.label.set_color('white')
    
    # Yardım butonu
    ax_yardim = plt.axes([0.92, 0.95, 0.07, 0.04])
    self.yardim_butonu = Button(ax_yardim, 'Yardım', color='#34495e', hovercolor='#2c3e50')
    self.yardim_butonu.on_clicked(self.yardim_goster)
    self.yardim_butonu.label.set_color('white')
    
    # Animasyon etkinleştirme checkboxı
    ax_checkbox = plt.axes([0.82, 0.95, 0.09, 0.04])
    self.animasyon_checkbox = CheckButtons(ax_checkbox, ['Animasyon'], [True])
    self.animasyon_checkbox.on_clicked(self.animasyon_etkinlestir)

    # Checkbox arkaplan
    ax_checkbox.set_facecolor('#34495e')

    # Checkbox stilini ayarla
    try:
        if hasattr(self.animasyon_checkbox, 'rectangles'):
            for rect in self.animasyon_checkbox.rectangles:
                rect.set_facecolor('white')
                rect.set_edgecolor('white')
                rect.set_linewidth(2)
                
            if hasattr(self.animasyon_checkbox, 'lines'):
                for line in self.animasyon_checkbox.lines:
                    for l in line:
                        l.set_color('black')
                        l.set_linewidth(3) 
        
        elif hasattr(self.animasyon_checkbox, 'artists'):
            for artist in self.animasyon_checkbox.artists:
                if hasattr(artist, 'set_facecolor') and artist.get_label() != '_nolegend_':
                    artist.set_facecolor('white')
                if hasattr(artist, 'set_edgecolor'):
                    artist.set_edgecolor('white')
        
        if hasattr(self.animasyon_checkbox, 'labels'):
            for text in self.animasyon_checkbox.labels:
                text.set_color('white')
                text.set_fontsize(10)
    except:
        pass

def ciz(self):
    # Önceki çizimleri temizle - ilk çizimse komple temizle, değilse sadece vurgulamaları
    if not hasattr(self, 'ilk_cizim') or self.ilk_cizim:
        self.ax.clear()
        self.ilk_cizim = False
    else:
        # Highlight edilmiş kenarları temizle
        for line in self.highlight_edges:
            if line in self.ax.lines:
                line.remove()
        self.highlight_edges = []
        
        # İstasyon düğümlerini temizle
        for collection in self.ax.collections:
            collection.remove()
    
    # Arkaplan stil ayarları
    self.ax.set_facecolor('#d9d9d9')
    self.ax.grid(True, linestyle='--', alpha=0.3)
    
    # İstasyon konumlarını al
    pos = nx.get_node_attributes(self.G, 'pos')
    
    # Her hat için ayrı çizgiler çiz
    for hat, renk in self.hat_renkleri.items():
        hat_edges = [(u, v) for u, v, d in self.G.edges(data=True) 
                   if self.G.nodes[u]['hat'] == hat and self.G.nodes[v]['hat'] == hat]
        
        # Hat üzerindeki kenarları çiz
        for u, v in hat_edges:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            line = plt.Line2D([x0, x1], [y0, y1], color=renk,
                            linewidth=3.0, alpha=0.8,
                            solid_capstyle='round',
                            zorder=1)
            self.ax.add_line(line)
    
    # Aktarma bağlantılarını çiz (farklı hat istasyonları arasındaki bağlantılar)
    aktarma_edges = [(u, v) for u, v, d in self.G.edges(data=True) 
                   if self.G.nodes[u]['hat'] != self.G.nodes[v]['hat']]
    
    for u, v in aktarma_edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        line = plt.Line2D([x0, x1], [y0, y1], color='#7f8c8d',
                        linewidth=1.8, alpha=0.7,
                        linestyle='dashed',
                        zorder=1)
        self.ax.add_line(line)
    
    # İstasyon düğümlerini çiz - aktarma istasyonları daha büyük olsun
    node_sizes = []
    for node in self.G.nodes():
        # Aktarma istasyonları için daha büyük boyut
        if any(self.G.nodes[komsu]['hat'] != self.G.nodes[node]['hat'] 
              for komsu in self.G.neighbors(node)):
            node_sizes.append(850)
        else:
            node_sizes.append(650)
    
    # Düğümleri hat renklerine göre çiz
    for hat, renk in self.hat_renkleri.items():
        hat_nodes = [node for node, attr in self.G.nodes(data=True) if attr.get('hat') == hat]
        hat_sizes = [node_sizes[list(self.G.nodes()).index(node)] for node in hat_nodes]
        
        nx.draw_networkx_nodes(self.G, pos, ax=self.ax, nodelist=hat_nodes, 
                             node_color=renk, node_size=hat_sizes, alpha=0.85,
                             edgecolors='#c0c0c0', linewidths=2, node_shape='o')
    
    # Başlangıç ve bitiş istasyonlarını vurgula
    if self.baslangic_istasyon:
        nx.draw_networkx_nodes(self.G, pos, ax=self.ax, nodelist=[self.baslangic_istasyon], 
                             node_color='#abebc6', node_size=900, 
                             edgecolors='#27ae60', linewidths=3)
        baslangic_ad = self.G.nodes[self.baslangic_istasyon]['name']
        self.baslangic_text.set_text(f"Başlangıç: {baslangic_ad}")
    else:
        self.baslangic_text.set_text("")
    if self.bitis_istasyon:
        nx.draw_networkx_nodes(self.G, pos, ax=self.ax, nodelist=[self.bitis_istasyon], 
                             node_color='#f5b7b1', node_size=900,
                             edgecolors='#c0392b', linewidths=3)
        bitis_ad = self.G.nodes[self.bitis_istasyon]['name']
        self.bitis_text.set_text(f"Bitiş: {bitis_ad}")
    else:
        self.bitis_text.set_text("")
    
    # İstasyon isimlerini göster - ilk kez çiziyorsak
    if not self.node_labels:
        labels = {node: self.G.nodes[node]['name'] for node in self.G.nodes()}
        self.node_labels = nx.draw_networkx_labels(self.G, pos, labels=labels, font_size=10, 
                                                font_weight='bold', font_family='sans-serif')
    
    # İstasyonlar arası süreleri göster - ilk kez çiziyorsak
    if not self.edge_labels:
        edge_labels = {(u, v): f"{self.G[u][v]['weight']} dk" for u, v in self.G.edges()}
        
        self.edge_labels = nx.draw_networkx_edge_labels(
            self.G, pos, edge_labels=edge_labels,
            font_size=9, font_weight='bold', font_color='#333333',
            bbox=dict(facecolor='#d9d9d9', edgecolor='#999999', alpha=0.95, boxstyle='round,pad=0.3'),
            label_pos=0.35,
            verticalalignment='bottom',
            horizontalalignment='center',
            rotate=False,
            ax=self.ax
        )
    
    # Harita için açıklama (legend) ekle
    legend_elements = [mpatches.Patch(color=color, label=hat) 
                     for hat, color in self.hat_renkleri.items()]
    legend_elements.append(mpatches.Patch(color='#7f8c8d', label='Aktarma'))
    legend_elements.append(mpatches.Patch(color='#abebc6', label='Başlangıç'))
    legend_elements.append(mpatches.Patch(color='#f5b7b1', label='Bitiş'))
    
    self.ax.legend(handles=legend_elements, loc='upper right', 
                 bbox_to_anchor=(0.99, 0.99), fancybox=True, shadow=True)
    
    # Harita başlığı ekle
    self.ax.set_title('Metro Ağı Simülasyonu', fontsize=18, fontweight='bold', 
                   color='#f0f0f0', pad=15,
                   bbox=dict(facecolor='#444444', alpha=0.8, boxstyle='round,pad=0.5'))
    
    # Eksen etiketlerini kaldır - gereksiz görünüyordu
    self.ax.set_xticks([])
    self.ax.set_yticks([])
    
    # Çizimi güncelle
    self.fig.canvas.draw()