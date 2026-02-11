import discord # API
from discord.ext import commands # comando
import logging # logs para debug
from dotenv import load_dotenv # .env
import os
import random # randomizar

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

LANES = ['top','jg','mid','adc','sup'] # tipos de lanes
LANES_SET = set(LANES)
prefs = {} # preferencias
ALIASES = {
    "csgo": "cs",
    "counter-strike": "cs",
    "cs2": "cs",
    "leagueoflegends": "lol",

    "jungle": "jg",
    "support": "sup",
    "bot": "adc"
}
lobby_config = {}
draft_config = {}  

bot = commands.Bot(command_prefix='!', intents=intents) # prefixo do bot

@bot.event
async def on_ready(): 
    print(f'Bot conectado como {bot.user.name}')

def membros_na_call(ctx, qtd):
    if not ctx.author.voice:
        return None, "Você precisa estar em um canal de voz."

    vc = ctx.author.voice.channel
    membros = [m for m in vc.members if not m.bot]

    if len(membros) < qtd:
        return None, f"Precisa ter pelo menos {qtd} pessoas na call. Atualmente tem {len(membros)}"

    random.shuffle(membros)
    return membros[:qtd], None

@bot.command()
async def lobby(ctx): # !Lobby
    gid = ctx.guild.id
    config = lobby_config.get(gid)

    if not config:
        await ctx.send("Use !setlobby primeiro.")
        return

    qtd = config["qtd"]
    modo = config["mode"]

    if modo == "draft":
        await ctx.send("Modo draft ativo. Use !draft (capitães aleatórios) ou !capitao @capitao1 @capitao2")
        return

    if not ctx.author.voice: # verificar se o membro que enviou o comando está na call.
        await ctx.send(f'Você precisa estar em um canal de voz.')
        return
 
    voice_channel = ctx.author.voice.channel
    membros = [m for m in voice_channel.members if not m.bot]

    if len(membros) < qtd:
        await ctx.send(f'Precisa ter pelo menos {qtd} pessoas na call. Atualmente tem {len(membros)}')
        return

    await ctx.send(f"Criando lobby modo {modo} com {qtd} jogadores... ")
    
    random.shuffle(membros) # randomizar os membros
    selecionados = membros[:qtd] # pegar a quantidade exata de membros da call

    meio = qtd // 2
    time1 = selecionados[:meio]
    time2 = selecionados[meio:]
    
    if config.get("lanes"):
        a1 = assign_lanes(time1, prefs)
        a2 = assign_lanes(time2, prefs)

    msg = "**Time 1:**\n"
    for m in time1:
        msg += f'- {m.display_name}\n'

    msg += "\n**Time 2:**\n"
    for m in time2:
        msg += f'- {m.display_name}\n'
    
    await ctx.send(msg)

@bot.command()
async def lane(ctx, primaria: str = None, secundaria: str = None): # !lane

    if primaria is None:
        await ctx.send(f'Use !lane <top/jg/mid/adc/sup/fill>.')
        return
    
    primaria = primaria.lower().strip()
    secundaria = secundaria.lower().strip() if secundaria else None

    primaria = ALIASES.get(primaria, primaria)
    secundaria = ALIASES.get(secundaria, secundaria) if secundaria else None

    if primaria ==   "fill": # fill
        prefs[ctx.author.id] = (None, None)
        if secundaria is not None:
            await ctx.send(f'{ctx.author.display_name}: **FILL** (qualquer lane).')
        else:
            await ctx.send(f"{ctx.author.display_name}: **FILL** (qualquer lane).")
        return

    if primaria not in LANES_SET:
        await ctx.send('Está lane não existe.')
        return

    if secundaria is None:
        await ctx.send("Faltou a segunda lane.")
        return

    if secundaria == "fill":
        prefs[ctx.author.id] = (primaria, None)
        await ctx.send(f'{ctx.author.display_name}: **{primaria.upper()} / FILL**')
        return
    
    if primaria == secundaria:
        await ctx.send("A primeira e segunda lane tem que ser diferentes.")
        return
 
    if secundaria not in LANES_SET:
        await ctx.send('Está lane não existe.')
        return

    prefs[ctx.author.id] = (primaria,secundaria)
    await ctx.send(f"{ctx.author.display_name}: {primaria.upper()} / {secundaria.upper()}")

def assign_lanes(team_members, prefs_map): # prioridade de 2 a 0 / 2 sendo a menor e 0 sendo a maior prioridade.
    lanes = LANES[:] # cópia das lanes
    assignment = {} # informações dos jogadores

    def prioridade(m): 
        pr = prefs_map.get(m.id)
        if not pr or pr == (None, None):
            return 2
        return 0

    members = sorted(team_members, key=prioridade) # randomizar os jogadores com as lanes escolhidas

    lanes_utilizadas = set() # Não ter duas lanes em 1 time

    for m in members:
        pr = prefs_map.get(m.id) # preferencia do jogador
        if pr and pr != (None, None): # ver se o jogador é diferente de fill
            primaria, secundaria = pr
            if primaria not in lanes_utilizadas: # atribuir como lane utlizada
                assignment[m] = primaria
                lanes_utilizadas.add(primaria)

    for m in members:
        if m in assignment:
            continue # se já está inserido na equipe / continua o código
        pr = prefs_map.get(m.id)
        if pr and pr != (None, None):
            primaria, secundaria = pr
            if secundaria not in lanes_utilizadas: # atribuir a segunda lane como utilizada
                assignment[m] = secundaria
                lanes_utilizadas.add(secundaria)

    for m in members:
        if m in assignment:
            continue
        for lane in lanes:
            if lane not in lanes_utilizadas: # ver qual lane está faltando
                assignment[m] = lane
                lanes_utilizadas.add(lane)
                break

    if len(assignment) != 5: # verificar se preencheu todas as lanes.
        return None 
    
    return assignment

@bot.command()
async def minhalane(ctx): # !minhalane / para saber qual lane o usuário é
    pr = prefs.get(ctx.author.id)

    if not pr: # se não tem preferencia de lane
        await ctx.send("Você não tem lanes salvas. Use `!lane mid sup` ou `!lane fill`.")
        return

    if pr == (None, None): # se é fill
        await ctx.send("Sua preferência atual: **FILL**.")
        return

    primaria, secundaria = pr
    primaria_txt = primaria.upper() if primaria else "fill"
    secundaria_txt = secundaria.upper() if secundaria else "fill"

    await ctx.send(f"Sua preferência atual: **{primaria_txt.upper()} / {secundaria_txt.upper()}**")

@bot.command()
async def setlobby(ctx, mode: str = None, qtd: int = None):  # Escolher que tipo de modo do lobby.

    if mode is None:
        await ctx.send('Escolha um tipo de lobby. Ex: !setlobby <cs,lol,custom> [quantidade]')
        return
    mode = mode.lower().strip()
    mode = ALIASES.get(mode, mode)
    gid = ctx.guild.id

    if mode == "lol":
        lobby_config[gid] = {"mode": 'lol', "qtd": 10, "lanes": True}
        await ctx.send("Lobby definido como League of Legends.")
        return

    elif mode == "cs":
        lobby_config[gid] = {"mode": 'cs', "qtd": 10, "lanes": False}
        await ctx.send("Lobby definido como Counter Strike.")
        return

    elif mode == "custom":
        if qtd is None:
            await ctx.send("Custom precisa de quantidade. Ex: !setlobby custom 4")
            return
        lobby_config[gid] = {"mode": 'custom', "qtd": qtd, "lanes": False}
        await ctx.send("Lobby definido como custom.")
        return

    elif mode == "draft":
        qtd_final = qtd if qtd is not None else 10
        if qtd_final < 4 or qtd_final % 2 != 0:
            await ctx.send(f'O modo Draft precisa de quantidade **par** e maior ou igual a 4. Ex: !Setlobby draft 6')
            return

        lobby_config[gid] = {"mode": 'draft', "qtd": qtd_final, "lanes": False}
        await ctx.send(f"Lobby definido como draft. players = {qtd_final}")
        return
    else:
        await ctx.send("Modos válidos: lol / cs / custom")

    await ctx.send(f'Modo de lobby definido para **{mode.upper()}**.')


async def start_draft(ctx, selecionados, cap1, cap2):
    gid = ctx.guild.id

    if cap1 not in selecionados or cap2 not in selecionados:
        await ctx.send("Os capitães precisam estar dentro da call.")
        return
    
    if cap1 == cap2:
        await ctx.send("Os capitães precisam ser diferentes.")
        return
    
    pool = {m.id for m in selecionados}
    pool.remove(cap1.id)
    pool.remove(cap2.id)

    draft_config[gid] = {
        "capitão": (cap1.id, cap2.id),
        "escolha": cap1.id,
        "pool": pool,
        "times": {cap1.id: [cap1.id], cap2.id: [cap2.id]},
        "qtd": len(selecionados),
    }

    await ctx.send(
        f'Draft iniciado!\n'
        f'Capitães: **{cap1.display_name}** vs **{cap2.display_name}**\n'
        f'Vez de: **{cap1.display_name}**\n'
        f'Use !pick @jogador'
        )

@bot.command()    
async def draft(ctx):
    gid = ctx.guild.id
    config = lobby_config.get(gid)

    if not config or config["mode"] != "draft":
        await ctx.send('Ative primeiro: !setlobby draft (quantidade de membros)')
        return
    
    if gid in draft_config:
        await ctx.send('Já existe um draft ativo no servidor. Use !draftcancel')
        return
    
    qtd = config["qtd"]
    selecionados, err = membros_na_call(ctx, qtd)
    if err:
        await ctx.send(err)
        return
    
    cap1, cap2 = random.sample(selecionados, 2)
    await start_draft(ctx, selecionados, cap1, cap2)
    
@bot.command()
async def capitao(ctx, cap1: discord.Member = None, cap2: discord.Member = None):
    gid = ctx.guild.id
    config = lobby_config.get(gid)

    if not config or config["mode"] != "draft":
        await ctx.send('Ative primeiro: !setlobby draft (quantidade de membros)')
        return

    if gid in draft_config:
        await ctx.send('Já existe um draft ativo no servidor. Use !draftcancel')
        return

    if cap1 is None or cap2 is None:
        await ctx.send("Os capitães não foram definidos. Use !capitão @capitão1 @capitão2")
        return
    
    qtd = config["qtd"]
    selecionados, err = membros_na_call(ctx, qtd)
    if err:
        await ctx.send(err)
        return
    await start_draft(ctx, selecionados, cap1, cap2)
    
@bot.command()
async def pick(ctx, jogador: discord.Member = None):
    gid = ctx.guild.id
    st = draft_config.get(gid)

    if not st:
        await ctx.send('Não existe draft ativo. Use !draft ou !capitão @capitão1 @capitão2')
        return

    if jogador is None:
        await ctx.send('Você não inseriu o jogador. Use !pick @jogador')
        return
    
    cap1_id, cap2_id = st["capitão"]

    if ctx.author.id not in (cap1_id, cap2_id):
        await ctx.send('Só capitães escolhe.')
        return
    
    if ctx.author.id != st["escolha"]:
        await ctx.send('Não é sua vez de escolher')
        return
    
    if jogador.id not in st["pool"]:
        await ctx.send('Esse jogador não está disponível ( ou já foi escolhido )')
        return

    st["pool"].remove(jogador.id)
    st["times"][ctx.author.id].append(jogador.id)

    st["escolha"] = cap2_id if st["escolha"] == cap1_id else cap1_id

    await ctx.send(f'**{ctx.author.display_name}** escolheu **{jogador.display_name}**. Agora é a vez de <@{st["escolha"]}>.')

    if not st["pool"]:
        guild = ctx.guild

        def nome(uid):
            m = guild.get_member(uid)
            return m.display_name if m else str(uid)
    
    t1 = ', '.join(nome(uid) for uid in st["times"][cap1_id])
    t2 = ', '.join(nome(uid) for uid in st["times"][cap2_id])

    await ctx.send("**Draft finalizado!**\n"
        f"Time 1 ({nome(cap1_id)}): {t1}\n"
        f"Time 2 ({nome(cap2_id)}): {t2}\n"
    )
    draft_config.pop(gid, None)

@bot.command()
async def draftstatus(ctx):
    st = draft_config.get(ctx.guild.id)
    if not st:
        await ctx.send('Draft não está ativo.')
        return
    await ctx.send(f'Draft ativo. Restam **{len(st['pool'])}** no pool. Vez de <@{st['escolha']}>.')

@bot.command()
async def draftcancel(ctx):
    gid = ctx.guild.id
    if gid in draft_config:
        draft_config.pop(gid,None)
        await ctx.send('Draft cancelado.')
    else:
        await ctx.send('Não há draft ativo para cancelar')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)