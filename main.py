from scraper import Scraper
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Prefix for Bot
client = commands.Bot(command_prefix="$")

@client.event
async def on_ready():
    """
    Initiates Bot
    """
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('My Academic Results'))
    print('Bot is ready')

@client.command()
async def scrape(ctx, *, request):
    output = request.split(" ")
    year, unit = output[0], output[1]
    output_string_assessments, unit_code, output_string_chief_examiners = run_scraper(year, unit)
    embedVar = discord.Embed(title="Unit Description", color=0x00ff00)
    embedVar.add_field(name="Unit Code", value=unit_code, inline=False)
    embedVar.add_field(name="Chief Examiner(s)", value=output_string_chief_examiners, inline=False)
    embedVar.add_field(name="Assessments", value=output_string_assessments, inline=False)
    await ctx.channel.send(embed=embedVar)


def run_scraper(year, unit):
    scraper = Scraper(year, unit)
    assessments = scraper.getassessments()
    unit_code = scraper.getunitcode()
    chief_examiners = scraper.getchiefexaminers()
    output_string_chief_examiners = ""
    output_string_assessments = ""
    for j in range(len(chief_examiners)):
        output_string_chief_examiners += f'Chief Examiner(s): {chief_examiners[j]}\n'
    for i in range(len(assessments[0])):
        output_string_assessments += f'Assessment {i+1}: {assessments[0][i]}\nWeightage: {assessments[1][i]}%\n'
    return output_string_assessments, str(unit_code), output_string_chief_examiners

# def output(assessments, unit_code, chief_examiners):
    
    # return embedVar

# Runs Client depending on Client Token
client.run(os.getenv('TOKEN'))