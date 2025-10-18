from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# INITIAL DATA
# -----------------------------
def create_initial_data():
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq='ME')
    products = ["Brownies", "Cookies", "Muffin", "Roll Cake"]
    rows = []
    for i, d in enumerate(dates):
        prod = np.random.choice(products)
        harga = np.random.randint(10000, 60000)
        biaya_prod = np.random.randint(4000, harga // 2)
        biaya_iklan = np.random.randint(1000, 5000)
        terjual = np.random.randint(5, 50)
        biaya_ops = np.random.randint(1000, 5000)
        pendapatan = harga * terjual
        modal = biaya_prod * terjual + biaya_iklan
        laba = pendapatan - modal - biaya_ops
        rows.append({
            "ID": i + 1,
            "Tanggal": d.strftime("%Y-%m-%d"),
            "Nama_Produk": prod,
            "Harga_Jual": harga,
            "Biaya_Produksi": biaya_prod,
            "Biaya_Iklan": biaya_iklan,
            "Terjual": terjual,
            "Biaya_Ops": biaya_ops,
            "Pendapatan": pendapatan,
            "Laba": laba
        })
    return pd.DataFrame(rows)

data = create_initial_data()

# -----------------------------
# FUNGSI RE-NUMBER ID
# -----------------------------
def renumber_ids(df):
    """Pastikan kolom ID selalu berurutan dari 1 tanpa lompat"""
    df = df.reset_index(drop=True)
    df["ID"] = df.index + 1
    return df

# -----------------------------
# REDIRECT UTAMA KE /vallenenjoyer
# -----------------------------
@app.route("/")
def home_redirect():
    return redirect(url_for("index"))

# -----------------------------
# ROUTE UTAMA
# -----------------------------
@app.route("/vallenenjoyer", methods=["GET", "POST"])
def index():
    global data
    if request.method == "POST":
        action = request.form.get("action")

        if action == "Tambah":
            tgl = request.form.get("tanggal") or datetime.today().strftime("%Y-%m-%d")
            produk = request.form.get("produk") or "Unknown"
            harga = int(request.form.get("harga") or 0)
            biaya_prod = int(request.form.get("biaya_prod") or 0)
            biaya_iklan = int(request.form.get("biaya_iklan") or 0)
            terjual = int(request.form.get("terjual") or 0)
            biaya_ops = int(request.form.get("biaya_ops") or 0)
            pendapatan = harga * terjual
            modal = biaya_prod * terjual + biaya_iklan
            laba = pendapatan - modal - biaya_ops

            new_row = {
                "ID": len(data) + 1,
                "Tanggal": tgl,
                "Nama_Produk": produk,
                "Harga_Jual": harga,
                "Biaya_Produksi": biaya_prod,
                "Biaya_Iklan": biaya_iklan,
                "Terjual": terjual,
                "Biaya_Ops": biaya_ops,
                "Pendapatan": pendapatan,
                "Laba": laba
            }
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
            data = renumber_ids(data)

        elif action == "Hapus":
            try:
                id_hapus = int(request.form.get("id_hapus"))
                data = data[data["ID"] != id_hapus]
                data = renumber_ids(data)
            except:
                pass

        elif action == "Update":
            try:
                id_edit = int(request.form.get("id_update"))
                produk = request.form.get("produk_update")
                harga = int(request.form.get("harga_update") or 0)
                terjual = int(request.form.get("terjual_update") or 0)
                biaya_prod = int(request.form.get("biaya_prod_update") or 0)
                biaya_iklan = int(request.form.get("biaya_iklan_update") or 0)
                biaya_ops = int(request.form.get("biaya_ops_update") or 0)
                pendapatan = harga * terjual
                modal = biaya_prod * terjual + biaya_iklan
                laba = pendapatan - modal - biaya_ops

                data.loc[data["ID"] == id_edit, [
                    "Nama_Produk", "Harga_Jual", "Terjual", "Biaya_Produksi",
                    "Biaya_Iklan", "Biaya_Ops", "Pendapatan", "Laba"
                ]] = [produk, harga, terjual, biaya_prod, biaya_iklan, biaya_ops, pendapatan, laba]

                data = renumber_ids(data)
            except:
                pass

        return redirect(url_for("index"))

    return render_template("index.html", data=data.to_dict(orient="records"))

# -----------------------------
# JSON DATA UNTUK CHART.JS
# -----------------------------
@app.route("/chart-data")
def chart_data():
    df = data.groupby("Tanggal").sum(numeric_only=True)
    labels = df.index.tolist()
    laba = df["Laba"].tolist()
    pendapatan = df["Pendapatan"].tolist()

    mu, sigma = np.mean(data["Laba"]), np.std(data["Laba"])
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    y = (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-0.5*((x - mu)/sigma)**2)

    return jsonify({
        "labels": labels,
        "laba": laba,
        "pendapatan": pendapatan,
        "dist_x": x.tolist(),
        "dist_y": y.tolist()
    })

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
