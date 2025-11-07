# SportsHub/controladores/novedad_controlador.py

from typing import List
from modelos.novedad_modelo import NovedadModelo
from Clases import Novedad

class NovedadControlador:
    def __init__(self, modelo: NovedadModelo):
        self.modelo = modelo

    async def obtener_novedades_recientes(self, limite: int = 50) -> List[Novedad]:
        return await self.modelo.listar_recientes(limite)