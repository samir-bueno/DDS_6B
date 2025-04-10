import asyncio

async def iniciar_dia(ctx, partida):
    # empieza el día, se avisa al pueblo que es hora de votar
    await ctx.send("🌞 Amanece un nuevo día en el pueblo. ¡Es hora de votar por un posible mafioso! Usen `!votar @jugador`")

    votos = {}
    jugadores = list(partida["jugadores"].keys())  # lista de jugadores vivos
    jugadores_que_votaron = set()  # para que nadie vote dos veces

    # esta función filtra que el mensaje sea un voto válido
    def mensaje_voto(msg):
        return (
            msg.author in jugadores  # solo los que siguen vivos pueden votar
            and msg.content.startswith("!votar ")
            and msg.mentions  # se tiene que mencionar a alguien
            and msg.author not in jugadores_que_votaron  # no se puede votar dos veces
        )

    try:
        # se espera a que los jugadores hayan votados
        while len(jugadores_que_votaron) < len(jugadores):
            msg = await ctx.bot.wait_for("message", check=mensaje_voto, timeout=60)
            votante = msg.author
            votado = msg.mentions[0]

            if votado not in jugadores:
                await ctx.send(f"⚠️ {votado.display_name} no está en la partida.")
                continue

            # se registra el voto
            votos[votado] = votos.get(votado, 0) + 1
            jugadores_que_votaron.add(votante)
            await ctx.send(f"✅ {votante.display_name} ha votado por {votado.display_name}.")

    except asyncio.TimeoutError:
        # Si se termina el tiempo, la votación termina
        await ctx.send("⏳ Tiempo de votación terminado.")

    # si nadie votó, no se elimina a nadie
    if not votos:
        await ctx.send("⚠️ No hubo votos. Nadie será eliminado.")
        return

    # se elimina al jugador con más votos
    expulsado = max(votos, key=votos.get)
    rol_expulsado = partida["jugadores"].pop(expulsado)
    await ctx.send(f"💀 {expulsado.display_name} ha sido eliminado. Era un **{rol_expulsado}**.")

    # se verifica si el juego ya tiene un ganador después de la eliminación
    await verificar_ganador(ctx, partida)

# verifica si el juego termino y quien gano
async def verificar_ganador(ctx, partida):

    mafiosos = sum(1 for r in partida["jugadores"].values() if r == "Mafioso")
    ciudadanos = len(partida["jugadores"]) - mafiosos

    if mafiosos == 0:
        await ctx.send("🎉 ¡Los ciudadanos han ganado! La mafia ha sido erradicada.")
    elif mafiosos >= ciudadanos:
        await ctx.send("💀 La mafia ha tomado el control del pueblo. ¡La mafia gana!")
    else:
        return False  # el juego sigue

    # Si alguien ganó, se elimina el canal de la mafia
    if partida.get("canal_mafia"):
        try:
            await partida["canal_mafia"].delete()
        except Exception as e:
            print(f"Error al borrar canal de mafia: {e}")

    # la partida se resetea
    partida.update({
        "activa": False,
        "jugadores": {},
        "max_jugadores": 0,
        "canal_mafia": None
    })

    return True