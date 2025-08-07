from modelos.horario_modelo import HorarioModelo
from Clases import Horario

class HorarioControlador:
    def __init__(self, modelo: HorarioModelo):
        self.modelo = modelo

    async def agregar_temporada(self, id_liga: str, horario: Horario) -> bool:
        return await self.modelo.agregar_temporada_a_liga(id_liga, horario)

    async def actualizar_temporada(self, id_liga: str, index: int, horario: Horario) -> bool:
        return await self.modelo.actualizar_temporada_en_liga(id_liga, index, horario)

    async def actualizar_horario_partido(self, id_partido: str, horario: Horario) -> bool:
        return await self.modelo.actualizar_horario_en_partido(id_partido, horario)
