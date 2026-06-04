# ⚽ Ghost Scout: Sistema Inteligente de Recomendación de Futbolistas

**Ghost Scout** es una aplicación web interactiva de analítica deportiva orientada al scouting de fútbol. El sistema procesa datos de eventos p90 para identificar perfiles estadísticamente similares ("clones") a un jugador objetivo, utilizando algoritmos de aprendizaje no supervisado.

---

## 🚀 Características Clave

* **Filtrado Posicional Dinámico:** El sistema restringe las comparaciones únicamente a futbolistas que operan en el mismo rol táctico.
* **Modelo K-NN (Algoritmo de Vecinos Más Cercanos):** Implementación de similitud basada en la **Distancia Coseno** sobre métricas de rendimiento normalizadas (`StandardScaler`).
* **Visualización de Rendimiento Multivariable:** Gráfico de radar dinámico e interactivo integrado con Plotly para comparar métricas p90 clave (goles, asistencias, pases, regates, recuperaciones).
* **Interfaz de Usuario de Alta Velocidad:** Implementada con Streamlit y optimizada mediante sistemas de almacenamiento en caché (`@st.cache_data`).

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Procesamiento de Datos:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (`NearestNeighbors`, `StandardScaler`)
* **Visualización:** Plotly, Streamlit
* **Fuente de Datos:** StatsBomb API (Temporada 15/16)

---

## 📦 Instalación y Uso Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/pryct_llm_jogabonito.git](https://github.com/TU_USUARIO/Ghost-Scout.git)
   cd pryct_llm_jogabonito

2. **Crear y activar el entorno virtual::**
    python -m venv .venv
    # En Windows (tu entorno):
    .venv\Scripts\activate
    # En Mac/Linux:
    source .venv/bin/activate

3. **Instalar dependencias*::**
    pip install -r requirements.txt

4. **Ejecutar la aplicacion web::**
    streamlit run app.py