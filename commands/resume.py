import discord
from discord import app_commands
from commands.nowplaying import create_nowplaying_embed

@app_commands.command(name="resume", description="일시정지된 음악을 이어서 재생합니다.")
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if not voice_client or not voice_client.is_paused():
        await interaction.response.send_message("일시정지된 음악이 없습니다.", ephemeral=True)
        return

    try:
        voice_client.resume()
        player = voice_client.source
        embed = await create_nowplaying_embed(interaction, player)
        await interaction.response.send_message(content="▶️음악을 이어서 재생합니다!", embed=embed)

    except discord.ClientException as e:
        await interaction.response.send_message(f"이어서 재생 중 오류: {str(e)}", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"예기치 않은 오류 발생: {str(e)}", ephemeral=True)
