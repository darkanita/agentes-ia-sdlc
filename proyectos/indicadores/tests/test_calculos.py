import pytest

from indicadores.calculos import aprobo, promedio_ponderado, tasa_aprobacion, tasa_desercion
from indicadores.datos import Calificacion, Matricula


def cal(nota, asignatura="Cálculo I", periodo="2026-1", programa="P", codigo="E1", creditos=4):
    return Calificacion(periodo, programa, asignatura, codigo, creditos, nota)


def test_aprueba_con_nota_alta():
    assert aprobo(4.5)


def test_reprueba_con_nota_baja():
    assert not aprobo(2.9)


def test_tasa_aprobacion():
    datos = [cal(4.0, codigo="E1"), cal(2.0, codigo="E2"), cal(3.5, codigo="E3"), cal(1.0, codigo="E4")]
    assert tasa_aprobacion(datos, "Cálculo I", "2026-1") == 0.5


def test_tasa_aprobacion_por_programa():
    datos = [cal(4.0, programa="A"), cal(2.0, programa="B")]
    assert tasa_aprobacion(datos, "Cálculo I", "2026-1", programa="A") == 1.0


def test_tasa_aprobacion_sin_datos():
    with pytest.raises(ValueError):
        tasa_aprobacion([], "Cálculo I", "2026-1")


def test_promedio_ponderado():
    datos = [cal(4.0, creditos=4), cal(3.0, asignatura="Ecología", creditos=2)]
    assert promedio_ponderado(datos, "E1") == 3.67


def mat(codigo, periodo, estado, cohorte="2025-2", programa="P"):
    return Matricula(codigo, programa, cohorte, periodo, estado)


def test_desercion_cohorte_nueva():
    datos = [mat("E1", "2025-2", "matriculado"), mat("E1", "2026-1", "matriculado"),
             mat("E2", "2025-2", "matriculado"), mat("E2", "2026-1", "retirado")]
    assert tasa_desercion(datos, "P", "2025-2", "2026-1") == 0.5
