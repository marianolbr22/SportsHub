from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Clases import Equipo
from Fachada import EliminacionEquipoFacade
from modelos.jugador_modelo import JugadorModelo
from controladores.jugador_controlador import JugadorControlador
from Clases import Jugador
from modelos.equipo_modelo import EquipoModelo
from modelos.liga_modelo import LigaModelo
from controladores.equipo_controlador import EquipoControlador
from controladores.liga_controlador import LigaControlador
from modelos.usuario_modelo import UsuarioModelo

router = APIRouter()
equipo_controlador = EquipoControlador(EquipoModelo())
liga_controlador = LigaControlador(LigaModelo())
jugador_controlador = JugadorControlador(JugadorModelo())
# Instancia la fachada SOLO una vez (mejor fuera del endpoint)
eliminacion_equipo_facade = EliminacionEquipoFacade(
    EquipoModelo(),
    UsuarioModelo()    # si todos los usuarios están en la misma colección
)

class CrearEquipoEnLigaRequest(BaseModel):
    equipo: Equipo
    id_liga: str

class IdEquipoRequest(BaseModel):
    id_equipo: str
    id_liga: str

class ActualizarDirectorRequest(BaseModel):
    id_equipo: str
    id_director: str

class ActualizarPosicionRequest(BaseModel):
    id_equipo: str
    nueva_posicion: str

class ActualizarEstadisticasRequest(BaseModel):
    id_equipo: str
    ganados: int
    perdidos: int
    empatados: int
    puntos: int

class AgregarJugadorRequest(BaseModel):
    id_equipo: str
    jugador: Jugador

class EliminarJugadorRequest(BaseModel):
    id_equipo: str
    numero: int  # Se identifica por número, como en tu modelo

# --------- Crear equipo y asociar a liga ---------
@router.post("/equipos/registrar_en_liga")
async def registrar_equipo_en_liga(request: CrearEquipoEnLigaRequest):
    id_equipo = await equipo_controlador.crear_equipo(request.equipo)
    ok = await liga_controlador.agregar_equipo(request.id_liga, id_equipo)
    if not ok:
        raise HTTPException(status_code=500, detail="No se pudo agregar el equipo a la liga")
    return {"id_equipo": id_equipo, "detalle": "Equipo creado y asignado a la liga"}

# --------- Agregar equipo existente a liga ---------
@router.post("/equipos/agregar_a_liga")
async def agregar_equipo_a_liga(request: IdEquipoRequest):
    ok = await liga_controlador.agregar_equipo(request.id_liga, request.id_equipo)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo agregar el equipo existente a la liga")
    return {"detalle": "Equipo agregado correctamente a la liga"}

# --------- Buscar equipo por id ---------
@router.get("/equipos/{id}")
async def get_equipo(id: str):
    equipo = await equipo_controlador.obtener_equipo_por_id(id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

# --------- Eliminar equipo ---------
@router.delete("/equipos/{id}")
async def eliminar_equipo(id: str):
    # Aquí puedes decidir si también lo quitas de la liga (extra)
    ok = await equipo_controlador.eliminar_equipo(id)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo eliminar el equipo")
    return {"detalle": "Equipo eliminado correctamente"}

# --------- Actualizar director ---------
@router.post("/equipos/actualizar_director")
async def actualizar_director(request: ActualizarDirectorRequest):
    ok = await equipo_controlador.asignar_director(request.id_equipo, request.id_director)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el director")
    return {"detalle": "Director actualizado correctamente"}

# --------- Actualizar posición ---------
@router.post("/equipos/actualizar_posicion")
async def actualizar_posicion(request: ActualizarPosicionRequest):
    ok = await equipo_controlador.actualizar_posicion(request.id_equipo, request.nueva_posicion)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la posición")
    return {"detalle": "Posición actualizada correctamente"}

# --------- Actualizar estadísticas ---------
@router.post("/equipos/actualizar_estadisticas")
async def actualizar_estadisticas(request: ActualizarEstadisticasRequest):
    ok = await equipo_controlador.actualizar_estadisticas(
        request.id_equipo, request.ganados, request.perdidos, request.empatados, request.puntos
    )
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudieron actualizar las estadísticas")
    return {"detalle": "Estadísticas actualizadas correctamente"}

# --------- Listar todos los equipos ---------
@router.get("/equipos")
async def listar_equipos():
    equipos = await equipo_controlador.listar_equipos()
    return equipos

# --------- Agregar jugador a equipo ---------
@router.post("/equipos/agregar_jugador")
async def agregar_jugador(request: AgregarJugadorRequest):
    ok = await jugador_controlador.agregar_jugador(request.id_equipo, request.jugador)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo agregar el jugador")
    return {"detalle": "Jugador agregado correctamente"}

# --------- Eliminar jugador de equipo ---------
@router.post("/equipos/eliminar_jugador")
async def eliminar_jugador(request: EliminarJugadorRequest):
    ok = await jugador_controlador.eliminar_jugador(request.id_equipo, request.numero)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo eliminar el jugador")
    return {"detalle": "Jugador eliminado correctamente"}

# --------- Buscar equipo por id de director ---------
@router.get("/equipos/por_director/{id_director}")
async def get_equipo_por_director(id_director: str):
    equipo = await equipo_controlador.buscar_por_director(id_director)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado para este director")
    return equipo

@router.delete("/equipos/{id}/completo")
async def eliminar_equipo_completo(id: str):
    ok = await eliminacion_equipo_facade.eliminar_equipo_completo(id)
    if not ok:
        raise HTTPException(status_code=404, detail="No se pudo eliminar el equipo o no existe")
    return {"detalle": "Equipo y referencias en favoritos eliminados correctamente"}