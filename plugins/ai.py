# plugins/ai.py - AI-powered features
from telethon import events
import requests, json

async def register_handlers(client, bot):
    # ChatGPT-like responses
    @client.on(events.NewMessage(pattern=r'\.ask (.*)'))
    async def ai_handler(event):
        query = event.pattern_match.group(1)
        await event.reply("💭 Thinking...")
        
        try:
            # Using OpenAI API (replace with your API key)
            headers = {
                "Authorization": f"Bearer {os.getenv('OPENAI_KEY')}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": query}],
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                await event.reply(f"🤖 **Prince-X AI**\n\n{answer}")
            else:
                await event.reply(f"❌ API Error: {response.text}")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
    
    # Image generation with DALL-E
    @client.on(events.NewMessage(pattern=r'\.genimg (.*)'))
    async def genimg_handler(event):
        prompt = event.pattern_match.group(1)
        await event.reply("🎨 Generating image...")
        
        try:
            headers = {
                "Authorization": f"Bearer {os.getenv('OPENAI_KEY')}",
                "Content-Type": "application/json"
            }
            data = {
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024"
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                await event.reply(f"🖼️ **{prompt}**", file=image_url)
            else:
                await event.reply(f"❌ API Error: {response.text}")
        except Exception as e:
            await event.reply(f"❌ Error: {str(e)}")
