import discord
from discord import app_commands

@app_commands.command(
    name="join",
    description="봇을 음성 채널에 들어오게 합니다."
)
async def join(interaction: discord.Interaction):
    if not interaction.user.voice:
        await interaction.response.send_message("음성 채널에 연결 되어 있어야 합니다!", ephemeral=True)
        return
    
    try:
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client and interaction.guild.voice_client.channel == channel:
            await interaction.response.send_message(f"이미 {channel}에 연결되어 있습니다!", ephemeral=True)
            return
        await channel.connect()
        await interaction.response.send_message(f"{channel}에 참여했습니다!")

    except discord.ClientException as e:
        await interaction.response.send_message(f"음성 채널 참여 중 오류: {str(e)}", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"예기치 않은 오류 발생: {str(e)}", ephemeral=True)