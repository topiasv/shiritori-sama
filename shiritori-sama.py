import discord
import asyncio
import unicodedata

client = discord.Client()
isGame = False
currentLetter = 'り'

def isKana(str):
    for c in str:
        unidata = unicodedata.name(c)
        if not unidata.startswith('HIRAGANA') and not unidata.startswith('KATAKANA'):
            return False
        else:
            return True

def isFirstCurrentKana(str):
    first = str[:1]
    if str[:1] == currentLetter:
        return True

def takeLastKana(str):
    global currentLetter
    if isKana(str):
        currentLetter = str[-1]

def isLastN(str):
    if str.endswith('ん'):
        return True

def shiritori(str, user):
    global isGame
    if isKana(str):
        if isFirstCurrentKana(str):
            if isLastN(str):
                isGame = False
                return 'Game over! ' + user.mention + ' said the word ' + str + ' ends with ん.'
            else:
                takeLastKana(str)
                return user.mention + ' said ' + str + '. Say a word starting with ' + currentLetter + '.'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    global isGame
    global currentLetter
    if message.author.id != client.user.id:
        if message.content.startswith('!st'):
            await client.send_message(message.channel, 'Starting a shiritori game. Input a word in Hiragana starting with り')
            isGame = True
            currentLetter = 'り'

        elif isGame and isFirstCurrentKana(message.content):
            msg = shiritori(message.content, message.author)
            if msg != "":
                await client.send_message(message.channel, msg)

client.run('CLIENT_TOKEN_HERE')
