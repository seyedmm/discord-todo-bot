from discord.ext import commands
import discord
from discord.flags import alias_flag_value
import db_using
import asyncio
import time

client = commands.Bot(command_prefix='t:')
client.remove_command('help')
ok_url='https://i.imgur.com/n9bzswD.png'
oops_url='https://i.imgur.com/vCK001Y.png'
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('t:help'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command()
async def help(ctx):
    embed = discord.Embed(title='Help', description='Commands', color=0x00ff00)
    embed.add_field(name='t:help', value='این پیام رو نشون میده', inline=True)
    embed.add_field(name='t:add', value='یه کار جدید اضافه میکنه', inline=True)
    embed.add_field(name='t:remove <ID>', value='یه کارو با آیدیش حذف میکنه.', inline=True)
    embed.add_field(name='t:remove_all', value='همه کارارو حذف میکنه', inline=True)
    embed.add_field(name='t:list_all', value='لیست همه کارارو نشون میده', inline=True)
    embed.add_field(name='t:list_done', value='لیست همه لیست کارای انجام شده رو نشون میده', inline=True)
    embed.add_field(name='t:list_undone', value='لیست کارای انجام نشده رو نشون میده', inline=True)
    embed.add_field(name='t:view <ID>', value='اطلاعات یه کارو با آیدیش نشون میده', inline=True)
    embed.add_field(name='t:done <ID>', value='یه کارو با آیدیش بعنوان انجام شده تنظیم میکنه', inline=True)
    embed.add_field(name='t:undone <ID>', value='یه کارو با آیدیش به عنوان انجام نشده تنظیم میکنه', inline=True)
    await ctx.send(embed=embed)





@client.command()
async def add(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        await ctx.reply('عنوان کار رو بفرست')
        title_msg = await client.wait_for('message', timeout=60, check=check)
    except asyncio.TimeoutError:
        await ctx.send('جواب نمیدی؟ منم کنسل میکنم!:joy:')
    else:
        await ctx.send(f'عنوان ست شد: {title_msg.content}\nحالا توضیحات کار رو بفرست')
        try:
            task_msg = await client.wait_for('message', timeout=60, check=check)
        except asyncio.TimeoutError:
            await ctx.send('جواب نمیدی؟ منم کنسل میکنم!:joy:')
        else:
            db_using.add(str(title_msg.content),str(task_msg.content))
            await ctx.send(f'کار با این مشخصات اضافه شد:\nعنوان: ***{title_msg.content}***\nتوضیحات: ***{task_msg.content}***\nآیدی: ***{db_using.view_all()[-1][0]}***')




@client.command(aliases=['all'])
async def list_all(ctx):
    embed = discord.Embed(title='لیست همه کار ها:', description='انجام شده یا انجام نشده فرقی نداره. همشون توی لیستن', color=0x00ff00)
    embed.set_footer(text=f'{len(db_using.view_all())} کار',icon_url='https://image.flaticon.com/icons/png/512/906/906334.png')
    for i in db_using.view_all():
        if i[-1] == 1:
            done_txt = 'انجام دادی'
        else:
            done_txt = 'انجام ندادی'
        embed.add_field(name=f'{i[1]}',value=f'>>> ***عنوان:***\n{i[1]}\n***توضیحات:***\n{i[2]}\n***آیدی:***\n{i[0]}\n{done_txt}\n',inline=False)

    await ctx.send(embed=embed)
            


@client.command()
async def list_done(ctx):
    embed = discord.Embed(title='لیست انجام شده ها:', description='فقط انجام شده ها توی لیستن', color=0x00ff00)
    embed.set_footer(text=f'{len(db_using.view_done())} کار انجام شده',icon_url='https://image.flaticon.com/icons/png/512/906/906334.png')
    for i in db_using.view_done():
        embed.add_field(name=f'{i[1]}',value=f'>>> ***عنوان:***\n{i[1]}\n***توضیحات:***\n{i[2]}\n***آیدی:***\n{i[0]}\n\n',inline=False)
    await ctx.send(embed=embed)



@client.command()
async def list_undone(ctx):
    embed = discord.Embed(title='لیست انجام نشده ها:', description='فقط انجام نشده ها توی لیستن', color=0x00ff00)
    embed.set_footer(text=f'{len(db_using.view_undone())} کار انجام نشده',icon_url='https://image.flaticon.com/icons/png/512/906/906334.png')
    for i in db_using.view_undone():
        embed.add_field(name=f'{i[1]}',value=f'>>> ***عنوان:***\n{i[1]}\n***توضیحات:***\n{i[2]}\n***آیدی:***\n{i[0]}\n\n',inline=False)
    await ctx.send(embed=embed)


@client.command()
async def view(ctx, id):
    task = db_using.view_one(id)
    if task != None:
        if task[-1] == 1:
            done_txt = 'انجام دادی'
        else:
            done_txt = 'انجام ندادی'
        embed= discord.Embed(title= task[1],description=f'{task[2]}\n-----------\n{done_txt}',color=0x0ff000)
        await ctx.reply(embed=embed)
    else:
        oops_embed = discord.Embed(title='پیدا نشد!',description=f'مطمئنی آیدی *{id}* وجود داره؟!',color=0x00ff00)
        oops_embed.set_thumbnail(url=oops_url)
        await ctx.reply(embed=oops_embed)





@client.command(aliases=['delete'])
async def remove(ctx,id):
    rows = db_using.view_all()
    ids = [str(row[0]) for row in rows]
    print(ids)
    print(rows)
    if id in ids:
        try:
            db_using.delete(id)
        except:
            oops_embed = discord.Embed(title='حذف نشد!',description=f'کار با آیدی *{id}* حذف نشد!',color=0x00ff00)
            oops_embed.set_thumbnail(url=oops_url)
            await ctx.reply(embed=oops_embed)
        else:
            ok_embed = discord.Embed(title='حذف شد!',description=f'کار با آیدی *{id}* حذف شد!',color=0x00ff00)
            ok_embed.set_thumbnail(url=ok_url)
            await ctx.reply(embed=ok_embed)
    else:
        oops_embed = discord.Embed(title='حذف نشد!',description=f'مطمئنی آیدی *{id}* وجود داره؟!',color=0x00ff00)
        oops_embed.set_thumbnail(url=oops_url)
        await ctx.reply(embed=oops_embed)



@client.command(aliases=['delete_all'])
async def remove_all(ctx):
    rows = db_using.view_all()
    if len(rows) != 0:
        try:
            db_using.delete_all()
        except:
            oops_embed = discord.Embed(title='حذف نشد!',description=f'کارها حذف نشدن =(',color=0x00ff00)
            oops_embed.set_thumbnail(url=oops_url)
            await ctx.reply(embed=oops_embed)
        else:
            ok_embed = discord.Embed(title='حذف شد!',description=f'کار ها حذف شدن =)',color=0x00ff00)
            ok_embed.set_thumbnail(url=ok_url)
            await ctx.reply(embed=ok_embed)
    else:
        oops_embed = discord.Embed(title='حذف نشد!',description=f'لیست کار خالیه. چجوری میخوای خالی ترش کنی؟',color=0x00ff00)
        oops_embed.set_thumbnail(url=oops_url)
        await ctx.reply(embed=oops_embed)



@client.command()
async def done(ctx,id):
    rows = db_using.view_all()
    ids = [str(row[0]) for row in rows]
    if id in ids:
        for i in rows:
            if str(i[0]) == id:
                task_row = i
        if task_row[-1] == 0:
            try:
                db_using.done(id)
            except:
                oops_embed = discord.Embed(title='انجام نشد!',description=f'نتونستم کار *{task_row[1]}* رو به عنوان انجام شده علامت بزنم',color=0x00ff00)
                oops_embed.set_thumbnail(url=oops_url)
                await ctx.reply(embed=oops_embed)
            else:
                ok_embed = discord.Embed(title='اوکیه :slight_smile:',description=f'کار *{task_row[1]}* به عنوان انجام شده علامت خورد!',color=0x00ff00)
                ok_embed.set_thumbnail(url=ok_url)
                await ctx.reply(embed=ok_embed)
        else:
            oops_embed = discord.Embed(title='انجام نشد!',description=f'کار *{task_row[1]}* رو قبلا به عنوان انجام شده علامت زدی =|',color=0x00ff00)
            oops_embed.set_thumbnail(url=oops_url)
            await ctx.reply(embed=oops_embed)
    else:
        oops_embed = discord.Embed(title='انجام نشد!',description=f'مطمئنی آیدی *{id}* وجود داره؟!',color=0x00ff00)
        oops_embed.set_thumbnail(url=oops_url)
        await ctx.reply(embed=oops_embed)
            



@client.command()
async def undone(ctx,id):
    rows = db_using.view_all()
    ids = [str(row[0]) for row in rows]
    if id in ids:
        for i in rows:
            if str(i[0]) == id:
                task_row = i
        if int(task_row[-1]) == 1:
            try:
                db_using.undone(id)
            except:
                oops_embed = discord.Embed(title='انجام نشد!',description=f'نتونستم کار *{task_row[1]}* رو به عنوان انجام نشده علامت بزنم',color=0x00ff00)
                oops_embed.set_thumbnail(url=oops_url)
                await ctx.reply(embed=oops_embed)
            else:
                ok_embed = discord.Embed(title='اوکیه :slight_smile:',description=f'کار *{task_row[1]}* به عنوان انجام نشده علامت خورد!',color=0x00ff00)
                ok_embed.set_thumbnail(url=ok_url)
                await ctx.reply(embed=ok_embed)
        else:
            oops_embed = discord.Embed(title='انجام نشد!',description=f'کار *{task_row[1]}* رو کلا انجام ندادی که بخوای دوباره انجام نشدش کنی =|',color=0x00ff00)
            oops_embed.set_thumbnail(url=oops_url)
            await ctx.reply(embed=oops_embed)
    else:
        oops_embed = discord.Embed(title='انجام نشد!',description=f'مطمئنی آیدی *{id}* وجود داره؟!',color=0x00ff00)
        oops_embed.set_thumbnail(url=oops_url)
        await ctx.reply(embed=oops_embed)







@client.command()
async def edit_title(ctx, id, *, new):
    rows = db_using.view_all()
    ids = [str(row[0]) for row in rows]
    if id in ids:
        for i in rows:
            if str(i[0]) == id:
                task_row = i
        try:
            db_using.edit_title(new,id)
        except:
            oops_embed = discord.Embed(title='انجام نشد!',description=f'نتونستم کار *{task_row[1]}* رو ویرایش کنم',color=0x00ff00)
            oops_embed.set_thumbnail(url=oops_url)
            await ctx.reply(embed=oops_embed)
        else:
            ok_embed = discord.Embed(title='اوکیه :slight_smile:',description=f'کار *{task_row[1]}* ویرایش شد!',color=0x00ff00)
            ok_embed.set_thumbnail(url=ok_url)
            await ctx.reply(embed=ok_embed)
    else:
        oops_embed = discord.Embed(title='انجام نشد!',description=f'مطمئنی آیدی *{id}* وجود داره؟!',color=0x00ff00)
        oops_embed.set_thumbnail(url=oops_url)
        await ctx.reply(embed=oops_embed)




@client.command()
async def edit_task(ctx, id, *, new):
    rows = db_using.view_all()
    ids = [str(row[0]) for row in rows]
    if id in ids:
        for i in rows:
            if str(i[0]) == id:
                task_row = i
        try:
            db_using.edit_task(new,id)
        except:
            oops_embed = discord.Embed(title='انجام نشد!',description=f'نتونستم کار *{task_row[1]}* رو ویرایش کنم',color=0x00ff00)
            oops_embed.set_thumbnail(url=oops_url)
            await ctx.reply(embed=oops_embed)
        else:
            ok_embed = discord.Embed(title='اوکیه :slight_smile:',description=f'کار *{task_row[1]}* ویرایش شد!',color=0x00ff00)
            ok_embed.set_thumbnail(url=ok_url)
            await ctx.reply(embed=ok_embed)
    else:
        oops_embed = discord.Embed(title='انجام نشد!',description=f'مطمئنی آیدی *{id}* وجود داره؟!',color=0x00ff00)
        oops_embed.set_thumbnail(url=oops_url)
        await ctx.reply(embed=oops_embed)









client.run('ODc5MDkzMzgxMDM1MzI3NTI5.YSKtgg.Y-VG2N1d-kBid7677kLMVORbXQs')