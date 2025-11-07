from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Clases import Partido
from Fachada import ConsultasAvanzadasFacade
from modelos.liga_modelo import LigaModelo
from modelos.partido_modelo import PartidoModelo
from controladores.partido_controlador import PartidoControlador
from typing import Dict, List
from modelos.reglas_modelo import ReglasModelo
from aspectos.logging import log_action  # <--- IMPORTAR DECORADOR

router = APIRouter()
partido_controlador = PartidoControlador(PartidoModelo())
consultas_facade = ConsultasAvanzadasFacade(
    LigaModelo(),
    ReglasModelo()
)

class ArbitroRequest(BaseModel):
    id_partido: str
    id_arbitro: str

class ResultadoRequest(BaseModel):
    id_partido: str
    resultado: Dict[str, int]

class EventosRequest(BaseModel):
    id_partido: str
    eventos: Dict[int, List[str]]  # Cambia List[str]

class EquipoRequest(BaseModel):
    id_equipo: str

# --------- Crear partido ---------
@router.post("/partidos")
@log_action(action_name="CREAR_PARTIDO")
async def crear_partido(partido: Partido):
    id_nuevo = await partido_controlador.crear_partido(partido)
    return {"id": id_nuevo}

# --------- Buscar partido por id ---------
@router.get("/partidos/{id}")
async def get_partido(id: str):
    partido = await partido_controlador.obtener_partido_por_id(id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

# --------- Agregar árbitro a partido ---------
@router.post("/partidos/agregar_arbitro")
@log_action(action_name="PARTIDO_AGREGAR_ARBITRO")
async def agregar_arbitro(request: ArbitroRequest):
    ok = await partido_controlador.agregar_arbitro(request.id_partido, request.id_arbitro)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo agregar el árbitro")
    return {"detalle": "Árbitro agregado correctamente"}

# --------- Eliminar árbitro de partido ---------
@router.post("/partidos/eliminar_arbitro")
@log_action(action_name="PARTIDO_ELIMINAR_ARBITRO")
async def eliminar_arbitro(request: BaseModel):
    id_partido = request.id_partido
    ok = await partido_controlador.eliminar_arbitro(id_partido)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo eliminar el árbitro")
    return {"detalle": "Árbitro eliminado correctamente"}

# --------- Actualizar resultado ---------
@router.post("/partidos/actualizar_resultado")
@log_action(action_name="PARTIDO_ACTUALIZAR_RESULTADO")
async def actualizar_resultado(request: ResultadoRequest):
    ok = await partido_controlador.actualizar_resultado(request.id_partido, request.resultado)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el resultado")
    return {"detalle": "Resultado actualizado correctamente"}

# --------- Actualizar eventos/faltas ---------
@router.post("/partidos/actualizar_eventos")
@log_action(action_name="PARTIDO_ACTUALIZAR_EVENTOS")
async def actualizar_eventos(request: EventosRequest):
    ok = await partido_controlador.actualizar_faltas(request.id_partido, request.eventos)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudieron actualizar los eventos")
    return {"detalle": "Eventos actualizados correctamente"}

# --------- Listar todos los partidos ---------
@router.get("/partidos")
async def listar_partidos():
    partidos = await partido_controlador.listar_partidos()
    return partidos

# --------- Listar partidos por equipo ---------
@router.get("/partidos/por_equipo/{id_equipo}")
async def partidos_por_equipo(id_equipo: str):
    partidos = await partido_controlador.buscar_partidos_por_equipo(id_equipo)
    return partidos

# --------- Listar partidos por arbitro ---------
@router.get("/partidos/por_arbitro/{id_arbitro}")
async def partidos_por_arbitro(id_arbitro: str):
    partidos = await partido_controlador.buscar_partidos_por_arbitro(id_arbitro)
    return partidos

@router.delete("/partidos/{id}")
@log_action(action_name="ELIMINAR_PARTIDO")
async def eliminar_liga(id: str):
    ok = await partido_controlador.eliminar_partido(id)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo eliminar partido")
    return {"detalle": "Partido eliminado correctamente"}

@router.put("/partidos/{id}")
@log_action(action_name="ACTUALIZAR_PARTIDO_COMPLETO")
async def actualizar_partido_completo(id: str, partido: Partido):
    ok = await partido_controlador.actualizar_partido_completo(id, partido)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el partido")
    return {"detalle": "Partido actualizado correctamente"}

@router.get("/partidos/{id}/reglas")
async def obtener_reglas_por_partido(id: str):
    reglas = await consultas_facade.obtener_reglas_por_partido(id)
    if not reglas:
        raise HTTPException(status_code=404, detail="No se encontraron las reglas para este partido")
    return reglas