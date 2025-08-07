from typing import List

from modelos.liga_modelo import LigaModelo
from Clases import Liga

class LigaControlador:
    def __init__(self, modelo: LigaModelo):
        self.modelo = modelo

    async def crear_liga(self, liga: Liga) -> str:
        return await self.modelo.insertar(liga)

    async def eliminar_liga(self, id: str) -> bool:
        return await self.modelo.eliminar(id)

    async def obtener_liga_por_id(self, id: str) -> Liga | None:
        return await self.modelo.buscar_por_id(id)

    async def agregar_arbitro(self, id_liga: str, id_arbitro: str) -> bool:
        return await self.modelo.agregar_arbitro(id_liga, id_arbitro)

    async def eliminar_arbitro(self, id_liga: str, id_arbitro: str) -> bool:
        return await self.modelo.eliminar_arbitro(id_liga, id_arbitro)

    async def agregar_director(self, id_liga: str, id_director: str) -> bool:
        return await self.modelo.agregar_director(id_liga, id_director)

    async def eliminar_director(self, id_liga: str, id_director: str) -> bool:
        return await self.modelo.eliminar_director(id_liga, id_director)

    async def agregar_partido(self, id_liga: str, id_partido: str) -> bool:
        return await self.modelo.agregar_partido(id_liga, id_partido)

    async def eliminar_partido(self, id_liga: str, id_partido: str) -> bool:
        return await self.modelo.eliminar_partido(id_liga, id_partido)

    async def actualizar_fase(self, id_liga: str, nueva_fase: str) -> bool:
        return await self.modelo.actualizar_fase(id_liga, nueva_fase)

    async def agregar_equipo(self, id_liga: str, id_equipo: str) -> bool:
        return await self.modelo.agregar_equipo(id_liga, id_equipo)

    async def eliminar_equipo(self, id_liga: str, id_equipo: str) -> bool:
        return await self.modelo.eliminar_equipo(id_liga, id_equipo)

    async def listar_ligas(self) -> list[Liga]:
        return await self.modelo.listar()

    async def directores_sin_equipo(self, id_liga: str, equipo_controlador) -> List[str]:
        return await self.modelo.directores_sin_equipo(id_liga, equipo_controlador.modelo)
