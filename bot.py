import discord
from time import sleep
from datetime import datetime
from discord.ext import commands
from random import choice
from random import randint
from bs4 import BeautifulSoup
import asyncio
import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def linknoticia(noticia):
    texto1 = str(noticia)
    texto1teste = texto1.find('"', 49)
    textofinal = (texto1[49:texto1teste])
    return textofinal

def checarmoeda(moeda):
    dict_moedas = {'eth':'ethereum','btc':'bitcoin','slp':'smooth-love-potion','hbar':'hedera-hashgraph','axie':'axie-infinity','cake':'pancakeswap','axs':'axie-infinity','bnb':'binance-coin','dot':'polkadot','link':'chainlink','ada':'cardano'}
    if moeda in dict.keys(dict_moedas):
        moeda = dict_moedas[moeda]
    else:
        return moeda
    return moeda

client = commands.Bot(command_prefix='$ ')


@client.event
async def on_ready():
    print('O bot está preparado')

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,name='EL FUEGO'))

    await auto()


@client.event
async def on_member_join(member):
    print(f'{member} entrou no servidor')


@client.event
async def on_member_remove(member):
    print(f'{member} saiu do servidor')

@client.command()
async def teste(ctx):
    await ctx.send(ctx.author.mention)

@client.command()
async def crypto(ctx, moeda, moeda1 = ''):
    moeda = moeda.lower()
    moeda = checarmoeda(moeda)

    moeda = str(moeda)
    if len(moeda1) >= 1:
        url = f'https://coinmarketcap.com/currencies/{moeda}-{moeda1}/'
    else:
        url = f'https://coinmarketcap.com/currencies/{moeda}/'
    html = requests.get(url)

    soup = BeautifulSoup(html.text, 'html.parser')
    try:
        texto = soup.find('div',attrs={'class':'priceValue'}).text
    except:
        await ctx.send('Moeda nao encontrada')
    else:
        maximadia = soup.find('div',attrs={'class':'sc-16r8icm-0 SjVBR'}).find('span',attrs={'class':'n78udj-5 dBJPYV'}).text
        urlfoto = soup.find('div',attrs={'class':'sc-16r8icm-0 gpRPnR nameHeader'})
        url_foto_final = urlfoto.img['src']
        minimadia = soup.find('span',attrs={'class':'n78udj-5 dBJPYV'}).text
        marketcap = soup.find('div', attrs={'class': 'statsValue'}).text


        #CRIAÇAO DO EMBED

        embed = discord.Embed(title=f'{moeda.upper()}', url2=url, description=f'{url}', color=discord.Color.blue())

        # ENCONTRA A VARIAÇAO DO PREÇO

        try:
            embed = discord.Embed(title=f'{moeda.upper()}', url2=url, description=f'{url}',color=discord.Color.dark_red())
            stonks = soup.find('div', attrs={'class': 'sc-16r8icm-0 kjciSH priceTitle'}).find('span', attrs='sc-15yy2pl-0 feeyND').text
            stonks = ':chart_with_downwards_trend: ' + '-' + stonks
        except:
            embed = discord.Embed(title=f'{moeda.upper()}', url2=url, description=f'{url}', color=discord.Color.dark_green())
            stonks = soup.find('div', attrs={'class': 'sc-16r8icm-0 kjciSH priceTitle'}).find('span',attrs='sc-15yy2pl-0 gEePkg').text
            stonks = ':chart_with_upwards_trend: ' + stonks
            embed.set_image(url='https://escolaeducacao.com.br/wp-content/uploads/2021/01/meme-stonks.jpg')
        else:
            embed.set_image(url='https://i.ytimg.com/vi/21UXJFvpG0I/maxresdefault.jpg')

        #VOLUME

        volume = soup.find('div', attrs={'class': 'statsItemRight'}).find_all_next('div', attrs={'class': 'statsValue'})
        volume_2 = str(volume[2])
        volume_final = volume_2[24:len(volume_2) - 6]

        #EMBED

        embed.set_thumbnail(url=url_foto_final)
        embed.add_field(name=f'Atual Valor : {texto}     ', value=f'Minima dia : {minimadia} \nMaxima dia : {maximadia}\nVariaçao de : {stonks}')
        embed.add_field(name=f'Marketcap : {marketcap}', inline=False, value=f'Volume 24h : {volume_final}',)


        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        embed.set_footer(text=f'Atualizado as {current_time}')
        await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    c = 0
    while True:
        await ctx.send(f'O ping é {round(client.latency * 1000)}')
        c += 1
        sleep(2)
        if c == 3:
            break

@client.command()
async def noticias(ctx, tipomoeda = None, auto = None):
    numeroaleatorio1 = randint(0, 10)
    numeroaleatorio2 = randint(0, 10)
    numeroaleatorio3 = randint(0, 10)
    numeroaleatorio4 = randint(0, 10)
    lista_moeda = ['eth', 'ada', 'btc', 'avax', 'uni', 'axs', 'bch', 'usdc', 'dot', 'link', 'axs', 'sol', 'usdt']

    if tipomoeda not in lista_moeda:
        tipomoeda = None
    if tipomoeda == None:
        url_crypto_panic = 'https://cryptopanic.com/api/v1/posts/?auth_token=939b70eb870230c217f7aa6ea0f79fa82079b67c&regions=pt'
    else:
        url_crypto_panic = f'https://cryptopanic.com/api/v1/posts/?auth_token=939b70eb870230c217f7aa6ea0f79fa82079b67c&regions=pt&currencies={tipomoeda}'

    request_panic = requests.get(url_crypto_panic)
    data = request_panic.json()
    pagina_panic = [data]


    urlnoticia2 = 'https://cointelegraph.com.br'
    htmlnoticia2 = requests.get(urlnoticia2)


    soupnoticia2 = BeautifulSoup(htmlnoticia2.text, 'html.parser')
    noticias2 = soupnoticia2.find_all('div', attrs={'class': 'main-news-controls__wrap'}, limit=10)
    link0 = soupnoticia2.find_all("a", attrs={'class': 'main-news-controls__link'}, href=True, limit=10)


    ultimanoticia = soupnoticia2.find_all('span', attrs={'class':'post-card__title'}, limit=3)
    ultimaslink = soupnoticia2.find_all("a",attrs={'class':'post-card__title-link'},href=True, limit=3)



 #   link1 = linknoticia(noticias[numeroaleatorio1])
 #   link2 = linknoticia(noticias[numeroaleatorio2])

    embednoticias = discord.Embed(title = 'NOTICIAS',url='https://cointelegraph.com.br', description=f'https://cryptopanic.com', color=discord.Color.blue() )
#    embednoticias.add_field(name= f'{noticias[numeroaleatorio1].text}', value=link1)
    embednoticias.add_field(name=f'DESTAQUE : {noticias2[numeroaleatorio2].text}',value='https://cointelegraph.com.br'+link0[numeroaleatorio2]['href'])
    '''
    embednoticias.add_field(name=f'ULTIMAS : {ultimanoticia[0].text}', value='https://cointelegraph.com.br'+ultimaslink[0]['href'] , inline= False)
    embednoticias.add_field(name=f'ULTIMAS : {ultimanoticia[1].text}', value='https://cointelegraph.com.br' + ultimaslink[1]['href'] , inline=False)
    
    '''
    embednoticias.add_field(name=f'{pagina_panic[0]["results"][0]["title"]}', value=f'{pagina_panic[0]["results"][0]["url"]}', inline=True)
    embednoticias.add_field(name=f'{pagina_panic[0]["results"][1]["title"]}',value=f'{pagina_panic[0]["results"][1]["url"]}', inline=True)

    embednoticias.set_thumbnail(url='https://static.cryptopanic.com/static/img/cryptopanic-logo-vert-dark.514a405381d8.svg')

    if auto == None:
        await ctx.send(embed=embednoticias)

    elif auto == 'comecar':
        variavel = 0
        while True:
            variavel += 1
            await ctx.send(embed=embednoticias)
            if variavel == 3:
                break
            await asyncio.sleep(60)


historico = ''
@client.command()
async def auto():
    global historico
#    if autonoti != 'comecar':
#        await ctx.send('o unico valor possivel é "comecar"')
#    variavel = 0
    url_crypto_panic_auto = 'https://cryptopanic.com/api/v1/posts/?auth_token=939b70eb870230c217f7aa6ea0f79fa82079b67c&regions=pt'
#    while autonoti == 'comecar':
    while True:
#        variavel += 1


        request_panic = requests.get(url_crypto_panic_auto)
        data_auto = request_panic.json()
        pagina_panic_auto = [data_auto]

        embednoticias_auto = discord.Embed(title='NOTICIAS AUTOMATICAS', url='https://cryptopanic.com', description=f'https://cryptopanic.com',color=discord.Color.blue())
        embednoticias_auto.add_field(name=f'{pagina_panic_auto[0]["results"][0]["title"]}', value=f'{pagina_panic_auto[0]["results"][0]["url"]}', inline=True)
        embednoticias_auto.add_field(name=f'{pagina_panic_auto[0]["results"][1]["title"]}', value=f'{pagina_panic_auto[0]["results"][1]["url"]}', inline=True)
    #await ctx.send(embed=embednoticias_auto)
        channel = client.get_channel(890696993234632774)
        if pagina_panic_auto[0]["results"][0]["title"] == historico:
            await asyncio.sleep(3600)
        else:
            historico = pagina_panic_auto[0]["results"][0]["title"]
            await channel.send(embed=embednoticias_auto)
            await asyncio.sleep(3600)


@client.command()
async def season(ctx):
    request_season = requests.get('https://www.blockchaincenter.net/altcoin-season-index/')
    soup = BeautifulSoup(request_season.text, 'html.parser')
    index = soup.find('div', attrs={'class': 'bccblock', 'style': ''})
    index2 = index.find_all('div')
    valor_index = index2[1].text

    image = Image.open('imagem.jpg')

    editar_imagem = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=25)

    var = int(valor_index)* 5 - 20
    editar_imagem.text((int(var), 6), text=valor_index, fill=(0, 0, 0), font=font)

    image.save('imagemfinal.jpg')
    # embed_season = discord.Embed(title = 'Altcoin Season Index', color=discord.Color.blue())
    # embed_season.add_field(name=f'Bitcoin Season {23*"⠀"}Altcoin Season',value=f'{b}{valor_index}')
    # embed_season.set_image()
    # embed_season.set_image(url='https://i.imgur.com/KVqSnCS.jpg')
    # await ctx.send(embed=embed_season)

    await ctx.send(file=discord.File('imagemfinal.jpg'))


@client.command('ajuda')
async def ajuda(ctx):
    embed_ajuda = discord.Embed(title='COMANDOS DISPONIVEIS', description='$ + [comando]', color=discord.Color.blue())
    embed_ajuda.add_field(name= 'crypto [moeda]', value='Fornece algumas informacoes sobre a moeda requisitada')
    embed_ajuda.add_field(name='noticias [opcional : moeda]', value='Ultimas noticias sobre o mercado ou sobre a moeda requisitada')
    embed_ajuda.add_field(name='auto comecar', value='Manda noticias automaticamente a cada 1 hora no canal onde o comando foi enviado.Reseta a cada 6 horas')
    await ctx.send(embed=embed_ajuda)

@client.command('limpar')
async def limpar(ctx, amount = 0):
    await ctx.channel.purge(limit=amount)


client.run(discord_key)
