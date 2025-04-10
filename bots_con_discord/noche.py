import asyncio

async def iniciar_noche(ctx, bot, partida):
    # se avisa que empezo la noche 
    await ctx.send("🌙 La noche ha caído. La mafia decide a quién eliminar...")

    # filtra los jugadores aue son mafiosos
    mafiosos = [j for j, r in partida["jugadores"].items() if r == "Mafioso"]

    # Si no hay mafiosos (por ejemplo, fueron eliminados), se salta la noche
    if not mafiosos:
        await ctx.send("No hay mafiosos. Se salta la fase de noche.")
        return

    # Se muestra una lista de jugadores la cual los mafiosos tienen que matar
    jugadores_vivos = [j.display_name for j in partida["jugadores"] if partida["jugadores"][j] != "Mafioso"]
    mensaje_lista = "👥 Jugadores vivos que NO son mafiosos:\n" + "\n".join(f"- {nombre}" for nombre in jugadores_vivos)

    # la lista de jugadores se manda al canal privado de los mafiosos
    if partida.get("canal_mafia"):
        await partida["canal_mafia"].send(mensaje_lista)

    # la función verifica que el mensaje es de un mafioso y tenga el formato correcto --> !matar @jugador
    def mensaje_mafioso(msg):
        return msg.author in mafiosos and msg.content.startswith("!matar ") and msg.mentions

    try:
        # el tiempo es de un minuto o 60 segundos que tiene el mafioso para matar sino lo hace en ese tiempo pasa a la fase dia
        msg = await bot.wait_for("message", check=mensaje_mafioso, timeout=60)
        victima = msg.mentions[0]  # El jugador mencionado es la víctima
    except asyncio.TimeoutError:
        # si se acaba el tiempo y la partida sigue, se avisa que no mataron a nadie
        if not partida["activa"]:
            return
        await ctx.send("⏳ La mafia no ha elegido a nadie esta noche.")
        return

    # se verifica si la partida sigue activa (osea si terminó justo después de elegir)
    if not partida["activa"]:
        return

    # se verifica que la víctima siga viva antes de intentar eliminarla
    if victima not in partida["jugadores"]:
        await ctx.send(f"⚠️ {victima.display_name} no está en la partida.")
        return

    # se elimina a la victima y se muestra cual fue su rol
    rol_victima = partida["jugadores"].pop(victima)
    await ctx.send(f"💀 {victima.display_name} ha sido eliminado durante la noche. Era un **{rol_victima}**.")