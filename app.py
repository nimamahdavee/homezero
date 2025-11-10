import streamlit as st
import matplotlib.pyplot as plt

# -------- PAGE SETUP --------
st.set_page_config(page_title="Shared Energy. Shared Future.", page_icon="🏡", layout="wide")

# -------- DARK THEME (HIGH CONTRAST) --------
st.markdown("""
<style>
  :root {
    --bg: #071a12;         /* main dark green */
    --panel: #0e2a1f;      /* panel dark */
    --text: #ffffff;       /* pure white */
    --muted: #d5e7df;      /* soft white for captions */
    --accent: #39d98a;     /* mint green */
    --gray: #9aa5a1;
  }
  .stApp { background: var(--bg); color: var(--text); }
  /* Sidebar */
  section[data-testid="stSidebar"] { background: #0b241b !important; }
  section[data-testid="stSidebar"] * { color: var(--text) !important; }
  .stSlider label, .stNumberInput label { color: var(--text) !important; }
  /* Headings */
  h1, h2, h3, h4 { color: var(--text) !important; }
  /* Custom KPI cards */
  .card { background: var(--panel); border:1px solid rgba(255,255,255,.12);
          border-radius:14px; padding:16px; }
  .card .title { font-size:0.95rem; color: var(--muted); margin-bottom:6px; }
  .card .value { font-size:1.8rem; font-weight:800; color: var(--text); }
  .card .delta { font-size:0.95rem; color: var(--accent); margin-top:6px; }
  .divider { height:1px; background: rgba(255,255,255,.16); margin: 12px 0 24px; }
</style>
""", unsafe_allow_html=True)

st.title("🌱 Green Block – Interactive Savings & CO₂ Calculator")
st.caption("Adjust the parameters below to see how community heating improves cost and emissions.")

# -------- SIDEBAR SLIDERS --------
st.sidebar.header("Adjust Parameters")

n_houses            = st.sidebar.slider("Number of Houses in the Community", 10, 500, 100, 10)
avg_gas_m3          = st.sidebar.slider("Average Gas Use per Home (m³/year)", 500, 2500, 1200, 50)
gas_price           = st.sidebar.slider("Gas Price (€/m³)", 0.80, 2.00, 1.20, 0.05)
district_heat_price = st.sidebar.slider("District Heat Price (€/kWh_th)", 0.05, 0.25, 0.12, 0.01)
co2_factor_gas      = st.sidebar.slider("CO₂ Factor – Gas (kg/m³)", 1.50, 2.50, 1.88, 0.01)
co2_factor_dh       = st.sidebar.slider("CO₂ Factor – District Heat (kg/kWh)", 0.01, 0.20, 0.05, 0.01)

# -------- CALCULATIONS --------
kwh_per_m3  = 9.77
boiler_eff  = 0.90

# Before (individual gas)
heat_kwh_home   = avg_gas_m3 * kwh_per_m3 * boiler_eff
cost_before     = avg_gas_m3 * gas_price
co2_before      = avg_gas_m3 * co2_factor_gas

# After (district heating)
cost_after      = heat_kwh_home * district_heat_price
co2_after       = heat_kwh_home * co2_factor_dh

# Totals for community
total_cost_before   = cost_before * n_houses
total_cost_after    = cost_after * n_houses
total_savings       = total_cost_before - total_cost_after
total_co2_before    = co2_before * n_houses
total_co2_after     = co2_after * n_houses
total_co2_reduction = total_co2_before - total_co2_after
savings_pct         = (total_savings / total_cost_before * 100) if total_cost_before else 0
co2_pct             = (total_co2_reduction / total_co2_before * 100) if total_co2_before else 0

# -------- KPI CARDS (HIGH CONTRAST) --------
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.subheader("🏘️ Community Summary")

c1, c2, c3 = st.columns(3)

with c1:
  st.markdown(f"""
  <div class="card">
    <div class="title">Total Houses</div>
    <div class="value">{n_houses:,}</div>
  </div>
  """, unsafe_allow_html=True)

with c2:
  st.markdown(f"""
  <div class="card">
    <div class="title">Total Annual Savings (€)</div>
    <div class="value">€{total_savings:,.0f}</div>
    <div class="delta">↑ {savings_pct:.0f}%</div>
  </div>
  """, unsafe_allow_html=True)

with c3:
  st.markdown(f"""
  <div class="card">
    <div class="title">CO₂ Reduction (tonnes)</div>
    <div class="value">{total_co2_reduction/1000:,.1f}</div>
    <div class="delta">↑ {co2_pct:.0f}%</div>
  </div>
  """, unsafe_allow_html=True)

# -------- CHARTS (DARK-FRIENDLY) --------
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("### 📊 Annual Cost and CO₂ Comparison")

fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.6))

# Cost
ax[0].bar(["Before", "After"], [total_cost_before, total_cost_after],
          color=["#8a8f8d", "#39d98a"])
ax[0].set_title("Total Annual Cost (€)", color="white")
ax[0].set_facecolor("#0e2a1f")
for spine in ax[0].spines.values(): spine.set_visible(False)
ax[0].tick_params(colors="white")
for i, v in enumerate([total_cost_before, total_cost_after]):
    ax[0].text(i, v*1.02, f"€{v:,.0f}", ha="center", color="white", fontsize=10)

# CO2
ax[1].bar(["Before", "After"],
          [total_co2_before/1000, total_co2_after/1000],
          color=["#8a8f8d", "#39d98a"])
ax[1].set_title("Total CO₂ Emissions (tonnes)", color="white")
ax[1].set_facecolor("#0e2a1f")
for spine in ax[1].spines.values(): spine.set_visible(False)
ax[1].tick_params(colors="white")
for i, v in enumerate([total_co2_before/1000, total_co2_after/1000]):
    ax[1].text(i, v*1.02, f"{v:,.1f}", ha="center", color="white", fontsize=10)

fig.patch.set_facecolor("#0e2a1f")  # panel background
st.pyplot(fig)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.caption("Switching from individual gas boilers to a shared district heat pump lowers total cost and emissions for the entire neighborhood.")
