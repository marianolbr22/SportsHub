import bcrypt

from modelos.admin_modelo import AdminModelo
from Clases import Admin

class AdminControlador:
    def __init__(self, modelo: AdminModelo):
        self.modelo = modelo

    async def agregar_liga(self, id_admin: str, id_liga: str) -> bool:
        return await self.modelo.agregar_liga(id_admin, id_liga)

    async def registrar_admin(self, admin: Admin) -> str:
        return await self.modelo.insertar(admin)

    async def obtener_admin_por_id(self, id: str):
        return await self.modelo.buscar_por_id(id)

    async def agregar_favorito(self, id_admin: str, tipo: str, id_fav: str):
        return await self.modelo.agregar_favorito(id_admin, tipo, id_fav)

    async def eliminar_favorito(self, id_admin: str, tipo: str, id_fav: str):
        return await self.modelo.eliminar_favorito(id_admin, tipo, id_fav)

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