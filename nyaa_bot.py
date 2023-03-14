import telegram
import requests
from bs4 import BeautifulSoup

bot = telegram.Bot(token='5917925714:AAEFZ_MAEluZ7iM160gieMfKKQ-YAAMAjw0')

def search_torrents(query):
    search_url = 'https://nyaa.si/?q=' + query.replace(' ', '+')
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    torrents = []
    for row in soup.select('tbody tr'):
        cells = row.select('td')
        title = cells[1].text.strip()
        magnet_link = cells[2].select('a')[1]['href']
        torrent = {
            'title': title,
            'magnet_link': magnet_link
        }
        torrents.append(torrent)
    return torrents

def download_torrent(magnet_link):
    response = requests.get(magnet_link)
    return response.content

def upload_torrent(torrent_bytes):
    bot.send_document(chat_id='1083036384', document=torrent_bytes)

def handle_message(update, context):
    text = update.message.text
    if text.startswith('/search'):
        query = text.replace('/search', '').strip()
        torrents = search_torrents(query)
        for torrent in torrents:
            bot.send_message(chat_id=update.effective_chat.id, text=torrent['title'])
    elif text.startswith('/download'):
        magnet_link = text.replace('/download', '').strip()
        torrent_bytes = download_torrent(magnet_link)
        upload_torrent(torrent_bytes)

from telegram.ext import Updater, MessageHandler, Filters

updater = Updater(token='5917925714:AAEFZ_MAEluZ7iM160gieMfKKQ-YAAMAjw0', use_context=True)

updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

updater.start_polling()
