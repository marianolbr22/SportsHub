from bson import ObjectId
from typing import Optional, List
from Clases import Liga
from MongoDB import MongoDB

class LigaModelo:
    def __init__(self):
        db = MongoDB.get_database()
        self._coleccion = db["ligas"]

    async def insertar(self, liga: Liga) -> str:
        doc = liga.model_dump(by_alias=True, exclude_unset=True)
        resultado = await self._coleccion.insert_one(doc)
        return str(resultado.inserted_id)

    async def eliminar(self, id: str) -> bool:
        resultado = await self._coleccion.delete_one({"_id": ObjectId(id)})
        return resultado.deleted_count > 0

    async def buscar_por_id(self, id: str) -> Optional[Liga]:
        doc = await self._coleccion.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Liga(**doc)
        return None

    async def agregar_arbitro(self, id_liga: str, id_arbitro: str) -> bool:
        return await self._add_to_list(id_liga, "arbitros", id_arbitro)

    async def eliminar_arbitro(self, id_liga: str, id_arbitro: str) -> bool:
        return await self._remove_from_list(id_liga, "arbitros", id_arbitro)

    async def agregar_director(self, id_liga: str, id_director: str) -> bool:
        return await self._add_to_list(id_liga, "directores", id_director)

    async def eliminar_director(self, id_liga: str, id_director: str) -> bool:
        return await self._remove_from_list(id_liga, "directores", id_director)

    async def agregar_partido(self, id_liga: str, id_partido: str) -> bool:
        return await self._add_to_list(id_liga, "partidos", id_partido)

    async def eliminar_partido(self, id_liga: str, id_partido: str) -> bool:
        return await self._remove_from_list(id_liga, "partidos", id_partido)

    async def actualizar_fase(self, id_liga: str, nueva_fase: str) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_liga)},
            {"$set": {"fase": nueva_fase}}
        )
        return resultado.modified_count > 0

    async def agregar_equipo(self, id_liga: str, id_equipo: str) -> bool:
        return await self._add_to_list(id_liga, "equipos", id_equipo)

    async def eliminar_equipo(self, id_liga: str, id_equipo: str) -> bool:
        return await self._remove_from_list(id_liga, "equipos", id_equipo)

    async def _add_to_list(self, id_liga: str, campo: str, valor: str) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_liga)},
            {"$addToSet": {campo: valor}}
        )
        return resultado.modified_count > 0

    async def _remove_from_list(self, id_liga: str, campo: str, valor: str) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_liga)},
            {"$pull": {campo: valor}}
        )
        return resultado.modified_count > 0

    async def listar(self) -> List[Liga]:
        ligas = []
        cursor = self._coleccion.find({})
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            ligas.append(Liga(**doc))
        return ligas

    async def directores_sin_equipo(self, id_liga: str, equipo_modelo) -> List[str]:
        # 1. Buscar la liga y obtener lista de directores y equipos
        liga = await self.buscar_por_id(id_liga)
        if not liga or not hasattr(liga, "directores") or not hasattr(liga, "equipos"):
            return []

        directores_liga = set(liga.directores)
        equipos_ids = liga.equipos

        # 2. Buscar los equipos y extraer director_id
        director_ids_en_equipos = set()
        for id_equipo in equipos_ids:
            equipo = await equipo_modelo.buscar_por_id(id_equipo)
            if equipo and getattr(equipo, "director_id", None):
                director_ids_en_equipos.add(equipo.director_id)

        # 3. Devolver los directores de la liga que no están en equipos
        directores_sin = list(directores_liga - director_ids_en_equipos)
        return directores_sin

    async def buscar_por_partido(self, id_partido: str):
        doc = await self._coleccion.find_one({"partidos": id_partido})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Liga(**doc)
        return None