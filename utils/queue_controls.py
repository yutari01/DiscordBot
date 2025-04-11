import discord
from discord import ButtonStyle
from utils.queues import queues

class QueueControlView(discord.ui.View):
    def __init__(self, guild_id, current_page=0, *, timeout=180):
        super().__init__(timeout=timeout)
        self.guild_id = guild_id
        self.current_page = current_page
        self.update_buttons()
        
    def update_buttons(self):
        queue_length = len(queues[self.guild_id]) if self.guild_id in queues else 0
        max_pages = (queue_length + 9) // 10  # 10개씩 표시할 때 필요한 페이지 수
        
        self.first_page_button.disabled = (self.current_page <= 0)
        self.prev_page_button.disabled = (self.current_page <= 0)
        self.next_page_button.disabled = (self.current_page >= max_pages - 1)
        self.last_page_button.disabled = (self.current_page >= max_pages - 1)
        
        self.page_info_button.label = f"Page {self.current_page + 1}/{max_pages}"
    
    @discord.ui.button(label="⏪First", style=ButtonStyle.primary)
    async def first_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = 0
        self.update_buttons()
        
        from commands.queuelist import create_queue_embed  # 순환 참조 방지를 위해 로컬 임포트
        embed = create_queue_embed(self.guild_id, self.current_page)
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="◀️", style=ButtonStyle.primary)
    async def prev_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = max(0, self.current_page - 1)
        self.update_buttons()
        
        from commands.queuelist import create_queue_embed
        embed = create_queue_embed(self.guild_id, self.current_page)
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="페이지 정보", style=ButtonStyle.secondary, disabled=True)
    async def page_info_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 이 버튼은 정보 표시용으로만 사용되므로 아무 작업도 수행하지 않음
        await interaction.response.defer()
    
    @discord.ui.button(label="▶️", style=ButtonStyle.primary)
    async def next_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        queue_length = len(queues[self.guild_id]) if self.guild_id in queues else 0
        max_pages = (queue_length + 9) // 10
        
        self.current_page = min(self.current_page + 1, max_pages - 1)
        self.update_buttons()
        
        from commands.queuelist import create_queue_embed
        embed = create_queue_embed(self.guild_id, self.current_page)
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Last⏩", style=ButtonStyle.primary)
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        queue_length = len(queues[self.guild_id]) if self.guild_id in queues else 0
        max_pages = (queue_length + 9) // 10
        
        self.current_page = max_pages - 1
        self.update_buttons()
        
        from commands.queuelist import create_queue_embed
        embed = create_queue_embed(self.guild_id, self.current_page)
        await interaction.response.edit_message(embed=embed, view=self)
    
