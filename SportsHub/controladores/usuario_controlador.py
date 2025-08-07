import bcrypt

from modelos.usuario_modelo import UsuarioModelo
from Clases import Usuario

class UsuarioControlador:
    def __init__(self, modelo: UsuarioModelo):
        self.modelo = modelo

    async def registrar_usuario(self, usuario: Usuario) -> str:
        return await self.modelo.insertar(usuario)

    async def obtener_usuario_por_id(self, id: str):
        return await self.modelo.buscar_por_id(id)

    async def iniciar_sesion(self, correo: str, contrasena: str):
        return await self.modelo.buscar_por_correo(correo, contrasena)

    async def agregar_favorito(self, id_usuario: str, tipo: str, id_fav: str):
        return await self.modelo.agregar_favorito(id_usuario, tipo, id_fav)

    async def eliminar_favorito(self, id_usuario: str, tipo: str, id_fav: str):
        return await self.modelo.eliminar_favorito(id_usuario, tipo, id_fav)

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