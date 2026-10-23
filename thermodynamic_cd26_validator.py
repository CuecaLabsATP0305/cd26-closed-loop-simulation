#!/usr/bin/env python3
"""
================================================================================
PUBLICACIÓN DEFENSIVA / DEFENSIVE PUBLICATION
================================================================================
TÍTULO: Validación termodinámica del lazo cerrado para el receptor CD26 (PDB: 1X70)

PROPÓSITO ALTRUISTA HUMANITARIO:
  Este módulo está concebido para apoyo científico, salud pública, medicina
  preventiva, emergencia clínica, bioética y comprensión del equilibrio homeostático
  del receptor CD26/DPP4. Se desarrolla como una publicación defensiva de carácter
  abierto, con finalidad de protección y diseminación de conocimiento para beneficio
  humano y sostenibilidad de sistemas fisiológicos.

RESTRICCIÓN COMERCIAL Y DE DISTRIBUCIÓN:
  Este código no otorga ni implica derechos de explotación comercial, propiedad
  industrial o uso regulatorio privado. Cualquier incorporación a productos
  comerciales, plataformas de pago, licencias de uso institucional o procesos
  regulatorios requiere la autorización explícita del titular de los derechos y no
  se presume bajo esta publicación defensiva. La difusión se orienta al bien común,
  la investigación y la ayuda humanitaria, no a la monetización de la salud.

USO ALTRUISTA HUMANITARIO:
  Se autoriza el uso académico, científico, clínico y asistencial solo cuando se
  persiga el bienestar humano, la salud pública, la investigación no comercial y la
  protección de la vida. Este módulo no debe utilizarse con fines bélicos, coercitivos,
  discriminatorios ni para explotación de personas o poblaciones.

CONDICIÓN DE SEGURIDAD Y VALIDACIÓN:
  El cálculo termodinámico presentado aquí se orienta a la validación analítica del
  lazo cerrado y no reemplaza la validación clínica ni la autoridad regulatoria.
  El criterio de espontaneidad se aplica bajo el marco de equilibrio homeostático a
  310.15 K, con una formulación de entropía cuántica y energía libre efectiva que
  sirve como referencia de diagnóstico físico-matemático.
================================================================================
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np


R_GAS_KCAL_MOL_K = 0.0019872
TEMPERATURA_HOMEOSTATICA_K = 310.15


def _prepare_density_matrix(density_matrix: np.ndarray) -> np.ndarray:
    """Normaliza una matriz de densidad y comprueba condiciones básicas."""
    rho = np.asarray(density_matrix, dtype=np.complex128)
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
        raise ValueError("La matriz de densidad debe ser cuadrada.")

    rho = 0.5 * (rho + rho.conjugate().T)
    tr = np.trace(rho)
    if abs(np.real_if_close(tr)) < 1e-12:
        raise ValueError("La traza de la matriz de densidad no puede ser cero.")
    rho = rho / np.real_if_close(tr)
    return rho


def von_neumann_entropy_bits(density_matrix: np.ndarray) -> float:
    """Calcula la entropía cuántica de von Neumann en bits."""
    rho = _prepare_density_matrix(density_matrix)
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = np.real_if_close(eigenvalues)
    eigenvalues = np.clip(np.real(eigenvalues), 0.0, 1.0)
    eigenvalues = eigenvalues[eigenvalues > 1e-12]
    if eigenvalues.size == 0:
        return 0.0
    return float(-np.sum(eigenvalues * np.log2(eigenvalues)))


def effective_entropy_change_kcal_mol_k(entropy_bits: float) -> float:
    """Convierte entropía cuántica a contribución efectiva en kcal/(mol*K)."""
    if entropy_bits < 0.0:
        raise ValueError("La entropía cuántica no puede ser negativa.")
    return float(R_GAS_KCAL_MOL_K * entropy_bits / np.log(2.0))


def effective_gibbs_free_energy_delta_g(
    delta_h_kcal_mol: float,
    entropy_bits: float,
    temperature_k: float = TEMPERATURA_HOMEOSTATICA_K,
) -> float:
    """Calcula ΔG_eff = ΔH - T·ΔS_eff para un sistema homeostático.

    Se interpreta la entropía cuántica como una contribución efectiva a la
    variación de entropía del lazo cerrado y se evalúa con el criterio de
    espontaneidad para el sistema a 310.15 K.
    """
    delta_s_effective = effective_entropy_change_kcal_mol_k(entropy_bits)
    return float(delta_h_kcal_mol - temperature_k * delta_s_effective)


def homeostatic_spontaneity_criterion(
    delta_g_eff_kcal_mol: float,
    entropy_bits: float,
    temperature_k: float = TEMPERATURA_HOMEOSTATICA_K,
) -> Dict[str, object]:
    """Aplica el criterio de espontaneidad para un sistema homeostático."""
    spontaneous = bool(delta_g_eff_kcal_mol < 0.0 and entropy_bits <= 1.0 and temperature_k > 0.0)
    status = "ESPONTÁNEO Y HOMEOSTÁTICO" if spontaneous else "NO ESPONTÁNEO / INESTABLE PARA EL LAZO HOMEOSTÁTICO"
    return {
        "temperatura_k": float(temperature_k),
        "entropia_von_neumann_bits": float(entropy_bits),
        "delta_g_efectiva_kcal_mol": float(delta_g_eff_kcal_mol),
        "criterio_espontaneidad": spontaneous,
        "estado": status,
    }


def validate_cd26_closed_loop(
    density_matrix: np.ndarray,
    delta_h_kcal_mol: float,
    receptor_id: str = "CD26 / DPP4 (PDB: 1X70)",
    temperature_k: float = TEMPERATURA_HOMEOSTATICA_K,
) -> Dict[str, object]:
    """Valida el lazo cerrado del receptor CD26 usando entropía cuántica y ΔG efectiva."""
    rho = _prepare_density_matrix(density_matrix)
    entropy_bits = von_neumann_entropy_bits(rho)
    delta_g_eff = effective_gibbs_free_energy_delta_g(
        delta_h_kcal_mol=delta_h_kcal_mol,
        entropy_bits=entropy_bits,
        temperature_k=temperature_k,
    )
    criterion = homeostatic_spontaneity_criterion(
        delta_g_eff_kcal_mol=delta_g_eff,
        entropy_bits=entropy_bits,
        temperature_k=temperature_k,
    )

    return {
        "receptor": receptor_id,
        "temperatura_k": float(temperature_k),
        "traza_rho": float(np.real_if_close(np.trace(rho))),
        "entropia_von_neumann_bits": float(entropy_bits),
        "delta_h_kcal_mol": float(delta_h_kcal_mol),
        "delta_s_efectiva_kcal_mol_k": float(effective_entropy_change_kcal_mol_k(entropy_bits)),
        "delta_g_efectiva_kcal_mol": float(delta_g_eff),
        "criterio_espontaneidad": bool(criterion["criterio_espontaneidad"]),
        "estado": str(criterion["estado"]),
    }


def default_cd26_density_matrix() -> np.ndarray:
    """Estado denso ejemplar para un lazo cerrado homeostático del receptor CD26."""
    amplitudes = np.array([
        np.sqrt(0.48),
        np.sqrt(0.27),
        np.sqrt(0.15),
        np.sqrt(0.10),
    ], dtype=np.complex128)
    return np.outer(amplitudes, amplitudes.conjugate())


if __name__ == "__main__":
    print("[CD26 THERMODYNAMIC VALIDATION] Iniciando validación del lazo cerrado para PDB: 1X70")
    rho = default_cd26_density_matrix()
    report = validate_cd26_closed_loop(
        density_matrix=rho,
        delta_h_kcal_mol=-1.8,
        receptor_id="CD26 / DPP4 (PDB: 1X70)",
        temperature_k=TEMPERATURA_HOMEOSTATICA_K,
    )
    print(report)
    print("[CD26 THERMODYNAMIC VALIDATION] Fin del análisis termodinámico.")

