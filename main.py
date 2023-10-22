import re, os, asyncio, random, string
from discord.ext import commands, tasks

version = 'v2.7'

user_token = os.environ['user_token']
spam_id = os.environ['spam_id']
report_id = os.environ['report_id']

with open('pokemon','r', encoding='utf8') as file:
    pokemon_list = file.read()
with open('mythical','r') as file:
    mythical_list = file.read()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0

poketwo = 716390085896962058
client = commands.Bot(command_prefix= '????' )
intervals = [5.0, 5.2, 5.4, 5.6, 5.8]

def solve(message, file_name):
    hint = []
    for i in range(15,len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''
    for i in hint:
        hint_string += i
    hint_replaced = hint_string.replace('_', '.')
    with open(f"{file_name}", "r") as f:
        solutions = f.read()
    solution = re.findall('^'+hint_replaced+'$', solutions, re.MULTILINE)
    if len(solution) == 0:
        return None
    return solution

@tasks.loop(seconds=random.choice(intervals))
async def spam():
    channel = client.get_channel(int(spam_id))
    await channel.send(''.join(random.sample(['1','2','3','4','5','6','7','8','9','0'],7)*5))

async def on_ready():
    print(f'Logged into account: {client.user.name}')
    guild = client.guilds[0]

@spam.before_loop
async def before_spam():
    await client.wait_until_ready()

spam.start()
@client.event
async def on_ready():
    print(f'Logged into account: {client.user.name}')


@client.event
async def on_message(message):
    channel = client.get_channel(message.channel.id)
    guild = message.guild
    category = channel.category
    # Check if message is from Poketwo
    if message.author.id == poketwo:
      if message.channel.category.name == 'catch':
        # Check if message contains Pokemon embed
        if message.embeds:
            embed_title = message.embeds[0].title
            if 'wild pokémon has appeared!' in embed_title:
                await asyncio.sleep(1)
                await channel.send('<@716390085896962058> h')
        else:
            content = message.content
            solution = None
            
            # Try to solve the Pokemon name from the message content
            if 'The pokémon is ' in content:
                       solution = solve(content, 'pokemon')
                       if solution:
                        await asyncio.sleep(2)
                        await channel.send(f'<@716390085896962058> c {solution[0]}')
                        await asyncio.sleep(2)
            if 'Congratulations' in content:
              await asyncio.sleep(2)
            if 'human' in content:
                    spam.cancel()
                    await channel.send(f'<@{report_id}> Reboot')
                    print('Captcha detected; autocatcher paused. Resume Manually, after solving captcha manually.')
    if not message.author.bot:
         await client.process_commands(message)
            
@client.command()
async def report(ctx, *, args):
  await ctx.send(args)

@client.command()
async def reboot(ctx):
  spam.start()

@client.command()
async def pause(ctx):
  spam.cancel()





client.run(f"{user_token}")
