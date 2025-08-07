import bcrypt

from modelos.arbitro_modelo import ArbitroModelo
from Clases import Arbitro

class ArbitroControlador:
    def __init__(self, modelo: ArbitroModelo):
        self.modelo = modelo

    async def registrar_arbitro(self, arbitro: Arbitro) -> str:
        return await self.modelo.insertar(arbitro)

    async def obtener_arbitro_por_id(self, id: str):
        return await self.modelo.buscar_por_id(id)

    async def agregar_favorito(self, id_arbitro: str, tipo: str, id_fav: str):
        return await self.modelo.agregar_favorito(id_arbitro, tipo, id_fav)

    async def eliminar_favorito(self, id_arbitro: str, tipo: str, id_fav: str):
        return await self.modelo.eliminar_favorito(id_arbitro, tipo, id_fav)

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

    # En arbitro_controlador.py
    async def eliminar_arbitro(self, id_arbitro: str) -> bool:
        return await self.modelo.eliminar(id_arbitro)
