import asyncio
from collections import defaultdict
from typing import Dict, Optional, Any, List

from Clases import Novedad
from modelos.novedad_modelo import NovedadModelo


# --- Gestor de Conexiones (sin cambios) ---
class Observer:
    def __init__(self):
        self.active_connections: Dict[str, asyncio.Queue] = defaultdict(asyncio.Queue)

    async def connect(self, user_id: str) -> asyncio.Queue:
        print(f"Nuevo cliente conectado: {user_id}")
        return self.active_connections[user_id]

    def disconnect(self, user_id: str):
        print(f"Cliente desconectado: {user_id}")
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast(self, message: str):
        print(f"Enviando broadcast a {len(self.active_connections)} clientes.")
        for queue in self.active_connections.values():
            await queue.put(message)


# --- Instancias Singleton ---
manager = Observer()
novedad_modelo = NovedadModelo()


async def crear_y_enviar_novedad(
        tipo: str,
        datos: Dict[str, Any],
        liga_id: Optional[str] = None,
        equipos_ids: Optional[List[str]] = None
):
    """
    Crea una novedad, la guarda en la BD y la transmite a todos.
    """
    novedad = Novedad(
        tipo=tipo,
        liga_id=liga_id,
        equipos_ids=equipos_ids or [],
        data=datos
    )

    # 1. Guardar en la base de datos y CAPTURAR el ID real devuelto
    inserted_id = await novedad_modelo.insertar(novedad)

    # 2. Asignar el ID al objeto para que se serialize correctamente
    novedad.id = inserted_id

    # 3. Serializar el objeto (que AHORA SÍ tiene el ID) a un string JSON
    message_payload = novedad.model_dump_json(by_alias=True)

    # 4. Transmitir a todos los clientes conectados
    await manager.broadcast(message_payload)