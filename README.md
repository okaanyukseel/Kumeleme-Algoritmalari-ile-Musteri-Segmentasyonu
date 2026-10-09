# Kümeleme Algoritmaları ile Müşteri Segmentasyonu

Projede python programlama dili kullanılmıştır.
Kumeleme algoritmaları kullanılarak musteri segmentasyonu tahmin etmek için yapılmıştır.

Müşteriler, alışveriş verilerinden hesaplanan **RFM** (Recency, Frequency, Monetary) değerlerine göre üç farklı kümeleme algoritmasıyla gruplandırılır:

- K-Means
- Agglomerative (Hiyerarşik) Kümeleme
- DBSCAN

---

## Veri Seti

Veri seti **depoda bulunmamaktadır**. Kod, çalışma dizininde `OnlineRetail.csv` adlı bir dosya bekler ve onu `ISO-8859-1` kodlamasıyla okur.

Kodda kullanılan sütunlar:

| Sütun | Kullanım |
|---|---|
| `CustomerID` | Müşteri kimliği (boş olan satırlar atılır) |
| `InvoiceNo` | Fatura numarası (`C` içerenler iade kabul edilip atılır; Frequency hesabı) |
| `InvoiceDate` | Fatura tarihi (gün önce gelecek şekilde, `dayfirst=True` ile okunur) |
| `Quantity` | Ürün adedi |
| `UnitPrice` | Birim fiyat |

---

## Yöntem

1. **Temizleme**
   - `CustomerID` boş olan satırlar atılır.
   - `InvoiceDate` tarihe çevrilir; okunamayan tarihler atılır.
   - `Quantity <= 0` veya `UnitPrice <= 0` olan satırlar atılır.
   - İade faturaları (`InvoiceNo` içinde `C` geçenler) atılır.
   - `TotalPrice = Quantity * UnitPrice` hesaplanır.
2. **RFM tablosu** (müşteri bazında)
   - **Recency**: Referans tarihi (veri setindeki son tarih + 1 gün) ile müşterinin son alışverişi arasındaki gün sayısı
   - **Frequency**: Benzersiz fatura sayısı
   - **Monetary**: Toplam harcama (`TotalPrice` toplamı)
   - `Monetary <= 0` olan müşteriler atılır.
3. **Ölçekleme**: RFM değerleri `StandardScaler` ile standartlaştırılır.
4. **Kümeleme**
   - `KMeans(n_clusters=4, random_state=42, n_init="auto")`
   - `AgglomerativeClustering(n_clusters=4, linkage="ward")`
   - `DBSCAN(eps=0.8, min_samples=5)` (`-1` etiketi gürültü / aykırı noktaları ifade eder)
5. **Özetler**: Her algoritma için küme bazında Recency / Frequency / Monetary ortalama, medyan, adet ve toplam değerleri ile küme büyüklükleri yazdırılır.
6. **Çıktı**: Tüm küme etiketlerini içeren RFM tablosu `rfm_clusters_all.csv` dosyasına kaydedilir.

---

## Sonuçlar

Depoda kaydedilmiş bir çıktı bulunmamaktadır. Küme özetlerini görmek için betiği çalıştırın; sonuçlar konsola yazdırılır ve `rfm_clusters_all.csv` dosyasına kaydedilir.

---

## Proje Yapısı

```
.
├── kumeleme.py        # Veri temizleme, RFM hesaplama, kümeleme ve raporlama
├── requirements.txt
└── README.md
```

---

## Çalıştırma

1. `OnlineRetail.csv` dosyasını depo klasörüne koyun.
2. Bağımlılıkları kurup betiği çalıştırın:

```bash
pip install -r requirements.txt
python kumeleme.py
```

---

## Gereksinimler

- Python 3
- pandas
- numpy
- scikit-learn (`KMeans(n_init="auto")` kullanıldığı için 1.2 veya üzeri bir sürüm gerekir)
