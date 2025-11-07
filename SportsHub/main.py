from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.cuentas import router as cuentas_router
from routes.ligas import router as ligas_router
from routes.reglas import router as reglas_router
from routes.partidos import router as partidos_router
from routes.equipo import router as equipo_router
from routes.notifications import router as notifications_router


app = FastAPI(
    title="SportsHub API",
    description="API para manejo de cuentas de usuarios, administradores, directores y árbitros.",
    version="1.0.0"
)

# Permitir CORS para desarrollo (puedes limitar los dominios en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, usa: ["https://tu-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar los endpoints de cuentas (usuarios, admins, directores, árbitros)
app.include_router(cuentas_router, prefix="")
app.include_router(ligas_router, prefix="")
app.include_router(reglas_router, prefix="")
app.include_router(equipo_router, prefix="")
app.include_router(partidos_router, prefix="")
app.include_router(notifications_router, prefix="")


# Si después tienes más routers, inclúyelos aquí:
# from routes.equipos import router as equipos_router
# app.include_router(equipos_router, prefix="/equipos")

# Endpoint raíz opcional
@app.get("/")
def root():
    return {"mensaje": "API de SportsHub activa"}
