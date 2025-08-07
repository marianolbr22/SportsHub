from bson import ObjectId
from Clases import Admin
import bcrypt
from MongoDB import MongoDB

class AdminModelo:
    def __init__(self):
        db = MongoDB.get_database()
        self._coleccion = db["usuarios"]

    async def insertar(self, admin: Admin) -> str:
        doc = admin.model_dump(by_alias=True, exclude_unset=True)
        doc["contrasena"] = bcrypt.hashpw(doc["contrasena"].encode(), bcrypt.gensalt()).decode()
        resultado = await self._coleccion.insert_one(doc)
        return str(resultado.inserted_id)

    async def buscar_por_id(self, id: str) -> Admin | None:
        doc = await self._coleccion.find_one({"_id": ObjectId(id), "rol": "admin"})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Admin(**doc)
        return None

    async def agregar_favorito(self, id_admin: str, tipo: str, id_fav: str) -> bool:
        campo = "ligasFav" if tipo == "liga" else "equipoFav"
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_admin), "rol": "admin"},
            {"$addToSet": {campo: id_fav}}
        )
        return resultado.modified_count > 0

    async def eliminar_favorito(self, id_admin: str, tipo: str, id_fav: str) -> bool:
        campo = "ligasFav" if tipo == "liga" else "equipoFav"
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_admin), "rol": "admin"},
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

    async def agregar_liga(self, id_admin: str, id_liga: str) -> bool:
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_admin), "rol": "admin"},
            {"$addToSet": {"ligas": id_liga}}
        )
        return resultado.modified_count > 0

    async def eliminar_liga_de_admins(self, id_liga: str) -> None:
        await self._coleccion.update_many(
            {},
            {"$pull": {"ligas": id_liga}}
        )
