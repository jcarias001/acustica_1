"""
Módulo de suma de emisores acústicos.
Fórmula de suma de dB (fuentes incoherentes):
    L_total = 10 × log₁₀( ∑ 10^(Lᵢ / 10) )
"""

import numpy as np


def sumar_dB(valores: list[float]) -> float:
    """
    Suma niveles de presión sonora en dB de múltiples fuentes.

    Para fuentes incoherentes (caso general):
        L_total = 10 × log₁₀( Σ 10^(Lᵢ / 10) )

    Parameters
    ----------
    valores : list[float]
        Lista de niveles dB de cada emisor.

    Returns
    -------
    float
        Nivel total combinado en dB.
    """
    if not valores:
        return 0.0
    suma = sum(10.0 ** (v / 10.0) for v in valores)
    return float(10.0 * np.log10(suma))


def generar_datos_grafica(valores: list[float]) -> dict:
    """
    Genera los datos para la gráfica de emisores.

    Parameters
    ----------
    valores : list[float]
        Lista de niveles dB de cada emisor (1 a N).

    Returns
    -------
    dict with keys:
        x : list[int]
            Índices de emisores (1, 2, ..., N).
        individuales : list[tuple[str, list[float]]]
            Lista de (nombre_emisor, valores_constantes_por_emisor).
        combinada : list[float]
            Valores de la suma acumulativa para cada paso.
        total : float
            Nivel total combinado de todos los emisores.
    """
    n = len(valores)
    if n == 0:
        return {"x": [], "individuales": [], "combinada": [], "total": 0.0}

    x = list(range(1, n + 1))

    # Cada emisor: línea horizontal constante a su valor dB
    individuales = []
    for i, v in enumerate(valores):
        individuales.append((f"Emisor {i+1} ({v:.1f} dB)", [v] * n))

    # Combinada: suma acumulativa (cuánto se obtiene al añadir cada emisor)
    combinada = []
    for i in range(1, n + 1):
        total_parcial = sumar_dB(valores[:i])
        combinada.append(total_parcial)

    total = sumar_dB(valores)

    return {
        "x": x,
        "individuales": individuales,
        "combinada": combinada,
        "total": total,
    }
