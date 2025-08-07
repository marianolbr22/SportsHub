from bson import ObjectId
from typing import Optional, List, Dict
from Clases import Partido
from MongoDB import MongoDB

class PartidoModelo:
    def __init__(self):
        db = MongoDB.get_database()
        self._coleccion = db["partidos"]

    async def insertar(self, partido: Partido) -> str:
        doc = partido.model_dump(by_alias=True, exclude_unset=True)
        resultado = await self._coleccion.insert_one(doc)
        return str(resultado.inserted_id)

    async def agregar_arbitro(self, id_partido: str, id_arbitro: str) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_partido)},
            {"$set": {"arbitro_id": id_arbitro}}
        )
        return resultado.modified_count > 0

    async def eliminar_arbitro(self, id_partido: str) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_partido)},
            {"$unset": {"arbitro_id": ""}}
        )
        return resultado.modified_count > 0

    async def actualizar_resultado(self, id_partido: str, resultado: Dict[str, int]) -> bool:
        resultado_op = await self._coleccion.update_one(
            {"_id": ObjectId(id_partido)},
            {"$set": {"resultado": resultado}}
        )
        return resultado_op.modified_count > 0

    async def actualizar_eventos(self, id_partido: str, eventos: Dict[int, List[str]]) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_partido)},
            {"$set": {"eventos": eventos}}
        )
        return resultado.modified_count > 0

    async def listar(self) -> List[Partido]:
        partidos = []
        cursor = self._coleccion.find({})
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            partidos.append(Partido(**doc))
        return partidos

    async def buscar_por_id(self, id: str) -> Optional[Partido]:
        doc = await self._coleccion.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Partido(**doc)
        return None

    async def buscar_por_equipo(self, id_equipo: str) -> List[Partido]:
        partidos = []
        cursor = self._coleccion.find({
            "$or": [
                {"local_id": id_equipo},
                {"visitante_id": id_equipo}
            ]
        })
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            partidos.append(Partido(**doc))
        return partidos

    async def buscar_por_arbitro(self, id_arbitro: str) -> List[Partido]:
        partidos = []
        cursor = self._coleccion.find({"arbitro_id": id_arbitro})
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            partidos.append(Partido(**doc))
        return partidos

    async def eliminar(self, id: str) -> bool:
        resultado = await self._coleccion.delete_one({"_id": ObjectId(id)})
        return resultado.deleted_count > 0

    from Clases import Partido

    async def actualizar_completo(self, id: str, partido: Partido) -> bool:
        data = partido.model_dump(by_alias=True, exclude_unset=True)
        data.pop("_id", None)
        resultado = await self._coleccion.replace_one(
            {"_id": ObjectId(id)},
            data
        )
        return resultado.modified_count > 0
