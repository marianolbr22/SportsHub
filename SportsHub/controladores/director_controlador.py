import bcrypt

from modelos.director_modelo import DirectorModelo
from Clases import Director

class DirectorControlador:
    def __init__(self, modelo: DirectorModelo):
        self.modelo = modelo

    async def registrar_director(self, director: Director) -> str:
        return await self.modelo.insertar(director)

    async def obtener_director_por_id(self, id: str):
        return await self.modelo.buscar_por_id(id)

    async def agregar_favorito(self, id_director: str, tipo: str, id_fav: str):
        return await self.modelo.agregar_favorito(id_director, tipo, id_fav)

    async def eliminar_favorito(self, id_director: str, tipo: str, id_fav: str):
        return await self.modelo.eliminar_favorito(id_director, tipo, id_fav)

    async def cambiar_contrasena(self, id_usuario: str, actual: str, nueva1: str, nueva2: str) -> str:
        usuario = await self.modelo.buscar_por_id(id_usuario)
        if not usuario:
            return "Usuario no encontrado."

        if not bcrypt.checkpw(actual.encode(), usuario.contrasena.encode()):
            return "La contraseña actual es incorrecta."

        if nueva1 != nueva2:
            return "Las nuevas contraseñas no coinciden."

        cambio = await self.modelo.cambiar_contrasena(id_usuario, nueva1)
        return "Contraseña actualizada correctamente." if cambio else "No se pudo actualizar la contraseña."

    # En director_controlador.py
    async def eliminar_director(self, id_director: str) -> bool:
        return await self.modelo.eliminar(id_director)
