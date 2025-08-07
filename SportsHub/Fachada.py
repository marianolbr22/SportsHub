class RegistroLigaFacade:
    def __init__(self, director_controlador, arbitro_controlador, liga_controlador):
        self.director_controlador = director_controlador
        self.arbitro_controlador = arbitro_controlador
        self.liga_controlador = liga_controlador

    async def registrar_director_en_liga(self, director, id_liga):
        id_director = await self.director_controlador.registrar_director(director)
        ok = await self.liga_controlador.agregar_director(id_liga, id_director)
        if not ok:
            raise Exception("No se pudo agregar el director a la liga")
        return id_director

    async def registrar_arbitro_en_liga(self, arbitro, id_liga):
        id_arbitro = await self.arbitro_controlador.registrar_arbitro(arbitro)
        ok = await self.liga_controlador.agregar_arbitro(id_liga, id_arbitro)
        if not ok:
            raise Exception("No se pudo agregar el árbitro a la liga")
        return id_arbitro

class EliminacionEquipoFacade:
    def __init__(
        self,
        equipo_modelo,
        usuario_modelo,
    ):
        self.equipo_modelo = equipo_modelo
        self.usuario_modelo = usuario_modelo

    async def eliminar_equipo_completo(self, id_equipo: str) -> bool:
        # 1. Elimina el equipo de los favoritos de todos los usuarios, admins, directores y árbitros
        await self.usuario_modelo.eliminar_equipo_favorito_en_todos(id_equipo)

        # 2. Elimina el equipo de la base de datos
        return await self.equipo_modelo.eliminar(id_equipo)


class EliminacionLigaFacade:
    def __init__(
        self,
        liga_modelo,
        equipo_modelo,
        partido_modelo,
        arbitro_modelo,
        director_modelo,
        usuario_modelo,
        admin_modelo
    ):
        self.liga_modelo = liga_modelo
        self.equipo_modelo = equipo_modelo
        self.partido_modelo = partido_modelo
        self.arbitro_modelo = arbitro_modelo
        self.director_modelo = director_modelo
        self.usuario_modelo = usuario_modelo
        self.admin_modelo = admin_modelo

    async def eliminar_liga_completa(self, id_liga: str) -> bool:
        # 1. Busca la liga por id
        liga = await self.liga_modelo.buscar_por_id(id_liga)
        if not liga:
            return False

        # 2. Elimina todos los equipos asociados
        if hasattr(liga, "equipos"):
            for id_equipo in liga.equipos:
                await self.usuario_modelo.eliminar_equipo_favorito_en_todos(id_equipo)
                await self.equipo_modelo.eliminar(id_equipo)

        # 3. Elimina todos los partidos asociados
        if hasattr(liga, "partidos"):
            for id_partido in liga.partidos:
                await self.partido_modelo.eliminar(id_partido)

        # 4. Elimina todos los árbitros asociados
        if hasattr(liga, "arbitros"):
            for id_arbitro in liga.arbitros:
                await self.arbitro_modelo.eliminar(id_arbitro)

        # 5. Elimina todos los directores asociados
        if hasattr(liga, "directores"):
            for id_director in liga.directores:
                await self.director_modelo.eliminar(id_director)

        # 6. Elimina la liga de los favoritos de todos los usuarios, admins, directores y árbitros
        await self.usuario_modelo.eliminar_liga_favorita_en_todos(id_liga)

        # 7. Elimina la liga de las ligas de todos los admins
        await self.admin_modelo.eliminar_liga_de_admins(id_liga)

        # 8. Elimina el documento de la liga
        ok = await self.liga_modelo.eliminar(id_liga)
        return ok

class ConsultasAvanzadasFacade:
    def __init__(self, liga_modelo, reglas_modelo):
        self.liga_modelo = liga_modelo
        self.reglas_modelo = reglas_modelo

    async def obtener_reglas_por_partido(self, id_partido: str):
        liga = await self.liga_modelo.buscar_por_partido(id_partido)
        if not liga:
            return None
        return await self.reglas_modelo.buscar_por_id(liga.reglas_id)

