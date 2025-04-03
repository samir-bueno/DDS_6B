import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from noche import iniciar_noche

# Carga las variables de entorno
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurar permisos (intents) para el bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Crear el bot incluyendo el prefijo !
bot = commands.Bot(command_prefix="!", intents=intents)

# Diccionario que representa el estado de la partida
partida = {
    "activa": False,  # indica si hla partida esta activa o no
    "jugadores": {},  # es un diccionario el cual almacena a los jugadores
    "max_jugadores": 0,  # el numero máximo de jugadores permitidos en la partida
    "canal_mafia": None  # canal privado para los mafiosos
}

# este evento nos dice si el bot esta conectado
@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

# este Comando crea una partida con !mafia_crear <cantidad_jugadores> 
@bot.command()
async def mafia_crear(ctx, cantidad: int):
    if partida["activa"]:
        await ctx.send("⚠️ Ya hay una partida en curso.")
        return

    # actualiza la partida con los nuevos valores
    partida.update({
        "activa": True,
        "jugadores": {},
        "max_jugadores": cantidad,
        "canal_mafia": None
    })
    
    await ctx.send(f"🎭 **Se ha creado una partida de Mafia para {cantidad} jugadores!**\nUsa `!mafia_unirme` para participar.")

# este Comando sirve para que los jugadores se unan a la partida con !mafia_unirme
@bot.command()
async def mafia_unirme(ctx):
    if not partida["activa"]:
        await ctx.send("⚠️ No hay ninguna partida creada. Usa `!mafia_crear <número>` para iniciar una.")
        return

    if ctx.author in partida["jugadores"]:
        await ctx.send("⚠️ Ya estás en la partida.")
        return

    if len(partida["jugadores"]) >= partida["max_jugadores"]:
        await ctx.send("⚠️ La partida ya está llena.")
        return

    # se agregan los jugadores a la partida
    partida["jugadores"][ctx.author] = None
    await ctx.send(f"✅ {ctx.author.display_name} se ha unido. Jugadores actuales: {len(partida['jugadores'])}/{partida['max_jugadores']}")

    # cuando la partida se llena se asignan los roles
    if len(partida["jugadores"]) == partida["max_jugadores"]:
        await asignar_roles(ctx)

# esta funcion asigna los roles automaticamente a los jugadores que estan en la partida
async def asignar_roles(ctx):
    roles_disponibles = ["Mafioso", "Ciudadano", "Doctor", "Detective"]
    jugadores = list(partida["jugadores"].keys())
    
    random.shuffle(jugadores)  # mezcla los jugadores para asignar roles aleatoriamente
    roles_asignados = random.choices(roles_disponibles, k=len(jugadores))
    
    for jugador, rol in zip(jugadores, roles_asignados):
        partida["jugadores"][jugador] = rol
        try:
            await jugador.send(f"🤫 Tu rol en la partida es **{rol}**.")
        except discord.Forbidden:
            await ctx.send(f"⚠️ No puedo enviarle mensaje privado a {jugador.display_name}. Activa los mensajes privados.")
    
    # Crear el canal privado para la mafia
    await crear_canal_mafia(ctx)
    
    await ctx.send("🔒 Todos los roles han sido asignados en privado. ¡Que comience la partida! 🎭")
    await iniciar_noche(ctx, bot, partida)

# Esta función crea un canal privado solo para los mafiosos
async def crear_canal_mafia(ctx):
    mafiosos = [j for j, r in partida["jugadores"].items() if r == "Mafioso"]
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),  # bloquea el acceso a todos los demás
    }
    
    for mafioso in mafiosos:
        overwrites[mafioso] = discord.PermissionOverwrite(read_messages=True, send_messages=True)  # permite a los mafiosos leer y escribir
    
    # Si existe el canal de la mafia, se elimina cuando la partida acabe
    if partida["canal_mafia"]:
        await partida["canal_mafia"].delete()
    
    canal_mafia = await guild.create_text_channel("canal-mafia", overwrites=overwrites)
    partida["canal_mafia"] = canal_mafia
    await canal_mafia.send("Bienvenidos, mafiosos. Aquí pueden hablar en secreto. Usen `!matar @jugador` para eliminar a alguien.")

# este Comando permite acabar la partida, ademas de limpiar los datos
@bot.command()
async def mafia_terminar(ctx):
    if not partida["activa"]:
        await ctx.send("No hay una partida en curso.")
        return
    
    # reinicia los valores de la partida por los que habia antes
    partida["activa"] = False
    partida["jugadores"].clear()
    partida["max_jugadores"] = 0
    
    # elimina el canal de la mafia si existe
    if partida["canal_mafia"]:
        await partida["canal_mafia"].delete()
        partida["canal_mafia"] = None
    
    await ctx.send("❌ La partida ha sido terminada")

# iniciar el bot
bot.run(TOKEN)
