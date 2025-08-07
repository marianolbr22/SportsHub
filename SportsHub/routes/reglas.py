from fastapi import APIRouter, HTTPException
from modelos.reglas_modelo import ReglasModelo
from controladores.reglas_controlador import ReglasControlador

router = APIRouter()
reglas_controlador = ReglasControlador(ReglasModelo())

# --------- Obtener regla por ID ---------
@router.get("/reglas/{id}")
async def get_regla(id: str):
    regla = await reglas_controlador.obtener_regla_por_id(id)
    if not regla:
        raise HTTPException(status_code=404, detail="Regla no encontrada")
    return regla

# --------- Listar todas las reglas ---------
@router.get("/reglas")
async def listar_reglas():
    reglas = await reglas_controlador.listar_reglas()
    return reglas
