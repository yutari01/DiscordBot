import discord
from discord import app_commands

@app_commands.command(name="pause", description="현재 재생 중인 음악을 일시정지합니다.")
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if not voice_client or not voice_client.is_playing():
        await interaction.response.send_message("현재 재생 중인 음악이 없습니다.", ephemeral=True)
        return

    try:
        voice_client.pause()
        await interaction.response.send_message("⏸️음악을 일시정지했습니다!")

    except discord.ClientException as e:
        await interaction.response.send_message(f"일시정지 중 오류: {str(e)}", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"예기치 않은 오류 발생: {str(e)}", ephemeral=True)