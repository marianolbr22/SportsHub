from bson import ObjectId
from Clases import Arbitro
import bcrypt
from MongoDB import MongoDB

class ArbitroModelo:
    def __init__(self):
        db = MongoDB.get_database()
        self._coleccion = db["usuarios"]

    async def insertar(self, arbitro: Arbitro) -> str:
        doc = arbitro.model_dump(by_alias=True, exclude_unset=True)
        doc["contrasena"] = bcrypt.hashpw(doc["contrasena"].encode(), bcrypt.gensalt()).decode()
        resultado = await self._coleccion.insert_one(doc)
        return str(resultado.inserted_id)

    async def buscar_por_id(self, id: str) -> Arbitro | None:
        doc = await self._coleccion.find_one({"_id": ObjectId(id), "rol": "arbitro"})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Arbitro(**doc)
        return None

    async def agregar_favorito(self, id_arbitro: str, tipo: str, id_fav: str) -> bool:
        campo = "ligasFav" if tipo == "liga" else "equipoFav"
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_arbitro), "rol": "arbitro"},
            {"$addToSet": {campo: id_fav}}
        )
        return resultado.modified_count > 0

    async def eliminar_favorito(self, id_arbitro: str, tipo: str, id_fav: str) -> bool:
        campo = "ligasFav" if tipo == "liga" else "equipoFav"
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_arbitro), "rol": "arbitro"},
            {"$pull": {campo: id_fav}}
        )
        return resultado.modified_count > 0

    async def cambiar_contrasena(self, id_usuario: str, nueva_contrasena: str) -> bool:
        nueva_contra_hash = bcrypt.hashpw(nueva_contrasena.encode(), bcrypt.gensalt()).decode()
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_usuario)},
            {"$set": {"contrasena": nueva_contra_hash}}
        )
        return resultado.modified_count > 0

    # En arbitro_modelo.py
    async def eliminar(self, id_arbitro: str) -> bool:
        resultado = await self._coleccion.delete_one({"_id": ObjectId(id_arbitro), "rol": "arbitro"})
        return resultado.deleted_count > 0
