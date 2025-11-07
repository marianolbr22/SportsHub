import functools
from fastapi import HTTPException
from pydantic import BaseModel
from controladores.log_controlador import LogControlador
from modelos.log_modelo import LogModelo

# Instancia global de nuestro controlador de logs
log_controlador = LogControlador(LogModelo())


def log_action(action_name: str):
    """
    Este es el decorador (Aspecto).
    Registra una acción en la base de datos DESPUÉS de que la función
    original se ejecute exitosamente.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):

            # 1. Capturar los detalles de la solicitud
            log_details = {}
            for key, value in kwargs.items():
                if isinstance(value, BaseModel):
                    # Si es un modelo Pydantic (como 'request'), lo convertimos a dict
                    log_details[key] = value.model_dump()
                elif isinstance(value, (str, int, bool, list, dict)):
                    # Si es un parámetro de ruta (como 'id')
                    log_details[key] = value

            try:
                # 2. Ejecutar la función original de la ruta
                result = await func(*args, **kwargs)

                # 3. Si tiene éxito, registrar el log
                await log_controlador.registrar_log(action_name, log_details)

                # 4. Devolver el resultado original
                return result

            except HTTPException as http_exc:
                # Si es una excepción HTTP (ej. 404, 400), la relanzamos.
                # No registramos errores de negocio intencionados.
                raise http_exc
            except Exception as e:
                # Si es un error inesperado del servidor (500)
                # Registramos el error
                error_details = {
                    "error": str(e),
                    "request_args": log_details
                }
                await log_controlador.registrar_log(f"ERROR::{action_name}", error_details)

                # Relanzamos la excepción para que FastAPI responda
                raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

        return wrapper

    return decorator