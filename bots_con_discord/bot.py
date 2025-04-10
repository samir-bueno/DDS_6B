import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from noche import iniciar_noche
from dia import iniciar_dia, verificar_ganador

# cargamos el token del bot desde el archivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# activamos los permisos necesarios para que el bot pueda leer mensajes, ver miembros, etc
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# crea el bot con el prefijo "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# se crea un diccionario para que guarda los valores principales de la partida actual, como si esta activa, jugadores, etc
partida = {
    "activa": False,
    "jugadores": {},
    "max_jugadores": 0,
    "canal_mafia": None
}

# cuando el bot se conecta, lo muestra en consola
@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

# este comando se usa para crear una nueva partida
@bot.command()
async def mafia_crear(ctx, cantidad: int):
    if partida["activa"]:
        await ctx.send("⚠️ Ya hay una partida en curso.")
        return

    partida.update({
        "activa": True,
        "jugadores": {},
        "max_jugadores": cantidad,
        "canal_mafia": None
    })
    await ctx.send(f"🎭 Se ha creado una partida para {cantidad} jugadores! Usa `!mafia_unirme` para participar.")

# comando para que un jugador se una a la partida
@bot.command()
async def mafia_unirme(ctx):
    if not partida["activa"]:
        await ctx.send("⚠️ No hay ninguna partida creada.")
        return

    if ctx.author in partida["jugadores"]:
        await ctx.send("⚠️ Ya estás en la partida.")
        return

    if len(partida["jugadores"]) >= partida["max_jugadores"]:
        await ctx.send("⚠️ La partida ya está llena.")
        return

    partida["jugadores"][ctx.author] = None
    await ctx.send(f"✅ {ctx.author.display_name} se ha unido. Jugadores actuales: {len(partida['jugadores'])}/{partida['max_jugadores']}")

    if len(partida["jugadores"]) == partida["max_jugadores"]:
        await asignar_roles(ctx)

# esta función asigna los roles al azar y avisa a cada jugador por el chat privado
async def asignar_roles(ctx):
    jugadores = list(partida["jugadores"].keys())
    num_jugadores = len(jugadores)

    # se define cuántos roles hay según la cantidad total
    num_mafiosos = max(1, num_jugadores // 3)
    num_doctores = 1 if num_jugadores >= 5 else 0
    num_detectives = 1 if num_jugadores >= 6 else 0
    num_ciudadanos = num_jugadores - (num_mafiosos + num_doctores + num_detectives)

    # se mezclan los roles
    roles = (["Mafioso"] * num_mafiosos + ["Doctor"] * num_doctores +
             ["Detective"] * num_detectives + ["Ciudadano"] * num_ciudadanos)
    random.shuffle(roles)

    # se asignan los roles y se mandan por el chat privado
    for jugador, rol in zip(jugadores, roles):
        partida["jugadores"][jugador] = rol
        try:
            await jugador.send(f"🤫 Tu rol en la partida es **{rol}**.")
        except discord.Forbidden:
            await ctx.send(f"⚠️ No puedo enviar mensaje privado a {jugador.display_name}.")

    # se crea canal privado para los mafiosos y comienza la partida
    await crear_canal_mafia(ctx)
    await ctx.send("🔒 Todos los roles han sido asignados. ¡Comienza la partida!")
    await turno_noche_dia(ctx)

# crea un canal privado para que los mafiosos se comuniquen aunque tambien incluye al admin del servidor sin importar su rol
async def crear_canal_mafia(ctx):
    mafiosos = [j for j, r in partida["jugadores"].items() if r == "Mafioso"]
    guild = ctx.guild
    overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}

    for mafioso in mafiosos:
        overwrites[mafioso] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

    # Si ya había un canal, lo borra primero
    if partida["canal_mafia"]:
        await partida["canal_mafia"].delete()

    canal_mafia = await guild.create_text_channel("canal-mafia", overwrites=overwrites)
    partida["canal_mafia"] = canal_mafia
    await canal_mafia.send("Bienvenidos, mafiosos. Usen `!matar @jugador` para eliminar a alguien.")

# este Comando se usa para cerrar la partida en cualquier momento
@bot.command()
async def mafia_terminar(ctx):
    if not partida["activa"]:
        await ctx.send("No hay una partida en curso.")
        return

    if partida["canal_mafia"]:
        await partida["canal_mafia"].delete()

    partida.update({"activa": False, "jugadores": {}, "max_jugadores": 0, "canal_mafia": None})
    await ctx.send("❌ La partida ha sido terminada.")

# este es el bucle principal para pasar de noche a dia y si sigue la partida se repite este ciclo hasta que alguien gane
async def turno_noche_dia(ctx):
    while partida["activa"]:
        await iniciar_noche(ctx, bot, partida)
        if not partida["activa"] or await verificar_ganador(ctx, partida):
            return
        await iniciar_dia(ctx, partida)
        if not partida["activa"] or await verificar_ganador(ctx, partida):
            return

# se arranca el bot si se encuentra el token
if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR: No se encontró un token de bot en el archivo .env")