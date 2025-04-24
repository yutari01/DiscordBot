import discord
import torch
from discord import app_commands
from utils.load_models import return_model, return_tokenizer
torch._dynamo.config.suppress_errors = True # Option 1: Suppress errors and fallback

@app_commands.command(name="chat", description="bitnet과 채팅을 할 수 있습니다.")
async def chat(interaction: discord.Interaction, *, message: str):
    # Defer the response first, as model loading can take time
    await interaction.response.defer(ephemeral=True)
    try:
        # Load tokenizer and model with trust_remote_code=True
        tokenizer = return_tokenizer()
        model = return_model()

        # Apply the chat template (using the user's message)
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": f"{message}"}, # <-- Use the actual message input
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        chat_input = tokenizer(prompt, return_tensors="pt").to(model.device) 

        chat_outputs = model.generate(**chat_input, max_new_tokens=150)
        response = tokenizer.decode(chat_outputs[0][chat_input['input_ids'].shape[-1]:], skip_special_tokens=True)

        await interaction.followup.send(response, ephemeral=True)

    except Exception as e:
        await interaction.followup.send(f"모델을 로드하거나 응답을 생성하는 중 오류가 발생했습니다: {e}", ephemeral=True)
        print(f"Error in chat command: {e}") # Log the error for debugging