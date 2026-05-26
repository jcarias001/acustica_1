# Acústica 1 — Calculadora de Nivel de Presión Sonora (SPL) y Suma de Emisores

Aplicación interactiva desarrollada con **Streamlit** y **Plotly** para cálculos acústicos fundamentales.

## Funcionalidades

### 🔹 Calculadora SPL (Columna izquierda)
- Ingresa un valor de presión sonora en pascales (Pa)
- Calcula el **Nivel de Presión Sonora (SPL)** usando la fórmula:
  \[
  \text{SPL} = 20 \times \log_{10}\left(\frac{P}{P_0}\right), \quad P_0 = 20\,\mu\text{Pa}
  \]
- Gráfica fija pre-calculada con escala logarítmica (Y: 0–100 Pa)
- Punto resaltado en rojo al calcular

### 🔹 Suma de Emisores (Columna derecha)
- Selecciona de **1 a 10 emisores** en el panel lateral
- Ingresa el nivel dB de cada emisor
- Calcula la **suma incoherente** usando:
  \[
  L_{\text{total}} = 10 \times \log_{10}\left(\sum_{i=1}^{n} 10^{L_i/10}\right)
  \]
- Gráfica con líneas individuales por emisor + línea combinada
- Tabla detallada con resultados acumulativos

## Requisitos

- Python 3.11 o superior
- pip

## Instalación y ejecución

```bash
# Clonar el repositorio
git clone https://github.com/jcarias001/acustica_1.git
cd acustica_1

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv

# Activar el entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

## Estructura del proyecto

```
acustica_1/
├── app.py               # Orquestador principal (UI + layout)
├── spl_calculator.py    # Módulo de cálculo SPL
├── emisores_sum.py      # Módulo de suma de emisores
├── requirements.txt     # Dependencias
├── .gitignore           # Archivos ignorados por Git
└── README.md            # Este archivo
```

## Autor

**jcarias001**
