from bson import ObjectId
from Clases import Horario
from MongoDB import MongoDB

class HorarioModelo:
    def __init__(self):
        db = MongoDB.get_database()
        self._ligas = db["ligas"]
        self._partidos = db["partidos"]

    async def agregar_temporada_a_liga(self, id_liga: str, horario: Horario) -> bool:
        resultado = await self._ligas.update_one(
            {"_id": ObjectId(id_liga)},
            {"$push": {"temporada": horario.model_dump()}}
        )
        return resultado.modified_count > 0

    async def actualizar_temporada_en_liga(self, id_liga: str, index: int, nuevo_horario: Horario) -> bool:
        campo = f"temporada.{index}"
        resultado = await self._ligas.update_one(
            {"_id": ObjectId(id_liga)},
            {"$set": {campo: nuevo_horario.model_dump()}}
        )
        return resultado.modified_count > 0

    async def actualizar_horario_en_partido(self, id_partido: str, nuevo_horario: Horario) -> bool:
        resultado = await self._partidos.update_one(
            {"_id": ObjectId(id_partido)},
            {"$set": {"horario": nuevo_horario.model_dump()}}
        )
        return resultado.modified_count > 0
