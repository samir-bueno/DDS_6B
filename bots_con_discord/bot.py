import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True

# Crear el bot con el prefijo '!'
bot = commands.Bot(command_prefix="!", intents=intents)

# Diccionario para manejar la partida
partida = {
    "activa": False,
    "jugadores": [],
    "max_jugadores": 0
}

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

@bot.command()
async def mafia_crear(ctx, cantidad: int):
    if partida["activa"]:
        await ctx.send("⚠️ Ya hay una partida en curso.")
        return

    partida.update({
        "activa": True,
        "jugadores": [ctx.author],
        "max_jugadores": cantidad
    })
    
    await ctx.send(f"🎭 **Se ha creado una partida de Mafia para {cantidad} jugadores!**\nUsa `!mafia unirme` para participar.")

@bot.command()
async def mafia_unirme(ctx):
    if not partida["activa"]:
        await ctx.send("⚠️ No hay ninguna partida creada. Usa `!mafia crear <número>` para iniciar una.")
        return

    if ctx.author in partida["jugadores"]:
        await ctx.send("⚠️ Ya estás en la partida.")
        return

    if len(partida["jugadores"]) >= partida["max_jugadores"]:
        await ctx.send("⚠️ La partida ya está llena.")
        return

    partida["jugadores"].append(ctx.author)
    await ctx.send(f"✅ {ctx.author.display_name} se ha unido. Jugadores actuales: {len(partida['jugadores'])}/{partida['max_jugadores']}")

    if len(partida["jugadores"]) == partida["max_jugadores"]:
        await asignar_roles(ctx)

async def asignar_roles(ctx):
    roles = ["Mafioso", "Ciudadano", "Doctor", "Detective"]
    random.shuffle(partida["jugadores"])

    for i, jugador in enumerate(partida["jugadores"]):
        rol = roles[i % len(roles)]
        try:
            await jugador.send(f"🤫 Tu rol en la partida es **{rol}**.")
        except discord.Forbidden:
            await ctx.send(f"⚠️ No puedo enviarle mensaje privado a {jugador.display_name}. Activa los mensajes privados.")

    await ctx.send("🔒 Todos los roles han sido asignados en privado. ¡Que comience la partida! 🎭")

bot.run(TOKEN)