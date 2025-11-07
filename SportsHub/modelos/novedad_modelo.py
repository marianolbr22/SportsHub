# SportsHub/modelos/novedad_modelo.py

from typing import List
from datetime import datetime

from Clases import Novedad
from MongoDB import MongoDB


class NovedadModelo:
    def __init__(self):
        db = MongoDB.get_database()
        self._coleccion = db["novedades"]

    async def insertar(self, novedad: Novedad) -> str:
        """Inserta una nueva novedad en la base de datos."""
        # exclude_none=True previene el error de _id nulo al insertar
        doc = novedad.model_dump(by_alias=True, exclude_none=True)

        if 'fecha' not in doc or doc['fecha'] is None:
            doc['fecha'] = datetime.utcnow()

        resultado = await self._coleccion.insert_one(doc)
        return str(resultado.inserted_id)

    async def listar_recientes(self, limite: int = 50) -> List[Novedad]:
        """
        Obtiene las últimas 'limite' novedades, ordenadas de la más nueva a la más antigua.
        """
        novedades = []
        cursor = self._coleccion.find({}).sort("fecha", -1).limit(limite)

        async for doc in cursor:
            # --- CORRECCIÓN AQUÍ ---
            # Convertimos el ObjectId de MongoDB a un string antes de pasarlo a Pydantic.
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])

            novedades.append(Novedad(**doc))

        # Las devolvemos en orden cronológico (más antiguas primero)
        return novedades[::-1]