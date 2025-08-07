from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Clases import Usuario, Admin
from modelos.usuario_modelo import UsuarioModelo
from modelos.admin_modelo import AdminModelo
from modelos.director_modelo import DirectorModelo
from modelos.arbitro_modelo import ArbitroModelo
from controladores.usuario_controlador import UsuarioControlador
from controladores.admin_controlador import AdminControlador
from controladores.director_controlador import DirectorControlador
from controladores.arbitro_controlador import ArbitroControlador

router = APIRouter()

usuario_controlador = UsuarioControlador(UsuarioModelo())
admin_controlador = AdminControlador(AdminModelo())
director_controlador = DirectorControlador(DirectorModelo())
arbitro_controlador = ArbitroControlador(ArbitroModelo())

# --------- Modelos Pydantic para Requests ---------
class LoginRequest(BaseModel):
    correo: str
    contrasena: str

class CambioContrasenaRequest(BaseModel):
    id: str
    actual: str
    nueva1: str
    nueva2: str

class FavoritoRequest(BaseModel):
    id_usuario: str
    tipo: str  # "liga" o "equipo"
    id_fav: str

class LigaAdminRequest(BaseModel):
    id_admin: str
    id_liga: str

# --------- Registro solo para usuario y admin ---------
@router.post("/registrar/usuario")
async def registrar_usuario(usuario: Usuario):
    id_nuevo = await usuario_controlador.registrar_usuario(usuario)
    return {"id": id_nuevo}

@router.post("/registrar/admin")
async def registrar_admin(admin: Admin):
    id_nuevo = await admin_controlador.registrar_admin(admin)
    return {"id": id_nuevo}

# --------- Login (funciona para todos los roles) ---------
@router.post("/login")
async def login(request: LoginRequest):
    usuario = await usuario_controlador.iniciar_sesion(request.correo, request.contrasena)
    if not usuario:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    user_dict = usuario.dict()
    user_dict.pop("contrasena", None)
    return user_dict

# --------- Obtener usuario/admin/director/arbitro por id ---------
@router.get("/usuario/{id}")
async def get_usuario(id: str):
    usuario = await usuario_controlador.obtener_usuario_por_id(id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_dict = usuario.dict()
    user_dict.pop("contrasena", None)
    return user_dict

@router.get("/admin/{id}")
async def get_admin(id: str):
    admin = await admin_controlador.obtener_admin_por_id(id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")
    admin_dict = admin.dict()
    admin_dict.pop("contrasena", None)
    return admin_dict

@router.get("/director/{id}")
async def get_director(id: str):
    director = await director_controlador.obtener_director_por_id(id)
    if not director:
        raise HTTPException(status_code=404, detail="Director no encontrado")
    director_dict = director.dict()
    director_dict.pop("contrasena", None)
    return director_dict

@router.get("/arbitro/{id}")
async def get_arbitro(id: str):
    arbitro = await arbitro_controlador.obtener_arbitro_por_id(id)
    if not arbitro:
        raise HTTPException(status_code=404, detail="Arbitro no encontrado")
    arbitro_dict = arbitro.dict()
    arbitro_dict.pop("contrasena", None)
    return arbitro_dict

# --------- Cambiar contraseña ---------
@router.post("/cambiar_contrasena/usuario")
async def cambiar_contrasena_usuario(request: CambioContrasenaRequest):
    resultado = await usuario_controlador.cambiar_contrasena(request.id, request.actual, request.nueva1, request.nueva2)
    if "correctamente" not in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return {"detalle": resultado}

@router.post("/cambiar_contrasena/admin")
async def cambiar_contrasena_admin(request: CambioContrasenaRequest):
    resultado = await admin_controlador.cambiar_contrasena(request.id, request.actual, request.nueva1, request.nueva2)
    if "correctamente" not in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return {"detalle": resultado}

@router.post("/cambiar_contrasena/director")
async def cambiar_contrasena_director(request: CambioContrasenaRequest):
    resultado = await director_controlador.cambiar_contrasena(request.id, request.actual, request.nueva1, request.nueva2)
    if "correctamente" not in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return {"detalle": resultado}

@router.post("/cambiar_contrasena/arbitro")
async def cambiar_contrasena_arbitro(request: CambioContrasenaRequest):
    resultado = await arbitro_controlador.cambiar_contrasena(request.id, request.actual, request.nueva1, request.nueva2)
    if "correctamente" not in resultado:
        raise HTTPException(status_code=400, detail=resultado)
    return {"detalle": resultado}

# --------- Favoritos ---------
@router.post("/favorito/usuario/agregar")
async def agregar_favorito_usuario(request: FavoritoRequest):
    ok = await usuario_controlador.agregar_favorito(request.id_usuario, request.tipo, request.id_fav)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo agregar favorito")
    return {"detalle": "Favorito agregado"}

@router.post("/favorito/usuario/eliminar")
async def eliminar_favorito_usuario(request: FavoritoRequest):
    ok = await usuario_controlador.eliminar_favorito(request.id_usuario, request.tipo, request.id_fav)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo eliminar favorito")
    return {"detalle": "Favorito eliminado"}

@router.post("/admin/agregar_liga")
async def agregar_liga_admin(request: LigaAdminRequest):
    ok = await admin_controlador.agregar_liga(request.id_admin, request.id_liga)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo agregar la liga al admin")
    return {"detalle": "Liga agregada correctamente"}

@router.delete("/arbitro/{id}")
async def eliminar_arbitro(id: str):
    ok = await arbitro_controlador.eliminar_arbitro(id)
    if not ok:
        raise HTTPException(status_code=404, detail="No se pudo eliminar el arbitro o no existe")
    return {"detalle": "Arbitro eliminado correctamente"}

@router.delete("/director/{id}")
async def eliminar_director(id: str):
    ok = await director_controlador.eliminar_director(id)
    if not ok:
        raise HTTPException(status_code=404, detail="No se pudo eliminar el director o no existe")
    return {"detalle": "Director eliminado correctamente"}
