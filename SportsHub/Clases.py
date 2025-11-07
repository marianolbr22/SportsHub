from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Union, List, Literal, Any

# Horario (embebido en partidos y ligas)
class Horario(BaseModel):
    #Depende si es para temporada o juego
    hora_inicio: Union[datetime, date]
    hora_fin: Union[datetime, date]

# Jugador embebido en equipo
class Jugador(BaseModel):
    nombre: str
    numero: int
    posicion: str
    edad: int

# Partido (colección: partidos)
class Partido(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    arbitro_id: str
    local_id: str
    visitante_id: str
    lugar: str
    resultado: Optional[Dict[str, int]]
    horario: Horario
    notas: Optional[List[str]]
    eventos: Optional[Dict[str, List[str]]]

# Liga (colección: ligas)
class Liga(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nombre: str
    reglas_id: str
    temporada: List[Horario]
    arbitros: Optional[List[str]]
    directores: Optional[List[str]]
    equipos: Optional[List[str]]
    partidos: List[str]
    fase: Optional[str]

# Reglas (colección: reglas)
class Reglas(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    deporte: str
    duracion_total: int
    num_por_equipo: int
    anotaciones: Dict[str, int]
    faltas: Dict[str, str]
    notas: Optional[List[str]]
    tipo_duracion: str

# Equipo (colección: equipos)
class Equipo(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nombre: str
    director_id: Optional[str]  # ID de un usuario con rol "director"
    jugadores: Optional[List[Jugador]]
    posicion: Optional[Union[str, int]]
    puntos_liga: int
    partidos_ganados: int
    partidos_perdidos: int
    partidos_empatados: int

# Arbitro, Director, Administrador y Usuario regular están todos en la colección "usuarios"
class Usuario(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nombre: str
    correo: EmailStr
    contrasena: str
    rol: Literal["usuario", "director", "arbitro", "admin"]
    equipoFav: Optional[List[str]] = []
    ligasFav: Optional[List[str]] = []

# Arbitro, Director, Administrador y Usuario regular están todos en la colección "usuarios"
class Admin(Usuario):
    id: Optional[str] = Field(default=None, alias="_id")
    nombre: str
    correo: EmailStr
    contrasena: str
    rol: Literal["usuario", "director", "arbitro", "admin"]
    equipoFav: Optional[List[str]] = []
    ligasFav: Optional[List[str]] = []
    telefono: str
    ligas: Optional[List[str]] = []

class Arbitro(Usuario):
    id: Optional[str] = Field(default=None, alias="_id")
    nombre: str
    correo: EmailStr
    contrasena: str
    rol: Literal["usuario", "director", "arbitro", "admin"]
    # Campos opcionales según el tipo de usuario
    equipoFav: Optional[List[str]] = []
    ligasFav: Optional[List[str]] = []
    telefono: str
    certificacion: str

class Director(Usuario):
    id: Optional[str] = Field(default=None, alias="_id")
    nombre: str
    correo: EmailStr
    contrasena: str
    rol: Literal["usuario", "director", "arbitro", "admin"]
    # Campos opcionales según el tipo de usuario
    equipoFav: Optional[List[str]] = []
    ligasFav: Optional[List[str]] = []
    telefono: str

class Novedad(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    fecha: datetime = Field(default_factory=datetime.utcnow)
    tipo: str  # ej: "resultado_actualizado", "partido_creado"
    liga_id: Optional[str] = None
    equipos_ids: Optional[List[str]] = []
    data: Dict[str, Any] # Payload con los detalles del evento