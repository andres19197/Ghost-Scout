import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import plotly.graph_objects as go

st.set_page_config(
    page_title="Ghost Scout v1.0",
    page_icon="⚽",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_parquet('data/processed/df_final_scouting.parquet')
    return df

df_scouting = load_data()

st.title("⚽ Ghost Scout")
st.subheader("Sistema Inteligente de Recomendación de Futbolistas (Temporada 15/16)")
st.markdown("---")

def find_similar_players(player_name, df_source, n_neighbors=10):
    # Verificar si el jugador existe en el DataFrame
    if player_name not in df_source['player'].values:
        print(f"Jugador '{player_name}' no encontrado en el dataset.")
        return None
    #sacar la posición del jugador para luego comparar solo con jugadores de la misma posición
    info_jugador = df_source[df_source['player'] == player_name].iloc[0]
    posicion_jugador = info_jugador['posicion']
    # Filtrar el DataFrame para quedarnos solo con jugadores de la misma posición
    df_posicion = df_source[df_source['posicion'] == posicion_jugador].copy()

    # 1. Columnas que NO queremos estandarizar
    columnas_omitir = ['player', 'posicion', 'minutes_played']
    columnas_features = [col for col in df_posicion.columns if col not in columnas_omitir]

    df_features_limpias = df_posicion[columnas_features].replace([np.inf, -np.inf], np.nan).fillna(0)

    # 2. Estandarizamos solo las columnas numéricas
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_features_limpias)

    df_scaled = pd.DataFrame(X_scaled, columns=columnas_features, index=df_posicion['player'])

    # 3. Creamos el modelo de vecinos más cercanos y lo ajustamos con los datos estandarizados
    nn = NearestNeighbors(n_neighbors=n_neighbors + 1, metric='cosine')
    nn.fit(df_scaled)

    # 4. Obtenemos el vector del jugador objetivo y calculamos sus vecinos más cercanos
    vector_jugador = df_scaled.loc[[player_name]]

    distancias, indices = nn.kneighbors(vector_jugador)

    # 5. Preparamos un DataFrame con los resultados, incluyendo la posición y minutos jugados de cada vecino
    resultados = []
    for i in range(len(indices[0])):
        nombre_vecino = df_scaled.index[indices[0][i]]
       # Excluir al jugador objetivo de los resultados 
        if nombre_vecino==player_name:
            continue
            # Obtener la posición y minutos jugados del vecino desde el DataFrame original
        datos_originales = df_posicion[df_posicion['player'] == nombre_vecino].iloc[0]
        resultados.append({
            'Jugador Similar': nombre_vecino,
            'Posición': datos_originales['posicion'],
            'Minutos Jugados': datos_originales['minutes_played'],
            'Distancia Coseno': distancias[0][i]
        })



    return pd.DataFrame(resultados).sort_values(by='Distancia Coseno').head(n_neighbors), posicion_jugador

st.sidebar.header("🔍 Filtros de Scouting")

listado_jugadores = sorted(df_scouting['player'].unique())
jugador_seleccionado = st.sidebar.selectbox("Selecciona un jugador para encontrar similares", listado_jugadores)

num_cercanos = st.sidebar.slider("Número de jugadores similares a mostrar", min_value=1, max_value=10, value=5)

if jugador_seleccionado:
    # Ejecutamos el modelo al seleccionar el jugador
    df_clones, pos_jugador = find_similar_players(jugador_seleccionado, df_scouting, n_neighbors=num_cercanos)
    
    # Tarjeta visual con info del jugador buscado
    st.metric(label="Jugador Objetivo", value=jugador_seleccionado, delta=f"Posición táctica: {pos_jugador}")
    
    st.write(f"### 🎯 Top {num_cercanos} jugadores más similares en métricas p90:")
    
    # Mostramos la tabla formateada y bonita en Streamlit
    st.dataframe(
        df_clones.style.background_gradient(cmap="viridis", subset=["Distancia Coseno"]),
        use_container_width=True
    )

    st.markdown("---")
    clon_top = df_clones.iloc[0]['Jugador Similar']
    st.write(f"### 📊 Comparativa Visual de Rendimiento p90: **{jugador_seleccionado}** vs **{clon_top}**")
        
        # Definimos las métricas que van a ir en los vértices del radar
        # NOTA: Ajusta estos nombres si en tu df_final_scouting se llaman de otra forma
    metricas_radar = [col for col in [ 'Shot', 'Pass', 'Dribble', 'Ball Recovery', 'Duel', 'Pressure'] 
                          if col in df_scouting.columns]
        
        # Si las métricas por defecto no se llaman exactamente así, tomamos dinámicamente las primeras 6 numéricas
    if len(metricas_radar) < 3:
        columnas_omitir = ['player', 'posicion', 'minutes_played']
        metricas_radar = [col for col in df_scouting.columns if col not in columnas_omitir][:6]

    if len(metricas_radar) >= 3:
    # 1. Obtenemos los valores máximos de estas métricas en TODO el dataset 
    # (o solo en esa posición) para normalizar el gráfico
        max_values = df_scouting[metricas_radar].max()
    
    # 2. Extraemos datos reales
        val_obj_real = df_scouting[df_scouting['player'] == jugador_seleccionado][metricas_radar].iloc[0]
        val_clon_real = df_scouting[df_scouting['player'] == clon_top][metricas_radar].iloc[0]
    
    # 3. Normalizamos SOLO para el dibujo (valor / maximo)
    # Así el que tenga el máximo en una métrica llegará al borde del radar
        datos_objetivo = (val_obj_real / max_values).tolist()
        datos_clon = (val_clon_real / max_values).tolist()

    # 4. El cierre del radar
        metricas_radar_cierre = metricas_radar + [metricas_radar[0]]
        datos_objetivo += [datos_objetivo[0]]
        datos_clon += [datos_clon[0]]
    
    # --- Al crear la figura ---
        fig = go.Figure()

        # Listas de valores reales usando .iloc[0] para extraer por posición física sin romper el índice
        val_obj_real_lista = val_obj_real.tolist() + [val_obj_real.iloc[0]]
        val_clon_real_lista = val_clon_real.tolist() + [val_clon_real.iloc[0]]

    # IMPORTANTE: En el 'hovertemplate' mostramos el valor REAL, aunque el dibujo use el normalizado
        fig.add_trace(go.Scatterpolar(
        r=datos_objetivo,
        theta=metricas_radar_cierre,
        fill='toself',
        name=jugador_seleccionado,
        text=val_obj_real_lista, # Valores reales para el tooltip
        hovertemplate="<b>%{theta}</b><br>Valor: %{text:.2f}",
        line=dict(color='#1f77b4')
    ))
    
        fig.add_trace(go.Scatterpolar(
        r=datos_clon,
        theta=metricas_radar_cierre,
        fill='toself',
        name=clon_top,
        text=val_clon_real_lista, # Valores reales para el tooltip
        hovertemplate="<b>%{theta}</b><br>Valor: %{text:.2f}",
        line=dict(color='#ff7f0e')
    ))

    # Fijamos el rango del eje de 0 a 1 para que no se autoescala
        fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        template="plotly_dark"
    )
    
        st.plotly_chart(fig, use_container_width=True)
    else:
            st.warning("⚠️ No se han encontrado suficientes columnas numéricas disponibles para pintar el gráfico de radar.")
else:
    st.error("No se han podido calcular clones para el jugador seleccionado.")