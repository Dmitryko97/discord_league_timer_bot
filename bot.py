import discord
from timer import timer

token = open('server_token.txt', 'r').read()
client = discord.Client()

spells = ['heal', 'ghost', 'barrier', 'exhaust', 'clarity', 'flash', 'teleport', 'cleanse', 'ignite']
roles = ['top', 'jungle', 'mid', 'adc', 'support']


def start_cd_checker(message):
    split = message.split(' ')
    
    if not(len(split) == 4):
        print(len(split))
        return None
    elif roles.index(split[2]) == -1:
        print(split[2])
        return None
    elif spells.index(split[3]) == -1:
        print(split[3])
        return None
    
    return (split[2], split[3])

def get_cd_checker(message):
    split = message.split(' ')
    
    if not(len(split) == 3):
        print(len(split))
        return None
    elif roles.index(split[2]) == -1:
        print(split[2])
        return None
    
    return split[2]

@client.event
async def on_ready():
    global game
    game = None
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global game
    #print(f'{message.channel}: {message.author}: {message.author.name}: {message.content}')
    if not message.author.bot:
        
        if 'exit' in message.content:
            await client.close()

        elif 'start' == message.content:
            if game is None:
                game = timer()
                await message.channel.send("Game started!")
            else:
                await message.channel.send("Game allready ongoing. Use 'end game' to stop existing game.")

        elif 'end' == message.content:
            game = None
            await message.channel.send("Game ended!")  

        elif 'time' == message.content:
            if game is not None:
                await message.channel.send(f"Game time: {game.get_match_time()}")
            else:
                await message.channel.send("No active game")

        elif message.content.startswith('start cd'):
            try:
                if game is not None:
                    role, spell = start_cd_checker(message.content)
                    game.start_cooldowns_for_spells(role, spell)
                    await message.channel.send(f"```{game.get_spells_uptime(role)}\n```")
                else:
                    await message.channel.send("No active game")
            except Exception as e:
                print(e)
                await message.channel.send("Invalid syntax. The command is: 'start cd {role} {spell}'")

        elif message.content.startswith('get cd'):
            try:
                if game is not None:
                    role = get_cd_checker(message.content)
                    await message.channel.send(f"```{game.get_spells_uptime(role)}\n```")
                else:
                    await message.channel.send("No active game")
            except Exception as e:
                print(e)
                await message.channel.send("Invalid syntax. The command is: 'get cd {role}'")

        elif 'get all cd' == message.content:
            if game is not None:
                await message.channel.send(f"```{game.get_spells_uptime_all()}```")
            else:
                await message.channel.send("No active game")
            

client.run(token)
