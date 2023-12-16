import asyncio

from prettytable import PrettyTable
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from Zaid import app, CMD_HELP
from Zaid.helper.PyroHelpers import ReplyCheck
from Zaid.helper.utility import split_list


async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    xyz = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await xyz(*args, **kwargs)

@Client.on_message(filters.command(["help", "helpme"], ".") & filters.me)
async def module_help(client: Client, message: Message):
    cmd = message.command
    help_arg = ""
    bot_username = (await app.get_me()).username
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:])
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("🤖")
        try:
            nice = await client.get_inline_bot_results(bot=bot_username, query="helper")
            await asyncio.gather(
                message.delete(),
                client.send_inline_bot_result(
                    message.chat.id, nice.query_id, nice.results[0].id
                ),
            )
        except BaseException as e:
            print(f"{e}")
            ac = PrettyTable()
            ac.header = False
            ac.title = "࿈ 𝐖ᴀsᴛᴇʀ┘"
            ac.align = "l"
            for x in split_list(sorted(CMD_HELP.keys()), 2):
                ac.add_row([x[0], x[1] if len(x) >= 2 else None])
            xx = await client.send_message(
                message.chat.id,
                f"```{str(ac)}```\n⤷ @TSO_CHATS\n⤷ @GODX_BOTS",
                reply_to_message_id=ReplyCheck(message),
            )
            await xx.reply(
                f"**𝐔sᴀɢᴇ :** `.help raid` \n𝐓ᴏ 𝐕ɪᴇᴡ 𝐌ᴏᴅᴜʟᴇ 𝐈ɴғᴏʀᴍᴀᴛɪᴏɴ"
            )
            return

    if help_arg:
        if help_arg in CMD_HELP:
            commands: dict = CMD_HELP[help_arg]
            this_command = f"──「 **𝐇ᴇʟᴘ 𝐅ᴏʀ {str(help_arg).upper()}** 」──\n\n"
            for x in commands:
                this_command += f"  •  **Command:** `.{str(x)}`\n  •  **Function:** `{str(commands[x])}`\n\n"
            this_command += "@GODX_BOTS"
            await edit_or_reply(
                message, this_command, parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await edit_or_reply(
                message,
                f"`{help_arg}` **𝐍ᴏᴛ 𝐀 𝐕ᴀʟɪᴅ 𝐌ᴏᴅᴜʟᴇ 𝐍ᴀᴍᴇ**",
            )


@Client.on_message(filters.command(["plugins", "modules"], ".") & filters.me)
async def module_helper(client: Client, message: Message):
    cmd = message.command
    help_arg = ""
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        help_arg = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        ac = PrettyTable()
        ac.header = False
        ac.title = "࿈ 𝐖ᴀsᴛᴇʀ┘"
        ac.align = "l"
        for x in split_list(sorted(CMD_HELP.keys()), 2):
            ac.add_row([x[0], x[1] if len(x) >= 2 else None])
        await edit_or_reply(
            message, f"```{str(ac)}```\n⤷ @TSO_CHATS\n⤷ @GODX_BOTS"
        )
        await message.reply(
            f"**𝐔sᴀɢᴇ**:`.help raid` **𝐓ᴏ 𝐕ɪᴇᴡ 𝐌ᴏᴅᴜʟᴇ 𝐃ᴇᴛᴀɪʟs**"
        )

    if help_arg:
        if help_arg in CMD_HELP:
            commands: dict = CMD_HELP[help_arg]
            this_command = f"──「 **𝐇ᴇʟᴘ 𝐅ᴏʀ {str(help_arg).upper()}** 」──\n\n"
            for x in commands:
                this_command += f"  •  **Command:** `.{str(x)}`\n  •  **Function:** `{str(commands[x])}`\n\n"
            this_command += "@GODX_BOTS"
            await edit_or_reply(
                message, this_command, parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await edit_or_reply(
                message,
                f"`{help_arg}` **𝐍ᴏᴛ 𝐀 𝐕ᴀʟɪᴅ 𝐌ᴏᴅᴜʟᴇ 𝐍ᴀᴍᴇ**",
            )


def add_command_help(module_name, commands):
    if module_name in CMD_HELP.keys():
        command_dict = CMD_HELP[module_name]
    else:
        command_dict = {}

    for x in commands:
        for y in x:
            if y is not x:
                command_dict[x[0]] = x[1]

    CMD_HELP[module_name] = command_dict
