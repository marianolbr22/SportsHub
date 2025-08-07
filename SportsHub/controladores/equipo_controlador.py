from modelos.equipo_modelo import EquipoModelo
from Clases import Equipo

class EquipoControlador:
    def __init__(self, modelo: EquipoModelo):
        self.modelo = modelo

    async def crear_equipo(self, equipo: Equipo) -> str:
        return await self.modelo.insertar(equipo)

    async def obtener_equipo_por_id(self, id: str) -> Equipo | None:
        return await self.modelo.buscar_por_id(id)

    async def asignar_director(self, id_equipo: str, id_director: str | None) -> bool:
        return await self.modelo.asignar_director(id_equipo, id_director)

    async def actualizar_posicion(self, id_equipo: str, nueva_posicion: str | int) -> bool:
        return await self.modelo.actualizar_posicion(id_equipo, nueva_posicion)

    async def actualizar_estadisticas(self, id_equipo: str, ganados: int, perdidos: int, empatados: int, puntos: int) -> bool:
        return await self.modelo.actualizar_estadisticas(id_equipo, ganados, perdidos, empatados, puntos)

    async def listar_equipos(self) -> list[Equipo]:
        return await self.modelo.listar()

    async def eliminar_equipo(self, id_equipo: str) -> bool:
        return await self.modelo.eliminar(id_equipo)

    async def buscar_por_director(self, id_director: str) -> Equipo | None:
        return await self.modelo.buscar_por_director(id_director)
