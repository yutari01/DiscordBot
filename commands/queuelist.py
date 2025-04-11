import discord
from discord import app_commands, Embed
from utils.queues import queues
from utils.queue_controls import QueueControlView

@app_commands.command(name="queue", description="현재 대기열을 확인합니다.")
async def queue(interaction: discord.Interaction):
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

def create_queue_embed(guild_id, page=0, items_per_page=10):
    # 대기열이 존재하는지 확인
    if guild_id not in queues or not queues[guild_id]:
        embed = Embed(title="🎶 현재 대기열", description="대기열이 비어 있습니다!", color=discord.Color.purple())
        return embed
    
    queue_list = list(queues[guild_id])
    total_songs = len(queue_list)
    
    # 페이지 계산
    max_pages = (total_songs + items_per_page - 1) // items_per_page
    current_page = min(page, max_pages - 1)
    
    # 현재 페이지에 표시할 항목 계산
    start_idx = current_page * items_per_page
    end_idx = min(start_idx + items_per_page, total_songs)
    
    # 임베드 생성
    embed = Embed(title="🎶 Music Queue", color=discord.Color.purple())
    
    # 항목 추가
    for i in range(start_idx, end_idx):
        embed.add_field(name=f"{i+1}.", value=queue_list[i], inline=False)
    
    # 푸터 설정
    if total_songs > items_per_page:
        embed.set_footer(text=f"Page {current_page + 1}/{max_pages} • Total {total_songs} songs in queue.")
    else:
        embed.set_footer(text=f"Total {total_songs} songs in queue.")
    
    return embed

