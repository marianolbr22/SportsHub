from bson import ObjectId
from Clases import Jugador
from MongoDB import MongoDB

class JugadorModelo:
    def __init__(self):
        db = MongoDB.get_database()
        self._coleccion = db["equipos"]

    async def agregar_jugador(self, id_equipo: str, jugador: Jugador) -> bool:
        jugador_dict = jugador.model_dump()
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_equipo)},
            {"$addToSet": {"jugadores": jugador_dict}}
        )
        return resultado.modified_count > 0

    async def eliminar_jugador(self, id_equipo: str, numero: int) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_equipo)},
            {"$pull": {"jugadores": {"numero": numero}}}
        )
        return resultado.modified_count > 0
