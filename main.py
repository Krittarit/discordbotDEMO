import os
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View

from myserver import server_on

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# //////////////////// Bot Event /////////////////////////
@bot.event
async def on_ready():
    print("Bot Online!")
    print("555")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s)")

# คำสั่ง chatbot
@bot.event
async def on_message(message):
    mes = message.content  # ดึงข้อความที่ถูกส่งมา
    if mes == 'สวัสดีครับ':  # เมื่อผู้ใช้พิมพ์ "สวัสดีครับ"
        # ส่งข้อความตอบกลับ
        await message.channel.send(
            "มีอะไรให้รับใช้ครับ? กรุณาเลือกสิ่งที่ต้องการรู้จากเมนูด้านล่าง",
            view=DropdownMenu()  # เพิ่มเมนู dropdown
        )

    await bot.process_commands(message)

# สร้างเมนู dropdown
class DropdownMenu(View):
    def __init__(self):
        super().__init__()

        # เพิ่มตัวเลือกใน dropdown
        self.add_item(SelectMenu())

class SelectMenu(Select):
    def __init__(self):
        # สร้าง dropdown กับตัวเลือก
        options = [
            discord.SelectOption(label="Stock", description="ดูสถานะของ stock", emoji="📦"),
            discord.SelectOption(label="ช่องทางชำระเงิน", description="ดูช่องทางการชำระเงิน", emoji="💳")
        ]
        super().__init__(placeholder="เลือกสิ่งที่คุณต้องการ", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # เมื่อลงคะแนนเลือกตัวเลือกแล้ว
        if self.values[0] == "Stock":
            await interaction.response.send_message("ข้อมูลเกี่ยวกับ stock จะถูกแสดงที่นี่")
        elif self.values[0] == "ช่องทางชำระเงิน":
            await interaction.response.send_message("ข้อมูลเกี่ยวกับช่องทางชำระเงินจะถูกแสดงที่นี่")

# ///////////////////// Commands /////////////////////
@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}!")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# Slash Commands
@bot.tree.command(name='hellobot', description='Replies with Hello')
async def hellocommand(interaction):
    await interaction.response.send_message("Hello It's me BOT DISCORD")

@bot.tree.command(name='name')
@app_commands.describe(name="What's your name?")
async def namecommand(interaction, name: str):
    await interaction.response.send_message(f"Hello {name}")

# Embeds
@bot.tree.command(name='help', description='Bot Commands')
async def helpcommand(interaction):
    emmbed = discord.Embed(title='Help Me! - Bot Commands',
                           description='Bot Commands',
                           color=0x66FFFF,
                           timestamp=discord.utils.utcnow())
    emmbed.add_field(name='/hello1', value='Hello Commmand', inline=True)
    emmbed.add_field(name='/hello2', value='Hello Commmand', inline=True)
    emmbed.add_field(name='/hello3', value='Hello Commmand', inline=False)
    emmbed.set_author(name='Author', url='https://www.youtube.com/@maoloop01/channels', icon_url='https://yt3.googleusercontent.com/0qFq3tGT6LVyfLtZc-WCXcV9YyEFQ0M9U5W8qDe36j2xBTN34CJ20dZYQHmBz6aXASmttHI=s900-c-k-c0x00ffffff-no-rj')
    emmbed.set_thumbnail(url='https://yt3.googleusercontent.com/0qFq3tGT6LVyfLtZc-WCXcV9YyEFQ0M9U5W8qDe36j2xBTN34CJ20dZYQHmBz6aXASmttHI=s900-c-k-c0x00ffffff-no-rj')
    emmbed.set_image(url='https://i.ytimg.com/vi/KZRa9DQzUpQ/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCfWDgiBYjFJtrUasd5yxmQZJG_cg')
    emmbed.set_footer(text='Footer', icon_url='https://yt3.googleusercontent.com/0qFq3tGT6LVyfLtZc-WCXcV9YyEFQ0M9U5W8qDe36j2xBTN34CJ20dZYQHmBz6aXASmttHI=s900-c-k-c0x00ffffff-no-rj')
    await interaction.response.send_message(embed=emmbed)

server_on()

bot.run(os.getenv('TOKEN'))
