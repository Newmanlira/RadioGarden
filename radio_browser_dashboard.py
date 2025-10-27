import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(
    page_title="🌎 Rádio Garden Mundial",
    layout="wide",
)

@st.cache_data(show_spinner=False)
def get_stations():
    """Baixa dados das rádios reais do Radio Browser"""
    url = "https://de1.api.radio-browser.info/json/stations"
    response = requests.get(url, timeout=30)
    data = response.json()
    df = pd.DataFrame(data)
    return df

st.title("🌎 Rádio Garden Mundial (via Radio Browser)")
st.markdown("Explore rádios de todo o mundo com base em dados reais!")

# --------------------------
# Download
# --------------------------
with st.spinner("🔄 Carregando lista de rádios..."):
    df = get_stations()

# --------------------------
# Filtros básicos
# --------------------------
country_list = sorted(df["country"].dropna().unique().tolist())
language_list = sorted(df["language"].dropna().unique().tolist())

col1, col2 = st.columns(2)
with col1:
    country = st.selectbox("🌍 País", ["Todos"] + country_list)
with col2:
    language = st.selectbox("🗣️ Idioma", ["Todos"] + language_list)

filtered_df = df.copy()
if country != "Todos":
    filtered_df = filtered_df[filtered_df["country"] == country]
if language != "Todos":
    filtered_df = filtered_df[filtered_df["language"] == language]

st.success(f"🎧 {len(filtered_df)} rádios encontradas!")

# --------------------------
# Mapa interativo
# --------------------------
if not filtered_df.empty:
    # Evita travar o mapa
    sample_df = filtered_df.dropna(subset=["geo_lat", "geo_long"]).sample(min(1000, len(filtered_df)))

    fig = px.scatter_mapbox(
        sample_df,
        lat="geo_lat",
        lon="geo_long",
        hover_name="name",
        hover_data={"country": True, "language": True, "state": True},
        color="country",
        zoom=1,
        height=700,
    )
    fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nenhuma rádio encontrada com esses filtros.")

# --------------------------
# Tabela de rádios
# --------------------------
st.subheader("📻 Lista de rádios")

selected_radio = st.selectbox(
    "🎶 Selecione uma rádio para ouvir:",
    filtered_df["name"].sort_values().tolist() if not filtered_df.empty else [],
)

if selected_radio:
    radio_url = filtered_df.loc[filtered_df["name"] == selected_radio, "url_resolved"].values[0]
    st.audio(radio_url, format="audio/mp3")

st.dataframe(
    filtered_df[["name", "country", "state", "language", "bitrate", "url_resolved"]]
    .sort_values("name")
    .reset_index(drop=True),
    use_container_width=True,
    height=500,
)
