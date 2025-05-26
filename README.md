# LinkedIn Connection Automation Tool

Bu araç, LinkedIn'de otomatik olarak bağlantı isteği göndermenizi sağlayan bir Python betiğidir. Belirlediğiniz anahtar kelimelerle arama yaparak bağlantı istekleri gönderebilirsiniz.

## Özellikler

- Otomatik LinkedIn girişi
- 2FA (İki faktörlü doğrulama) bekleme.
- Özelleştirilebilir bağlantı notları.
- Arama sonuçlarından bağlantı isteği gönderme
- Haftalık bağlantı limiti kontrolü

## Ön Gereksinimler

- Python 3.7 veya üzeri
- Chrome tarayıcı
- LinkedIn hesabı

## Kurulum

1. Projeyi klonlayın veya indirin:
   ```bash
   git clone https://github.com/xeloxa/linkedauto.git
   cd linkedauto
   ```

2. Sanal ortam oluşturun ve etkinleştirin:
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Kullanım

1. Betiği çalıştırın:
   ```bash
   python linkedAuto.py
   ```

2. Ekrandaki yönergeleri takip edin:

## Sık Karşılaşılan Sorunlar

- **Chrome sürüm uyumsuzluğu**: `webdriver-manager` otomatik olarak doğru ChromeDriver sürümünü yüklemelidir. Eğer sorun yaşarsanız, Chrome tarayıcınızı güncelleyin.
- **Giriş başarısız oluyor**: 2FA etkinse, giriş sırasında doğrulama kodu girmeniz gerekebilir.
- **Bağlantı istekleri gönderilmiyor**: LinkedIn'in haftalık bağlantı limitine ulaşmış olabilirsiniz. Bir süre bekleyip tekrar deneyin.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## Katkıda Bulunma

Hata düzeltmeleri ve yeni özellikler için pull request'lerinizi bekliyoruz. Lütfen önce bir konu açarak yapmak istediğiniz değişiklikleri tartışın.

## Sorumluluk Reddi

Bu araç yalnızca eğitim amaçlıdır. LinkedIn'in Kullanım Şartları'nı ihlal etmekten kaçının. Bu aracı kullanmanızdan doğabilecek her türlü sorumluluk size aittir.
