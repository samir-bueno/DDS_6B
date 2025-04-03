import asyncio

# funcion que inicia la noche
async def iniciar_noche(ctx, bot, partida):
    await ctx.send("🌙 La noche ha comenzado. Todos cierren los ojos...")

    # filtra los jugadores que tienen el rol de mafioso
    mafiosos = [j for j, r in partida["jugadores"].items() if r == "Mafioso"]
    if not mafiosos:
        await ctx.send("⚠️ No hay mafiosos en esta partida.")
        return
    
    # canal privado de mafiosos
    canal_mafia = partida.get("canal_mafia")
    if canal_mafia:
        await canal_mafia.send("🔪 Es la hora de decidir a quién eliminar. Un mafioso debe escribir `!matar @jugador`.")
    
    # función que verifica si el mensaje es de un mafioso
    def mensaje_mafioso(msg):
        return msg.author in mafiosos and msg.content.startswith("!matar ")
    
    try:
        # se espera 60 segundos a que un mafioso elija una víctima
        msg = await bot.wait_for("message", mensaje_mafioso=mensaje_mafioso, timeout=60)
        victima_mencion = msg.mentions[0] if msg.mentions else None

        # se valida si el jugador es valido o no
        if not victima_mencion or victima_mencion not in partida["jugadores"]:
            await canal_mafia.send("⚠️ No encontré ese jugador. Intenta de nuevo la próxima noche.")
            return

        # si es un jugador de la partida se elimina de la partida
        del partida["jugadores"][victima_mencion]
        await ctx.send(f"🔪 El sol ha salido. La noche ha terminado. **{victima_mencion.display_name}** fue eliminado. 🚨")
        
        # se muestra la lista de jugadores restantes
        jugadores_restantes = ", ".join(j.display_name for j in partida["jugadores"])
        await ctx.send(f"👥 Jugadores restantes: {jugadores_restantes}")

        # se verifica si la partida ya tiene un ganador
        await verificar_ganador(ctx, partida)
    
    except asyncio.TimeoutError:
        # si no mataron a nadie en el tiempo límite, la noche termina sin víctimas
        await canal_mafia.send("⏳ No eligieron a nadie. Nadie ha muerto esta noche.")
        await ctx.send("🌞 El sol ha salido. Nadie murió esta noche.")

# función que revisa si la partida ya tiene un ganador
async def verificar_ganador(ctx, partida):
    mafiosos = sum(1 for rol in partida["jugadores"].values() if rol == "Mafioso")
    ciudadanos = sum(1 for rol in partida["jugadores"].values() if rol != "Mafioso")

    # si no hay mafiosos los ciudadanos ganas
    if mafiosos == 0:
        await ctx.send("🎉 ¡Los ciudadanos han ganado la partida!")
        await finalizar_partida(ctx, partida)
    # en caso de haber quedado los mafiosos ellos ganan
    elif mafiosos >= ciudadanos:
        await ctx.send("💀 ¡La mafia ha tomado el control! La mafia gana.")
        await finalizar_partida(ctx, partida)

# función para reiniciar los valores de la partida cuando alguien gana
async def finalizar_partida(ctx, partida):
    partida["activa"] = False
    partida["jugadores"].clear()
    partida["max_jugadores"] = 0
    
    # se elimina el canal privado de la mafia si existía
    if partida["canal_mafia"]:
        await partida["canal_mafia"].delete()
        partida["canal_mafia"] = None
    
    await ctx.send("🏁 La partida ha finalizado")
