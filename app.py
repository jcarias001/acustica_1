"""
Aplicación Streamlit + Plotly - Calculadora SPL y Suma de Emisores Acústicos
Orquestador que coordina los módulos spl_calculator y emisores_sum.
Usa st.session_state para preservar ambos estados independientemente.
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from spl_calculator import calc_spl, generar_curva_fija, P0
from emisores_sum import sumar_dB, generar_datos_grafica

# ─── Inicializar session_state ───────────────────────────────────────────────

if "spl_calculado" not in st.session_state:
    st.session_state.spl_calculado = False
    st.session_state.spl_input = 20.0

if "emisores_calculado" not in st.session_state:
    st.session_state.emisores_calculado = False
    st.session_state.valores_emisores = []
    st.session_state.num_emisores = 3

# ─── Configuración de página ─────────────────────────────────────────────────

st.set_page_config(
    page_title="Calculadora SPL y Emisores Acústicos",
    page_icon="🔊",
    layout="wide",
)

# ─── Título principal ────────────────────────────────────────────────────────

st.title("🔊 Calculadora Acústica")
st.markdown("---")

# ─── Panel lateral ───────────────────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Controles")

    # ── Sección: SPL ──────────────────────────────────────────────────────
    st.subheader("📈 Calculadora SPL")

    with st.expander("📐 Fórmula acústica", expanded=False):
        st.markdown(
            r"""
            **SPL = 20 × log₁₀( P / P₀ )**

            Donde:
            - **P** = Pa de entrada (la presión sonora que quieres convertir a dB)
            - **P₀** = 20 μPa = **2×10⁻⁵ Pa**

            **Ejemplo:**
            - Entrada = 20 → SPL = 20 × log₁₀(20 / 2×10⁻⁵)
            - SPL = 20 × log₁₀(1,000,000) = **120 dB SPL**
            """
        )

    spl_input = st.number_input(
        "🎤 Pa de entrada",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.spl_input,
        step=0.00001,
        format="%.5f",
        key="spl_number_input",
        help="Valor usado como P en SPL = 20·log₁₀(P/P₀). Acepta hasta 5 decimales.",
    )

    if st.button("🔍 Calcular SPL", type="primary", use_container_width=True):
        st.session_state.spl_calculado = True
        st.session_state.spl_input = spl_input

    st.divider()

    # ── Sección: Emisores ─────────────────────────────────────────────────
    st.subheader("🔊 Suma de Emisores")

    with st.expander("📐 Fórmula de suma", expanded=False):
        st.markdown(
            r"""
            **L_total = 10 × log₁₀( Σ 10^(Lᵢ / 10) )**

            Donde:
            - **Lᵢ** = nivel dB de cada emisor
            - La suma asume fuentes **incoherentes**
            """
        )

    num_emisores = st.selectbox(
        "Número de emisores",
        options=list(range(1, 11)),
        index=st.session_state.num_emisores - 1,
        key="num_emisores_select",
        help="Selecciona cuántos emisores deseas sumar.",
    )

    # Generar dinámicamente los campos de entrada para cada emisor
    valores_emisores = []
    for i in range(num_emisores):
        # Valor por defecto según sesión almacenada o valores iniciales
        default_val = 80.0
        if st.session_state.emisores_calculado and i < len(st.session_state.valores_emisores):
            default_val = st.session_state.valores_emisores[i]
        elif i == 0:
            default_val = 80.0
        elif i == 1:
            default_val = 85.0
        elif i == 2:
            default_val = 90.0

        v = st.number_input(
            f"Emisor {i+1} (dB)",
            min_value=0.0,
            max_value=200.0,
            value=default_val,
            step=0.1,
            format="%.1f",
            key=f"emisor_{i}",
        )
        valores_emisores.append(v)

    if st.button("🔊 Calcular Emisores", type="primary", use_container_width=True):
        st.session_state.emisores_calculado = True
        st.session_state.valores_emisores = valores_emisores
        st.session_state.num_emisores = num_emisores

    st.divider()
    st.caption("Desarrollado con Streamlit + Plotly")


# ─── Área principal: 2 columnas ─────────────────────────────────────────────

col_izq, col_der = st.columns(2, gap="large")

# =============================================================================
# COLUMNA IZQUIERDA ── Calculadora SPL
# =============================================================================

with col_izq:
    st.header("📈 Nivel de Presión Sonora (SPL)")

    # Datos fijos de la curva
    y_vals, x_vals = generar_curva_fija()

    # ── Crear gráfica SPL ─────────────────────────────────────────────────
    fig_spl = go.Figure()

    # Curva principal
    fig_spl.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            name="SPL = 20·log₁₀(P / P₀)",
            line=dict(color="#1E88E5", width=3),
            hovertemplate=(
                "<b>Entrada:</b> %{y:.5f}<br>"
                "<b>SPL:</b> %{x:.2f} dB<br>"
                "<extra></extra>"
            ),
        )
    )

    # Punto destacado (solo si hay cálculo guardado en session_state)
    if st.session_state.spl_calculado:
        spl_val = calc_spl(st.session_state.spl_input)
        fig_spl.add_trace(
            go.Scatter(
                x=[spl_val],
                y=[st.session_state.spl_input],
                mode="markers",
                name=f"Entrada: {st.session_state.spl_input:.5f} → {spl_val:.2f} dB",
                marker=dict(
                    color="#E53935",
                    size=22,
                    symbol="circle",
                    line=dict(color="#B71C1C", width=4),
                ),
                hovertemplate=(
                    f"<b>Entrada:</b> {st.session_state.spl_input:.5f}<br>"
                    f"<b>SPL:</b> {spl_val:.2f} dB<br>"
                    "<extra></extra>"
                ),
            )
        )

    # Referencia y=20
    fig_spl.add_trace(
        go.Scatter(
            x=[-5, 200],
            y=[20, 20],
            mode="lines",
            line=dict(color="#BDBDBD", width=1, dash="dash"),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    fig_spl.update_layout(
        title="<b>Cantidad de SPL según entrada</b>",
        xaxis=dict(
            title="dB SPL de salida",
            range=[-5, 145],
            dtick=10,
            gridcolor="#E0E0E0",
            zerolinecolor="#BDBDBD",
        ),
        yaxis=dict(
            title="Pa de entrada",
            range=[-5, 105],
            dtick=10,
            gridcolor="#E0E0E0",
            zerolinecolor="#BDBDBD",
        ),
        legend=dict(
            x=0.02, y=0.98,
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#BDBDBD",
            borderwidth=1,
        ),
        hovermode="closest",
        template="plotly_white",
        margin=dict(l=40, r=40, t=40, b=40),
        height=400,
    )

    st.plotly_chart(fig_spl, use_container_width=True)

    # ── Resultados SPL ────────────────────────────────────────────────────
    if st.session_state.spl_calculado:
        spl_val = calc_spl(st.session_state.spl_input)
        relacion = st.session_state.spl_input / P0 if st.session_state.spl_input > 0 else 0

        st.markdown("#### 📊 Resultados SPL")

        col_spl1, col_spl2 = st.columns(2)

        with col_spl1:
            st.metric(
                label="🎯 SPL de Salida",
                value=f"{spl_val:.2f} dB SPL",
                delta=f"Entrada: {st.session_state.spl_input:.5f}",
            )

        with col_spl2:
            st.metric(
                label="📊 P / P₀",
                value=f"{relacion:,.2f}",
                delta=f"{np.log10(relacion):.2f} órdenes de magnitud" if relacion > 0 else "",
            )

        # Categoría cualitativa
        if spl_val < 30:
            categoria, color = "🔇 Muy bajo", "#4CAF50"
        elif spl_val < 60:
            categoria, color = "🔈 Moderado", "#FFC107"
        elif spl_val < 80:
            categoria, color = "🔉 Alto", "#FF9800"
        elif spl_val < 100:
            categoria, color = "🔊 Muy alto", "#FF5722"
        else:
            categoria, color = "🚨 Peligroso", "#E53935"

        st.markdown(
            f"""
            <div style="
                background-color: {color}20;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 12px;
                text-align: center;
            ">
                <span style="font-size: 24px; font-weight: bold; color: {color};">
                    {categoria}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Presiona **Calcular SPL** en el panel lateral para ver resultados.")

# =============================================================================
# COLUMNA DERECHA ── Suma de Emisores
# =============================================================================

with col_der:
    st.header("🔊 Suma de Emisores Acústicos")

    # ── Crear gráfica de emisores ─────────────────────────────────────────
    fig_em = go.Figure()

    if st.session_state.emisores_calculado and st.session_state.valores_emisores:
        datos = generar_datos_grafica(st.session_state.valores_emisores)
        x = datos["x"]
        n = len(x)

        colores_emisores = [
            "#1E88E5", "#43A047", "#FDD835", "#FB8C00",
            "#8E24AA", "#00ACC1", "#FF5252", "#6D4C41",
            "#546E7A", "#A1887F",
        ]

        # Línea de cada emisor (constante horizontal)
        for idx, (nombre, vals_y) in enumerate(datos["individuales"]):
            fig_em.add_trace(
                go.Scatter(
                    x=x,
                    y=vals_y,
                    mode="lines+markers",
                    name=nombre,
                    line=dict(
                        color=colores_emisores[idx % len(colores_emisores)],
                        width=1.5,
                        dash="dot",
                    ),
                    marker=dict(size=6),
                    hovertemplate=(
                        f"<b>{nombre}</b><br>"
                        "Nivel: %{y:.1f} dB<br>"
                        "<extra></extra>"
                    ),
                )
            )

        # Línea combinada (suma acumulativa)
        fig_em.add_trace(
            go.Scatter(
                x=x,
                y=datos["combinada"],
                mode="lines+markers",
                name=f"Combinado: {datos['total']:.2f} dB",
                line=dict(color="#E53935", width=4),
                marker=dict(size=10, symbol="diamond"),
                hovertemplate=(
                    "<b>Combinado</b><br>"
                    "Emisores: %{x}<br>"
                    "Total: %{y:.2f} dB<br>"
                    "<extra></extra>"
                ),
            )
        )

        fig_em.update_layout(
            title=f"<b>Emisores: combinación total = {datos['total']:.2f} dB</b>",
            xaxis=dict(
                title="Número de emisores",
                tickmode="array",
                tickvals=x,
                ticktext=[str(v) for v in x],
                range=[0.5, n + 0.5],
                gridcolor="#E0E0E0",
                zerolinecolor="#BDBDBD",
            ),
            yaxis=dict(
                title="Nivel (dB)",
                gridcolor="#E0E0E0",
                zerolinecolor="#BDBDBD",
            ),
            legend=dict(
                x=0.02, y=0.98,
                bgcolor="rgba(255,255,255,0.85)",
                bordercolor="#BDBDBD",
                borderwidth=1,
                font=dict(size=10),
            ),
            hovermode="closest",
            template="plotly_white",
            margin=dict(l=40, r=40, t=50, b=40),
            height=400,
        )
    else:
        fig_em.add_trace(
            go.Scatter(
                x=[], y=[],
                mode="lines",
                name="Sin datos",
                line=dict(color="#BDBDBD", width=2),
            )
        )
        fig_em.update_layout(
            title="<b>Selecciona emisores y presiona Calcular</b>",
            xaxis=dict(title="Número de emisores", range=[0.5, 3.5]),
            yaxis=dict(title="Nivel (dB)", range=[0, 120]),
            template="plotly_white",
            height=400,
        )
        fig_em.add_annotation(
            text="👈 Configura los emisores en el panel lateral<br>y presiona <b>Calcular Emisores</b>",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="#9E9E9E"),
        )

    st.plotly_chart(fig_em, use_container_width=True)

    # ── Resultados de emisores ─────────────────────────────────────────────
    if st.session_state.emisores_calculado and st.session_state.valores_emisores:
        datos = generar_datos_grafica(st.session_state.valores_emisores)

        st.markdown("#### 📊 Resultados de Emisores")

        col_em1, col_em2 = st.columns(2)

        with col_em1:
            st.metric(
                label="🎯 Total Combinado",
                value=f"{datos['total']:.2f} dB",
                delta=f"{datos['total'] - max(st.session_state.valores_emisores):.2f} dB sobre el mayor",
            )

        with col_em2:
            st.metric(
                label="📊 Emisores",
                value=f"{st.session_state.num_emisores}",
                delta=f"{' + '.join(f'{v:.1f}' for v in st.session_state.valores_emisores)} dB",
            )

        # Tabla resumen
        st.markdown("##### 📋 Detalle por emisor")
        detalle = [
            {"Emisor": f"Emisor {i+1}", "dB": f"{v:.1f} dB"}
            for i, v in enumerate(st.session_state.valores_emisores)
        ]
        st.dataframe(detalle, use_container_width=True, hide_index=True)

    else:
        st.info("Presiona **Calcular Emisores** en el panel lateral para ver resultados.")
