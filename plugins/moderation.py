# plugins/moderation.py - Moderation tools
from telethon import events, types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

async def register_handlers(client, bot):
    # Ban user command
    @client.on(events.NewMessage(pattern=r'\.ban', from_users=admins))
    async def ban_handler(event):
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            user = await reply.get_sender()
            try:
                await client(EditBannedRequest(
                    event.chat_id,
                    user.id,
                    ChatBannedRights(until_date=None, view_messages=True)
                ))
                await event.reply(f"🚫 **Banned** [{user.first_name}](tg://user?id={user.id})")
            except Exception as e:
                await event.reply(f"❌ Error: {str(e)}")
        else:
            await event.reply("Reply to a user to ban them")
    
    # Mute user command
    @client.on(events.NewMessage(pattern=r'\.mute', from_users=admins))
    async def mute_handler(event):
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            user = await reply.get_sender()
            try:
                await client.edit_permissions(
                    event.chat_id,
                    user.id,
                    send_messages=False
                )
                await event.reply(f"🔇 **Muted** [{user.first_name}](tg://user?id={user.id})")
            except Exception as e:
                await event.reply(f"❌ Error: {str(e)}")
        else:
            await event.reply("Reply to a user to mute them")
    
    # Purge messages command
    @client.on(events.NewMessage(pattern=r'\.purge', from_users=admins))
    async def purge_handler(event):
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            from_id = reply.id
            to_id = event.id
            
            msg_ids = []
            async for msg in client.iter_messages(
                event.chat_id,
                min_id=from_id,
                max_id=to_id
            ):
                msg_ids.append(msg.id)
            
            await client.delete_messages(event.chat_id, msg_ids)
            count = len(msg_ids)
            result = await event.reply(f"🧹 **Purged** `{count}` messages")
            await asyncio.sleep(3)
            await result.delete()
        else:
            await event.reply("Reply to a message to start purging")

# Admin list (replace with your admins)
admins = [123456789]  # Your admin user IDs
