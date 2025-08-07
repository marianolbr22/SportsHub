from bson import ObjectId
from typing import Optional
from Clases import Usuario, Admin, Director, Arbitro
import bcrypt
from MongoDB import MongoDB

class UsuarioModelo:
    def __init__(self):
        db = MongoDB.get_database()
        self._coleccion = db["usuarios"]

    async def insertar(self, usuario: Usuario) -> str:
        usuario_dict = usuario.model_dump(by_alias=True, exclude_unset=True)
        usuario_dict["contrasena"] = bcrypt.hashpw(usuario_dict["contrasena"].encode(), bcrypt.gensalt()).decode()
        resultado = await self._coleccion.insert_one(usuario_dict)
        return str(resultado.inserted_id)

    async def buscar_por_id(self, id: str) -> Optional[Usuario]:
        doc = await self._coleccion.find_one({"_id": ObjectId(id)})
        return self._construir_usuario(doc) if doc else None

    async def buscar_por_correo(self, correo: str, contrasena: str) -> Optional[Usuario]:
        doc = await self._coleccion.find_one({"correo": correo})
        if doc and bcrypt.checkpw(contrasena.encode(), doc["contrasena"].encode()):
            return self._construir_usuario(doc)
        return None

    async def agregar_favorito(self, id_usuario: str, tipo: str, id_fav: str) -> bool:
        campo = "ligasFav" if tipo == "liga" else "equipoFav"
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_usuario)},
            {"$addToSet": {campo: id_fav}}
        )
        return resultado.modified_count > 0

    async def eliminar_favorito(self, id_usuario: str, tipo: str, id_fav: str) -> bool:
        campo = "ligasFav" if tipo == "liga" else "equipoFav"
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_usuario)},
            {"$pull": {campo: id_fav}}
        )
        return resultado.modified_count > 0

    def _construir_usuario(self, doc: dict) -> Usuario:
        doc["_id"] = str(doc["_id"])
        rol = doc.get("rol")
        clase = {"admin": Admin, "arbitro": Arbitro, "director": Director}.get(rol, Usuario)
        return clase(**doc)

    async def cambiar_contrasena(self, id_usuario: str, nueva_contrasena: str) -> bool:
        nueva_contra_hash = bcrypt.hashpw(nueva_contrasena.encode(), bcrypt.gensalt()).decode()
        resultado = await self._coleccion.update_one(
            {"_id": ObjectId(id_usuario)},
            {"$set": {"contrasena": nueva_contra_hash}}
        )
        return resultado.modified_count > 0

    async def eliminar_liga_favorita_en_todos(self, id_liga: str) -> None:
        await self._coleccion.update_many(
            {},
            {"$pull": {"ligasFav": id_liga}}
        )

    async def eliminar_equipo_favorito_en_todos(self, id_equipo: str) -> None:
        await self._coleccion.update_many(
            {},
            {"$pull": {"equipoFav": id_equipo}}
        )
