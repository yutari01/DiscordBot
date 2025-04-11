import discord
from discord import app_commands
from utils.queues import queues

@app_commands.command(name="leave", description="봇을 음성 채널에서 나가게 합니다.")
async def leave(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if not voice_client or not voice_client.is_connected():
        await interaction.response.send_message("음성 채널에 연결되어 있지 않습니다!", ephemeral=True)
        return
        
    try:
        guild_id = interaction.guild.id
        if guild_id in queues:
            queues[guild_id].clear()
        await voice_client.disconnect()
        await interaction.response.send_message("음성 채널에서 나갔습니다!")

    except discord.ClientException as e:
        await interaction.response.send_message(f"음성 채널 나가기 중 오류: {str(e)}", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"예기치 않은 오류 발생: {str(e)}", ephemeral=True)
