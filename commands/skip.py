import discord
from discord import app_commands

@app_commands.command(name="skip", description="현재 재생 중인 곡을 건너뛰고 다음 곡을 재생합니다.")
async def skip(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if not voice_client or not voice_client.is_playing():
        await interaction.response.send_message("현재 재생 중인 음악이 없습니다.", ephemeral=True)
        return

    try:
        voice_client.stop()  # 현재 곡 중지, after 콜백 호출
        await interaction.response.send_message("⏭️현재 재생 중인 곡을 건너뛰고 다음 곡을 재생합니다!")

    except discord.ClientException as e:
        await interaction.response.send_message(f"건너뛰기 중 오류: {str(e)}", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"예기치 않은 오류 발생: {str(e)}", ephemeral=True)
