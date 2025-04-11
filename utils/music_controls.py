import discord
from discord.ui import View, Button
from discord import ButtonStyle
from commands.queuelist import create_queue_embed
from utils.queue_controls import QueueControlView
from utils.queues import queues

class MusicControlView(discord.ui.View):
    def __init__(self, guild_id, *, timeout=180):
        super().__init__(timeout=timeout)
        self.guild_id = guild_id
        
    @discord.ui.button(label="Play/Pause", style=ButtonStyle.success, emoji="⏯️")
    async def play_pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = interaction.guild.voice_client
        if not voice_client:
            await interaction.response.send_message("음성 채널에 연결되어 있지 않습니다.", ephemeral=True)
            return
        if voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("음악을 재개했습니다!", ephemeral=True)
        elif voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("음악을 일시정지했습니다!", ephemeral=True)
        else:
            await interaction.response.send_message("현재 재생 중인 음악이 없습니다.", ephemeral=True)
    
    @discord.ui.button(label="Skip", style=ButtonStyle.primary, emoji="⏭️")
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice_client = interaction.guild.voice_client
        if not voice_client or not voice_client.is_playing():
            await interaction.response.send_message("현재 재생 중인 음악이 없습니다.", ephemeral=True)
            return
            
        voice_client.stop()  # 현재 곡 중지, after 콜백 호출
        await interaction.response.send_message("현재 곡을 건너뛰었습니다!", ephemeral=True)
      
    @discord.ui.button(label="Clear", style=ButtonStyle.danger, emoji="🗑️")
    async def clear_queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.guild_id in queues:
            queues[self.guild_id].clear()
            await interaction.response.send_message("재생 대기열을 비웠습니다!", ephemeral=True)
        else:
            await interaction.response.send_message("재생 대기열이 이미 비어있습니다.", ephemeral=True)

    @discord.ui.button(label="Queue", style=ButtonStyle.secondary, emoji="📋")
    async def queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id
            
        if guild_id not in queues or not queues[guild_id]:
            await interaction.response.send_message("대기열이 비어 있습니다!", ephemeral=True)
            return

        try:
            embed = create_queue_embed(guild_id, page=0, items_per_page=10)
            view = QueueControlView(guild_id)
            
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"대기열 확인 중 오류: {str(e)}", ephemeral=True)