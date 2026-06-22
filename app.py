import streamlit as st
import pandas as pd
import numpy as np
import joblib

saved = joblib.load("simulator.pkl")

model = saved["model"]
baseline_pred = saved["baseline_pred"]

def run_simulation(iklan, diskon):
    input_data = np.array([[iklan, diskon]])

    prediction = model.predict(input_data)[0]

    delta = prediction - baseline_pred

    return prediction, delta

def generate_insight(iklan, diskon):
    insights = []

    if iklan < 10:
        insights.append("Anggaran iklan rendah dapat mengurangi jangkauan pelanggan.")

    if iklan > 30:
        insights.append("Iklan tinggi berpotensi meningkatkan awareness, tapi biaya juga naik.")

    if diskon > 25:
        insights.append("Diskon besar bisa meningkatkan penjualan jangka pendek, tapi menekan margin.")

    if diskon == 0:
        insights.append("Tanpa diskon, penjualan sangat bergantung pada iklan.")

    if iklan >= 20 and diskon >= 20:
        insights.append("Kombinasi iklan & diskon agresif: cocok untuk promo besar / event.")

    if not insights:
        insights.append("Kombinasi saat ini relatif stabil dan seimbang.")

    return insights

#streamlit UI

st.title("Simulator Kebijakan Keuntungan Toko")

# --- SIDEBAR: Variabel Kontrol ---
st.sidebar.header("Tuas Kebijakan (Intervensi)")
iklan_slider = st.sidebar.slider("Anggaran Iklan (Juta)", 0, 50, 10)
diskon_slider = st.sidebar.slider("Besaran Diskon (%)", 0, 50, 10)

st.sidebar.text("Geser slider untuk menyesuaikan skenario intervensi. Sistem akan memprediksi perubahan keuntungan dibandingkan baseline.")

st.sidebar.markdown("---")
st.sidebar.text("Alfan Pratama Farisqi\n2313020192\nkelas 3A")

# --- ENGINE: Jalankan Simulasi ---
hasil_pred, delta = run_simulation(iklan_slider, diskon_slider)

# --- UI: Tampilkan Hasil ---
col1, col2 = st.columns(2)
col1.metric("Prediksi Keuntungan", f"Rp {hasil_pred:.2f} Jt", f"{delta:.2f} Jt")
col2.write(f"Skenario ini menghasilkan perubahan sebesar {delta:.2f} Juta dibandingkan kondisi baseline.")

# Visualisasi Perbandingan
data_plot = pd.DataFrame({
    'Skenario': ['Baseline', 'Intervensi'],
    'Keuntungan': [baseline_pred, hasil_pred]
})
st.bar_chart(data=data_plot, x='Skenario', y='Keuntungan')
st.subheader("Insight & Rekomendasi")

insights = generate_insight(iklan_slider, diskon_slider)

for i in insights:
    st.info(i)

st.subheader("Analisis Singkat")
st.write(
    f"Dengan iklan sebesar {iklan_slider} juta dan diskon {diskon_slider}%, "
    f"sistem memprediksi perubahan keuntungan sebesar {delta:.2f} juta "
    f"dari baseline."
)