from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Clases import Liga, Director, Arbitro
from Fachada import RegistroLigaFacade, EliminacionLigaFacade
from modelos.admin_modelo import AdminModelo
from modelos.equipo_modelo import EquipoModelo
from modelos.liga_modelo import LigaModelo
from modelos.director_modelo import DirectorModelo
from modelos.arbitro_modelo import ArbitroModelo
from controladores.liga_controlador import LigaControlador
from controladores.director_controlador import DirectorControlador
from controladores.arbitro_controlador import ArbitroControlador
from modelos.partido_modelo import PartidoModelo
from modelos.usuario_modelo import UsuarioModelo
from routes.equipo import equipo_controlador
from aspectos.logging import log_action  # <--- IMPORTAR DECORADOR

router = APIRouter()
liga_controlador = LigaControlador(LigaModelo())
director_controlador = DirectorControlador(DirectorModelo())
arbitro_controlador = ArbitroControlador(ArbitroModelo())
# Instancia la fachada pasando los controladores ya existentes
registro_liga_facade = RegistroLigaFacade(
    director_controlador,
    arbitro_controlador,
    liga_controlador
)
eliminacion_liga_facade = EliminacionLigaFacade(
    LigaModelo(),
    EquipoModelo(),
    PartidoModelo(),
    ArbitroModelo(),
    DirectorModelo(),
    UsuarioModelo(),
    AdminModelo()
)


class IdRequest(BaseModel):
    id_liga: str
    id_item: str  # para árbitro, director, partido, equipo según el endpoint

class FaseRequest(BaseModel):
    id_liga: str
    nueva_fase: str

class CrearDirectorEnLigaRequest(BaseModel):
    director: Director
    id_liga: str

class CrearArbitroEnLigaRequest(BaseModel):
    arbitro: Arbitro
    id_liga: str

# --------- Crear liga ---------
@router.post("/ligas")
@log_action(action_name="CREAR_LIGA")
async def crear_liga(liga: Liga):
    id_nueva = await liga_controlador.crear_liga(liga)
    return {"id": id_nueva}

# --------- Buscar liga por id ---------
@router.get("/ligas/{id}")
async def get_liga(id: str):
    liga = await liga_controlador.obtener_liga_por_id(id)
    if not liga:
        raise HTTPException(status_code=404, detail="Liga no encontrada")
    return liga

# --------- Eliminar liga ---------
@router.delete("/ligas/{id}")
@log_action(action_name="ELIMINAR_LIGA")
async def eliminar_liga(id: str):
    ok = await liga_controlador.eliminar_liga(id)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo eliminar la liga")
    return {"detalle": "Liga eliminada correctamente"}

# --------- Agregar/eliminar árbitro ---------
@router.post("/ligas/agregar_arbitro")
@log_action(action_name="LIGA_AGREGAR_ARBITRO")
async def agregar_arbitro(req: IdRequest):
    ok = await liga_controlador.agregar_arbitro(req.id_liga, req.id_item)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo agregar árbitro")
    return {"detalle": "Árbitro agregado correctamente"}

@router.post("/ligas/eliminar_arbitro")
@log_action(action_name="LIGA_ELIMINAR_ARBITRO")
async def eliminar_arbitro(req: IdRequest):
    ok = await liga_controlador.eliminar_arbitro(req.id_liga, req.id_item)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo eliminar árbitro")
    return {"detalle": "Árbitro eliminado correctamente"}

# --------- Crear arbitro y asignar a liga ---------
@router.post("/ligas/registrar_arbitro_en_liga")
@log_action(action_name="REGISTRAR_ARBITRO_EN_LIGA")
async def registrar_arbitro_en_liga(request: CrearArbitroEnLigaRequest):
    try:
        id_arbitro = await registro_liga_facade.registrar_arbitro_en_liga(request.arbitro, request.id_liga)
        return {"id_arbitro": id_arbitro, "detalle": "Árbitro creado y asignado a la liga"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------- Agregar/eliminar director ---------
@router.post("/ligas/agregar_director")
@log_action(action_name="LIGA_AGREGAR_DIRECTOR")
async def agregar_director(req: IdRequest):
    ok = await liga_controlador.agregar_director(req.id_liga, req.id_item)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo agregar director")
    return {"detalle": "Director agregado correctamente"}

@router.post("/ligas/eliminar_director")
@log_action(action_name="LIGA_ELIMINAR_DIRECTOR")
async def eliminar_director(req: IdRequest):
    ok = await liga_controlador.eliminar_director(req.id_liga, req.id_item)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo eliminar director")
    return {"detalle": "Director eliminado correctamente"}

# --------- Crear director y asignar a liga ---------
@router.post("/ligas/registrar_director_en_liga")
@log_action(action_name="REGISTRAR_DIRECTOR_EN_LIGA")
async def registrar_director_en_liga(request: CrearDirectorEnLigaRequest):
    try:
        id_director = await registro_liga_facade.registrar_director_en_liga(request.director, request.id_liga)
        return {"id_director": id_director, "detalle": "Director creado y asignado a la liga"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------- Agregar/eliminar partido ---------
@router.post("/ligas/agregar_partido")
@log_action(action_name="LIGA_AGREGAR_PARTIDO")
async def agregar_partido(req: IdRequest):
    ok = await liga_controlador.agregar_partido(req.id_liga, req.id_item)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo agregar partido")
    return {"detalle": "Partido agregado correctamente"}

@router.post("/ligas/eliminar_partido")
@log_action(action_name="LIGA_ELIMINAR_PARTIDO")
async def eliminar_partido(req: IdRequest):
    ok = await liga_controlador.eliminar_partido(req.id_liga, req.id_item)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo eliminar partido")
    return {"detalle": "Partido eliminado correctamente"}

# --------- Actualizar fase ---------
@router.post("/ligas/actualizar_fase")
@log_action(action_name="LIGA_ACTUALIZAR_FASE")
async def actualizar_fase(req: FaseRequest):
    ok = await liga_controlador.actualizar_fase(req.id_liga, req.nueva_fase)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la fase")
    return {"detalle": "Fase actualizada correctamente"}

# --------- Agregar/eliminar equipo ---------
@router.post("/ligas/agregar_equipo")
@log_action(action_name="LIGA_AGREGAR_EQUIPO")
async def agregar_equipo(req: IdRequest):
    ok = await liga_controlador.agregar_equipo(req.id_liga, req.id_item)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo agregar equipo")
    return {"detalle": "Equipo agregado correctamente"}

@router.post("/ligas/eliminar_equipo")
@log_action(action_name="LIGA_ELIMINAR_EQUIPO")
async def eliminar_equipo(req: IdRequest):
    ok = await liga_controlador.eliminar_equipo(req.id_liga, req.id_item)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo eliminar equipo")
    return {"detalle": "Equipo eliminado correctamente"}

# --------- Listar todas las ligas ---------
@router.get("/ligas")
async def listar_ligas():
    ligas = await liga_controlador.listar_ligas()
    return ligas

#---------- Eliminar liga completa ---------
@router.delete("/ligas/{id}/completa")
@log_action(action_name="ELIMINAR_LIGA_COMPLETA")
async def eliminar_liga_completa(id: str):
    ok = await eliminacion_liga_facade.eliminar_liga_completa(id)
    if not ok:
        raise HTTPException(status_code=404, detail="No se pudo eliminar la liga o no existe")
    return {"detalle": "Liga y entidades relacionadas eliminadas correctamente"}

#---------- Directores sin equipo -----------
@router.get("/ligas/{id}/directores_sin_equipo")
async def get_directores_sin_equipo(id: str):
    directores = await liga_controlador.directores_sin_equipo(id, equipo_controlador)
    return {"directores_sin_equipo": directores}