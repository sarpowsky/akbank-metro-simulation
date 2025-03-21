# metro_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from metro_simulation import MetroAgi
from metro_viz import MetroGorselleştirme

class MetroSimulasyonArayuz:
    def __init__(self, root):
        self.root = root
        self.root.title("Metro Simülasyonu")
        self.root.geometry("1280x800")
        self.root.configure(bg='#333333')
        
        # Widget'lar için bir stil ayarlaması yaptım, böylece hepsi aynı temada olacak
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background='#333333')
        style.configure('TLabel', background='#333333', foreground='#FFFFFF')
        style.configure('TButton', background='#333333')
        
        # Metro ağını örneklerden oluşturalım
        self.metro_agi = self.ornek_metro_agi_olustur()
        
        # Arayüzümüzü hazırlayalım
        self.arayuz_olustur()
        
        # Bazı klavye kısayolları ekleyelim, böylece hızlıca işlem yapabiliriz.
        # Bunu implement edilebilir bir fikir olarak koymak istedim, tabiki kullanışlı değil pek şu haliyle.
        self.root.bind('<Control-q>', lambda e: self.cikis())
        self.root.bind('<Control-r>', lambda e: self.metro_gorsel.temizle(None))
        self.root.bind('<F5>', lambda e: self.metro_gorsel.rotalari_bul(None))
        # Animasyon için kısayol ekledim
        self.root.bind('<F6>', lambda e: self.metro_gorsel.animasyon_baslat_durdur(None))
        
        # Kullanıcı çarpı butonuna bastığında çıkış fonksiyonumuzu çağıralım
        self.root.protocol("WM_DELETE_WINDOW", self.cikis)
    
    def stil_ayarla(self):
        # ttk stili için tema ayarları, aslında ben de tam anlamadım ama güzel duruyo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Butonlar için stil ayarları
        style.configure('TButton', 
                       background='#3498db', 
                       foreground='white', 
                       font=('Helvetica', 10, 'bold'),
                       borderwidth=1)
        style.map('TButton', 
                 background=[('active', '#2980b9'), ('pressed', '#1f618d')])
        
        # Frame için stil
        style.configure('TFrame', background='#f0f0f0')
        
        # Etiketler için stil
        style.configure('TLabel', 
                       background='#f0f0f0', 
                       font=('Helvetica', 11))
        
        # Başlık etiketi için stil
        style.configure('Heading.TLabel', 
                       font=('Helvetica', 16, 'bold'), 
                       foreground='#2c3e50')
        
        # Durum çubuğu için stil
        style.configure('Status.TLabel', 
                       background='#ecf0f1', 
                       foreground='#34495e', 
                       font=('Helvetica', 9),
                       relief='sunken')
    
    def ornek_metro_agi_olustur(self):
        # Projede kullanacağımız metro ağını oluşturalım
        # SarpCanKaraman_MetroSimulation.py'deki aynı örneği kullanıyorum, ctrl+c ctrl+v
        metro = MetroAgi()
        
        # İstasyonları ekleyelim
        # Kırmızı hat (K) istasyonları
        metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
        metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
        metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
        metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
        
        # Mavi hat (M) istasyonları 
        metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
        metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")
        metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
        metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
        
        # Turuncu hat (T) istasyonları
        metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
        metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")
        metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")
        metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
        
        # İstasyonlar arası bağlantıları ekleyelim
        # Kırmızı hat içi bağlantılar
        metro.baglanti_ekle("K1", "K2", 4)
        metro.baglanti_ekle("K2", "K3", 6)
        metro.baglanti_ekle("K3", "K4", 8)
        
        # Mavi hat içi bağlantılar
        metro.baglanti_ekle("M1", "M2", 5)
        metro.baglanti_ekle("M2", "M3", 3)
        metro.baglanti_ekle("M3", "M4", 4)
        
        # Turuncu hat içi bağlantılar
        metro.baglanti_ekle("T1", "T2", 7)
        metro.baglanti_ekle("T2", "T3", 9)
        metro.baglanti_ekle("T3", "T4", 5)
        
        # Hat aktarmaları (aynı lokasyondaki farklı istasyonlar arası)
        metro.baglanti_ekle("K1", "M2", 2)  # Kızılay'da aktarma
        metro.baglanti_ekle("K3", "T2", 3)  # Demetevler'de aktarma
        metro.baglanti_ekle("M4", "T3", 2)  # Gar'da aktarma
        
        return metro
    
    def arayuz_olustur(self):
        # Ana paneli oluşturalım
        main_frame = ttk.Frame(self.root, padding=10, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Görselleştirme modülümüzü başlatalım
        self.metro_gorsel = MetroGorselleştirme(self.metro_agi)
        
        # Matplotlib figürünü Tkinter'a entegre edelim
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = FigureCanvasTkAgg(self.metro_gorsel.fig, master=canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Figür olayını bağlayalım (click falan işlemiyor gibi, boş bıraktım)
        self.metro_gorsel.fig.canvas.mpl_connect('button_press_event', lambda e: None)
        
        # Rotalari_bul fonksiyonunu ekleyerek F5 kısayolunun çalışmasını sağlayalım
        self.metro_gorsel.rotalari_bul = self.metro_gorsel.rotalari_bul
        
    def durum_guncelle(self):
       # Şimdilik boş, ileride istersem eğer durum çubuğu eklemek için hazır bıraktım
       pass

    def yardim_goster(self):
        """Kullanımla ilgili bilgiler içeren popup penceresi açalım"""
        yardim = tk.Toplevel(self.root)
        yardim.title("Yardım")
        yardim.geometry("600x400")
        yardim.resizable(False, False)
        
        # İçerik için metin alanı
        yardim_icerik = ttk.Frame(yardim, padding=20)
        yardim_icerik.pack(fill=tk.BOTH, expand=True)
        
        baslik = ttk.Label(yardim_icerik, text="Metro Simülasyonu Nasıl Kullanılır?", 
                          font=("Helvetica", 14, "bold"))
        baslik.pack(pady=10)
        
        icerik_metni = """
Metro Simülasyonu, bir metro ağında en hızlı ve en az aktarmalı rotaları bulmanızı sağlar.

Nasıl kullanılır:
1. Harita üzerinde bir istasyona tıklayarak başlangıç istasyonunu seçin
2. Başka bir istasyona tıklayarak bitiş istasyonunu seçin
3. "En Az Aktarma" veya "En Hızlı" düğmelerine tıklayarak ilgili rotayı görebilirsiniz
4. "Animasyon" düğmesine tıklayarak rotayı animasyonlu olarak izleyebilirsiniz
5. "Temizle" düğmesi seçimleri sıfırlar

Özellikler:
- BFS algoritması ile en az aktarmalı rotayı bulma
- A* algoritması ile en hızlı rotayı bulma
- Rota animasyonu ile yolculuğu gerçek zamanlı izleme
- Çift rota gösterimi (ortak kısımlar yeşil renktedir)
- Aktarma noktalarını gösterme
- İstasyon bilgilerini gösterme

Klavye Kısayolları:
- F5: Rotaları Bul
- F6: Animasyonu Başlat/Durdur
- Ctrl+R: Temizle
- Ctrl+Q: Çıkış
        """
        
        icerik = tk.Text(yardim_icerik, wrap=tk.WORD, height=20, width=70, 
                        font=("Helvetica", 10), bg='#f8f9fa', bd=0)
        icerik.insert(tk.END, icerik_metni)
        icerik.config(state='disabled')
        
        scrollbar = ttk.Scrollbar(yardim_icerik, command=icerik.yview)
        icerik.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        icerik.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        
        # Kapat düğmesi
        kapat_btn = ttk.Button(yardim, text="Kapat", command=yardim.destroy)
        kapat_btn.pack(pady=10)
    
    def cikis(self):
        """Çıkış için onay soralım, öylesine bir güzellik :)"""
        if messagebox.askokcancel("Çıkış", "Metro simülasyonundan çıkmak istiyor musunuz?"):
            self.root.quit()
    
    def calistir(self):
        # Uygulamayı başlat
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MetroSimulasyonArayuz(root)
    app.calistir()