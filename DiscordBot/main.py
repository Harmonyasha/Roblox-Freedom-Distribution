import discord
from discord.ext import commands
import threading
from flask import Flask, request, jsonify, send_file, send_from_directory,url_for,redirect
import string
import random
import json,os,time
database = "Database.json"

if not os.path.exists(database):
    with open(database, "w") as f:
        f.write("{}")

data = json.load(open(database))
#{"127.0.0.1": {"discord": 407242708143570967, "robloxid": 3226873826}}
print(data)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
app = Flask(__name__,template_folder='pages/')
robloxcodesforverify = {}
prefix = ">cmd"
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix=prefix, description="", intents=intents)
bot.remove_command('help')
tree = bot.tree

@tree.command(name = "ping", description = "Pong!")
async def ping(ctx: discord.Interaction):
    await ctx.response.send_message('Pong! {0}'.format(bot.latency, 1),ephemeral=True) 

async def removekey(code,ctx: discord.Interaction):
    time.sleep(60*5)
    if code in robloxcodesforverify:
        await ctx.response.defer(ephemeral=True)
        await ctx.followup.send(f"Your code is timed out")
        del robloxcodesforverify[code]

@tree.command(name="link", description="Link your discord account with your roblox account")
async def link(ctx: discord.Interaction):
    code = None
    while code == None:
        tcode = id_generator(10)
        if not tcode in robloxcodesforverify:
            code = tcode
    robloxcodesforverify[code] = {"ip":None,"discord":ctx.user.id,"roblox account id":None}
    await ctx.response.defer(ephemeral=True)
    await ctx.followup.send(f"Click [this](http://46.8.232.164:8512/Join/{code}) and enter the code in roblox game **{code}**")


@app.route('/CodeValidation', methods=['POST'])
def CodeValidation():
    global data
    r = json.loads(request.get_data(as_text=True))
    if not r['code'] in robloxcodesforverify:
        return "Code not exist"
    if robloxcodesforverify[r['code']]["ip"] == None:
        return "Needed data not exist please click on link again"
    
    tdata = robloxcodesforverify[r['code']]
    data[tdata["ip"]] = {"discord":tdata["discord"],"robloxid":r['id']}

    open(database,"w").write(json.dumps(data))
    print("writed",json.dumps(data))
    

    del robloxcodesforverify[r['code']]
    return "You can join the game now!"



@app.route('/Join/<code>', methods=['GET'])
def joingame(code):
    client_ip = request.remote_addr
    if code in robloxcodesforverify:
        robloxcodesforverify[code]["ip"] = client_ip
        return redirect("https://www.roblox.com/games/18817456252/Verify")

@app.route('/IsAllowedToJoin', methods=['POST'])
def IsAllowedToJoin():
    r = json.loads(request.get_data(as_text=True))
    if r["addr"] in data:
        return str(data[r["addr"]]["robloxid"])
    return "False"

@bot.event
async def on_ready():
    print(f"logged as {bot.user.name}")
    await tree.sync()
    await bot.change_presence(status=discord.Status.idle, activity = discord.Streaming(name = "♡" , url =  "https://www.youtube.com/watch?v=8NdXENJJwWE"))
def runflask():
 app.run(host="0.0.0.0",port=8512)
threading.Thread(target=runflask,args=()).start()
bot.run("Bot token")