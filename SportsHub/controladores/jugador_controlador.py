from modelos.jugador_modelo import JugadorModelo
from Clases import Jugador

class JugadorControlador:
    def __init__(self, modelo: JugadorModelo):
        self.modelo = modelo

    async def agregar_jugador(self, id_equipo: str, jugador: Jugador) -> bool:
        return await self.modelo.agregar_jugador(id_equipo, jugador)

    async def eliminar_jugador(self, id_equipo: str, numero: int) -> bool:
        return await self.modelo.eliminar_jugador(id_equipo, numero)
