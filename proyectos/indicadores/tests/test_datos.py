from indicadores.datos import cargar_calificaciones, cargar_matriculas


def test_carga_calificaciones():
    cal = cargar_calificaciones()
    assert cal and all(0 <= c.nota_final <= 5 for c in cal)


def test_carga_matriculas():
    mat = cargar_matriculas()
    assert {m.estado for m in mat} <= {"matriculado", "retirado", "graduado"}
