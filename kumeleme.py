
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

# VERİYİ OKU

df = pd.read_csv("OnlineRetail.csv", encoding="ISO-8859-1")


# TEMİZLEME

# CustomerID olmayanları at
df = df.dropna(subset=["CustomerID"])

# TARİHİ PARSE ET (gün ilk geliyor!)
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    dayfirst=True,          # 13-12-2010 gibi tarihleri doğru okur
    errors="coerce"         # okunamayanları NaT yap
)

# Tarihi okunamayan satırları at
df = df.dropna(subset=["InvoiceDate"])

# negatif / 0 adet ve fiyatları at
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

# iade faturaları (C ile başlayan)
df = df[~df["InvoiceNo"].astype(str).str.contains("C", na=False)]

# CustomerID int olsun
df["CustomerID"] = df["CustomerID"].astype(int)

# toplam tutar
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]


# RFM TABLOSU

reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (reference_date - x.max()).days,  # Recency
    "InvoiceNo": "nunique",                                    # Frequency
    "TotalPrice": "sum"                                        # Monetary
})

rfm.rename(columns={
    "InvoiceDate": "Recency",
    "InvoiceNo": "Frequency",
    "TotalPrice": "Monetary"
}, inplace=True)

# Bazen Monetary 0 çıkabilir, onları atmak mantıklı
rfm = rfm[rfm["Monetary"] > 0]

# ÖLÇEKLEME

X = rfm[["Recency", "Frequency", "Monetary"]].copy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#  ALGO - KMEANS

kmeans = KMeans(n_clusters=4, random_state=42, n_init="auto")
rfm["Cluster_KMeans"] = kmeans.fit_predict(X_scaled)


# ALGO - HİYERARŞİK (AGGLOMERATIVE)

agg = AgglomerativeClustering(n_clusters=4, linkage="ward")
rfm["Cluster_Agg"] = agg.fit_predict(X_scaled)


# ALGO - DBSCAN

# eps ve min_samples veri setine göre oynanmalı
dbscan = DBSCAN(eps=0.8, min_samples=5)
rfm["Cluster_DBSCAN"] = dbscan.fit_predict(X_scaled)
# DBSCAN'de -1 = gürültü / aykırı


# ÖZETLER

def print_cluster_summary(df_rfm, cluster_col, title):
    print(f"\n===== {title} =====")
    summary = df_rfm.groupby(cluster_col).agg({
        "Recency": ["mean", "median", "count"],
        "Frequency": ["mean", "median"],
        "Monetary": ["mean", "median", "sum"]
    }).round(2)
    print(summary)

print_cluster_summary(rfm, "Cluster_KMeans", "K-Means Küme Özeti")
print_cluster_summary(rfm, "Cluster_Agg", "Agglomerative Küme Özeti")
print_cluster_summary(rfm, "Cluster_DBSCAN", "DBSCAN Küme Özeti")


# KAYDET

rfm.to_csv("rfm_clusters_all.csv")
print("\nrfm_clusters_all.csv dosyası kaydedildi.")

# KISA RAPOR

print("\n=== Kısa Rapor ===")

print("\nK-Means küme sayıları:")
print(rfm["Cluster_KMeans"].value_counts().sort_index())

print("\nAgglomerative küme sayıları:")
print(rfm["Cluster_Agg"].value_counts().sort_index())

print("\nDBSCAN küme sayıları ( -1 = noise ):")
print(rfm["Cluster_DBSCAN"].value_counts().sort_index())


