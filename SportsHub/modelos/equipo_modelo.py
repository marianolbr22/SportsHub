from bson import ObjectId
from typing import Optional, List
from Clases import Equipo
from MongoDB import MongoDB

class EquipoModelo:
    def __init__(self):
        db = MongoDB.get_database()
        self._coleccion = db["equipos"]

    async def insertar(self, equipo: Equipo) -> str:
        doc = equipo.model_dump(by_alias=True, exclude_unset=True)
        resultado = await self._coleccion.insert_one(doc)
        return str(resultado.inserted_id)

    async def buscar_por_id(self, id: str) -> Optional[Equipo]:
        doc = await self._coleccion.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Equipo(**doc)
        return None

    async def asignar_director(self, id_equipo: str, id_director: Optional[str]) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_equipo)},
            {"$set": {"director_id": id_director}}
        )
        return resultado.modified_count > 0

    async def actualizar_posicion(self, id_equipo: str, nueva_posicion: str | int) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_equipo)},
            {"$set": {"posicion": nueva_posicion}}
        )
        return resultado.modified_count > 0

    async def actualizar_estadisticas(self, id_equipo: str, ganados: int, perdidos: int, empatados: int, puntos: int) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_equipo)},
            {
                "$set": {
                    "partidos_ganados": ganados,
                    "partidos_perdidos": perdidos,
                    "partidos_empatados": empatados,
                    "puntos_liga": puntos
                }
            }
        )
        return resultado.modified_count > 0

    async def listar(self) -> List[Equipo]:
        equipos = []
        cursor = self._coleccion.find({})
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            equipos.append(Equipo(**doc))
        return equipos

    async def eliminar(self, id_equipo: str) -> bool:
        resultado = await self._coleccion.delete_one({"_id": ObjectId(id_equipo)})
        return resultado.deleted_count > 0


    async def buscar_por_director(self, id_director: str) -> Optional[Equipo]:
        doc = await self._coleccion.find_one({"director_id": id_director})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Equipo(**doc)
        return None
