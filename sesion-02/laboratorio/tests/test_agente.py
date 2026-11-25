import json

from conftest import LLMFalso, llamada, respuesta


def calculadora(mod, **kw):
    return mod.Herramienta("sumar", "Suma dos números", lambda a, b: float(a) + float(b),
                           {"a": "primer número", "b": "segundo número"}, ["a", "b"], **kw)


# ---------- TODO 1: ejecutar_herramienta ----------

def test_herramienta_ok(mod):
    ag = mod.Agente(LLMFalso([]), "m", [calculadora(mod)])
    assert ag.ejecutar_herramienta("sumar", '{"a": "2", "b": "3"}') == "5.0"


def test_herramienta_desconocida(mod):
    ag = mod.Agente(LLMFalso([]), "m", [calculadora(mod)])
    assert ag.ejecutar_herramienta("borrar_todo", "{}") == "ERROR: herramienta desconocida: borrar_todo"


def test_argumentos_invalidos(mod):
    ag = mod.Agente(LLMFalso([]), "m", [calculadora(mod)])
    assert ag.ejecutar_herramienta("sumar", "a=2, b=3") == "ERROR: argumentos inválidos"


def test_excepcion_se_vuelve_observacion(mod):
    ag = mod.Agente(LLMFalso([]), "m", [calculadora(mod)])
    obs = ag.ejecutar_herramienta("sumar", '{"a": "dos", "b": "3"}')
    assert obs.startswith("ERROR: ValueError")


def test_falta_argumento_se_vuelve_observacion(mod):
    ag = mod.Agente(LLMFalso([]), "m", [calculadora(mod)])
    assert ag.ejecutar_herramienta("sumar", '{"a": "2"}').startswith("ERROR: TypeError")


def test_resultado_en_json_sin_escapar_tildes(mod):
    h = mod.Herramienta("saludo", "Saluda", lambda: {"mensaje": "Hola, ¿cómo vas?"})
    ag = mod.Agente(LLMFalso([]), "m", [h])
    assert json.loads(ag.ejecutar_herramienta("saludo", "")) == {"mensaje": "Hola, ¿cómo vas?"}
    assert "cómo" in ag.ejecutar_herramienta("saludo", "")


def test_aprobacion_denegada_no_ejecuta(mod):
    llamados = []
    h = mod.Herramienta("borrar", "Borra un archivo", lambda ruta: llamados.append(ruta), {"ruta": "archivo"},
                        ["ruta"], requiere_aprobacion=True)
    ag = mod.Agente(LLMFalso([]), "m", [h])
    assert ag.ejecutar_herramienta("borrar", '{"ruta": "x.txt"}') == "DENEGADO: la persona no aprobó borrar"
    assert llamados == []


def test_aprobacion_concedida_ejecuta_y_recibe_argumentos(mod):
    vistos = []
    h = calculadora(mod, requiere_aprobacion=True)
    ag = mod.Agente(LLMFalso([]), "m", [h], aprobador=lambda n, a: vistos.append((n, a)) or True)
    assert ag.ejecutar_herramienta("sumar", '{"a": "1", "b": "1"}') == "2.0"
    assert vistos == [("sumar", {"a": "1", "b": "1"})]


# ---------- TODOs 2 y 3: el ciclo ----------

def test_respuesta_directa_sin_herramientas(mod):
    llm = LLMFalso([respuesta("Hola")])
    r = mod.Agente(llm, "m", [calculadora(mod)]).ejecutar("saluda")
    assert (r.respuesta, r.pasos, r.traza, r.terminado) == ("Hola", 1, [], True)


def test_envia_sistema_pregunta_y_esquemas(mod):
    llm = LLMFalso([respuesta("ok")])
    mod.Agente(llm, "modelo-x", [calculadora(mod)], sistema="Eres útil").ejecutar("¿2+3?")
    primero = llm.recibido[0]
    assert primero["messages"] == [{"role": "system", "content": "Eres útil"}, {"role": "user", "content": "¿2+3?"}]
    assert primero["tools"][0]["function"]["name"] == "sumar"


def test_usa_herramienta_y_responde(mod):
    llm = LLMFalso([respuesta(None, [llamada("sumar", {"a": "2", "b": "3"})]), respuesta("Son 5")])
    r = mod.Agente(llm, "m", [calculadora(mod)]).ejecutar("¿2+3?")
    assert r.respuesta == "Son 5" and r.pasos == 2 and r.terminado
    assert r.traza == [{"herramienta": "sumar", "argumentos": '{"a": "2", "b": "3"}', "observacion": "5.0"}]


def test_la_observacion_vuelve_al_modelo(mod):
    llm = LLMFalso([respuesta(None, [llamada("sumar", {"a": "2", "b": "3"}, "id-7")]), respuesta("Son 5")])
    mod.Agente(llm, "m", [calculadora(mod)]).ejecutar("¿2+3?")
    segundo = llm.recibido[1]["messages"]
    assert segundo[-2]["role"] == "assistant" and segundo[-2]["tool_calls"][0]["id"] == "id-7"
    assert segundo[-1] == {"role": "tool", "tool_call_id": "id-7", "content": "5.0"}


def test_varias_herramientas_en_un_paso(mod):
    llm = LLMFalso([respuesta(None, [llamada("sumar", {"a": "1", "b": "1"}, "a"),
                                     llamada("sumar", {"a": "2", "b": "2"}, "b")]), respuesta("2 y 4")])
    r = mod.Agente(llm, "m", [calculadora(mod)]).ejecutar("dos sumas")
    assert [t["observacion"] for t in r.traza] == ["2.0", "4.0"]
    assert [m["tool_call_id"] for m in llm.recibido[1]["messages"] if m["role"] == "tool"] == ["a", "b"]


def test_error_de_herramienta_no_detiene_el_ciclo(mod):
    llm = LLMFalso([respuesta(None, [llamada("inexistente", {})]), respuesta("No pude")])
    r = mod.Agente(llm, "m", [calculadora(mod)]).ejecutar("x")
    assert r.terminado and r.traza[0]["observacion"].startswith("ERROR: herramienta desconocida")


def test_max_pasos_detiene_un_agente_en_bucle(mod):
    bucle = [respuesta(None, [llamada("sumar", {"a": "1", "b": "1"}, f"c{i}")]) for i in range(10)]
    llm = LLMFalso(bucle)
    r = mod.Agente(llm, "m", [calculadora(mod)], max_pasos=3).ejecutar("x")
    assert not r.terminado and r.pasos == 3 and len(llm.recibido) == 3 and len(r.traza) == 3
