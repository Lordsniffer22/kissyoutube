import os
from pytube import YouTube
from telegram import Bot
from telegram import InputFile

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '6675228824:AAFdQYBLNl8OYQ581dOlZLv0mcqK4c4iP9U'

# Function to download a YouTube video and send it to a Telegram chat
def download_and_forward_video(video_url, chat_id, bot):
    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if stream:
        video_path = stream.download()
        with open(video_path, 'rb') as video_file:
            bot.send_video(chat_id=chat_id, video=InputFile(video_file))
        os.remove(video_path)
    else:
        print('No suitable video stream found.')

# Main function to handle Telegram messages
def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    # Function to handle incoming messages
    def handle_messages(update, context):
        chat_id = update.effective_chat.id
        text = update.message.text

        if text.startswith('https://youtu.be/') or text.startswith('http://www.youtube.com/watch?v='):
            download_and_forward_video(text, chat_id, bot)
        else:
            bot.send_message(chat_id=chat_id, text='Please send a valid YouTube video link.')

    # Start polling for messages
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    updater.dispatcher.add_message_handler(handle_messages)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
