from modelos.reglas_modelo import ReglasModelo
from Clases import Reglas
from typing import List

class ReglasControlador:
    def __init__(self, modelo: ReglasModelo):
        self.modelo = modelo

    async def obtener_regla_por_id(self, id: str) -> Reglas | None:
        return await self.modelo.buscar_por_id(id)

    async def listar_reglas(self) -> List[Reglas]:
        return await self.modelo.listar()
