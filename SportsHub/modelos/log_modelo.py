from MongoDB import MongoDB
from Clases import LogEntry

class LogModelo:
    def __init__(self):
        db = MongoDB.get_database()
        # Creamos una nueva colección solo para los logs
        self._coleccion = db["logs"]

    async def insertar(self, log_entry: LogEntry):
        """
        Inserta una nueva entrada de log en la base de datos.
        """
        doc = log_entry.model_dump(by_alias=True, exclude_unset=True)
        # Usamos insert_one; no necesitamos devolver el ID
        await self._coleccion.insert_one(doc)