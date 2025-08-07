from modelos.partido_modelo import PartidoModelo
from Clases import Partido
from typing import Dict, List

class PartidoControlador:
    def __init__(self, modelo: PartidoModelo):
        self.modelo = modelo

    async def crear_partido(self, partido: Partido) -> str:
        return await self.modelo.insertar(partido)

    async def obtener_partido_por_id(self, id: str) -> Partido | None:
        return await self.modelo.buscar_por_id(id)

    async def agregar_arbitro(self, id_partido: str, id_arbitro: str) -> bool:
        return await self.modelo.agregar_arbitro(id_partido, id_arbitro)

    async def eliminar_arbitro(self, id_partido: str) -> bool:
        return await self.modelo.eliminar_arbitro(id_partido)

    async def actualizar_resultado(self, id_partido: str, resultado: Dict[str, int]) -> bool:
        return await self.modelo.actualizar_resultado(id_partido, resultado)

    async def actualizar_faltas(self, id_partido: str, eventos: Dict[int, List[str]]) -> bool:
        return await self.modelo.actualizar_eventos(id_partido, eventos)

    async def listar_partidos(self) -> List[Partido]:
        return await self.modelo.listar()

    async def buscar_partidos_por_equipo(self, id_equipo: str) -> List[Partido]:
        return await self.modelo.buscar_por_equipo(id_equipo)

    async def buscar_partidos_por_arbitro(self, id_arbitro: str) -> List[Partido]:
        return await self.modelo.buscar_por_arbitro(id_arbitro)

    async def eliminar_partido(self, id: str) -> bool:
        return await self.modelo.eliminar(id)

    async def actualizar_partido_completo(self, id: str, partido: Partido) -> bool:
        return await self.modelo.actualizar_completo(id, partido)
