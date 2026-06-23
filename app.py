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

st.markdown("""
<h1 style='text-align: center;'>
Simulator Kebijakan Keuntungan Toko
</h1>
""", unsafe_allow_html=True)

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
st.markdown("""
<style>
.prediksi-card {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}

.prediksi-title {
    font-size: 18px;
    font-weight: 500;
    opacity: 0.9;
    margin-bottom: 10px;
}

.prediksi-value {
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 15px;
}

.prediksi-delta {
    display: inline-block;
    background-color: rgba(255,255,255,0.15);
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 18px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="prediksi-card">
    <div class="prediksi-title">Prediksi Keuntungan</div>
    <div class="prediksi-value">Rp {hasil_pred:.2f} Jt</div>
    <div class="prediksi-delta">
        {'▲' if delta >= 0 else '▼'} {delta:.2f} Jt dari baseline
    </div>
</div>
""", unsafe_allow_html=True)

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
