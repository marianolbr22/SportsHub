from modelos.log_modelo import LogModelo
from Clases import LogEntry

class LogControlador:
    def __init__(self, modelo: LogModelo):
        self.modelo = modelo

    async def registrar_log(self, action: str, details: dict = None):
        """
        Crea y guarda una nueva entrada de log.
        """
        log_entry = LogEntry(action=action, details=details)
        await self.modelo.insertar(log_entry)