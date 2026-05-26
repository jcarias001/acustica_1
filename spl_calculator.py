"""
Módulo de cálculo de Nivel de Presión Sonora (SPL)
Fórmula: SPL = 20 × log₁₀(P / P₀), donde P₀ = 20 μPa (2×10⁻⁵ Pa)
"""

import numpy as np

# Constante acústica: presión de referencia en Pascales
P0 = 2e-5  # 20 μPa


def calc_spl(valor_entrada):
    """
    Calcula el SPL (dB) usando la fórmula acústica:
        SPL = 20 × log₁₀(valor_entrada / P₀)
    donde P₀ = 20 μPa (2×10⁻⁵ Pa).

    Acepta escalar o array de numpy.
    Para valor_entrada <= 0, retorna -inf.
    """
    v = np.asarray(valor_entrada, dtype=float)
    if v.ndim == 0:
        if v <= 0:
            return -float("inf")
        return 20.0 * np.log10(v / P0)
    # Array
    mascara = v > 0
    resultado = np.full_like(v, -float("inf"))
    resultado[mascara] = 20.0 * np.log10(v[mascara] / P0)
    return resultado


def generar_curva_fija():
    """
    Genera la curva fija de la gráfica con alta resolución.
    Y (eje vertical):   valores de entrada de 0 a 100 (2000 puntos)
    X (eje horizontal): SPL resultante = 20 × log₁₀(Y / P₀)
    """
    y_vals = np.linspace(0, 100, 2000)
    spl_array = calc_spl(y_vals)
    spl_array[0] = 0.0  # reemplazar -inf del punto 0 por 0 dB
    return y_vals, spl_array
