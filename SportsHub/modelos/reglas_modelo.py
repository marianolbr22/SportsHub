from bson import ObjectId
from Clases import Reglas
from typing import Optional, List
from MongoDB import MongoDB

class ReglasModelo:
    def __init__(self):
        db = MongoDB.get_database()
        self._coleccion = db["reglas"]

    async def buscar_por_id(self, id: str) -> Optional[Reglas]:
        doc = await self._coleccion.find_one({"_id": ObjectId(id)})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Reglas(**doc)
        return None

    async def listar(self) -> List[Reglas]:
        reglas = []
        cursor = self._coleccion.find({})
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            reglas.append(Reglas(**doc))
        return reglas
