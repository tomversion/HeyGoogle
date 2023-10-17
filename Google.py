import logging
import telebot
import requests
import urllib.parse
import random
from bs4 import BeautifulSoup
import json
import time



# Replace with your Google Search API key
API_KEY = 'AIzaSyCF9Gd6R_0BmQvXTLy7oTn8lW2mJ4eR56o'

# Replace with your Google Search Engine ID
SEARCH_ENGINE_ID = '56dc72e5bd2ff43ca'

# Create a bot instance
bot = telebot.TeleBot('6131824040:AAEf1Gay3d_1cqCpEWsWU2BpKHGJl1kjUJA')



# Define the path to the file where chat IDs will be saved
CHAT_IDS_FILE = 'chat_ids.json'

# Load saved chat IDs from the file
try:
    with open(CHAT_IDS_FILE, 'r') as f:
        chat_ids = set(json.load(f))
except FileNotFoundError:
    # If the file doesn't exist, start with an empty set
    chat_ids = set()

# Use the message handler decorator to handle /start commands
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Get the chat ID of the user who sent the message
    chat_id = message.chat.id
    # If the chat ID is not in the set, add it and send welcome message
    if chat_id not in chat_ids:
        chat_ids.add(chat_id)
        # Save the updated chat IDs to the file
        with open(CHAT_IDS_FILE, 'w') as f:
            json.dump(list(chat_ids), f)

    # Send a welcome message to the user
    bot.send_message(chat_id, "Welcome to my bot!\n\n" +
                    "Send /joke to get a joke,\n" +
                    "Send /search to search on Wikipedia,\n" +
                    "Send /image to get an image from Google, and\n" +
                    "Send /surprise for a surprise message! ")



# Define a function to handle the /search command
@bot.message_handler(commands=['search'])
def search(message):
    query = message.text.replace('/search', '').strip()
    if not query:
        bot.send_message(chat_id=message.chat.id, text="Please enter a valid search query.")
        return
    try:
        url = 'https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=' + SEARCH_ENGINE_ID + '&q=' + urllib.parse.quote_plus(query)
        response = requests.get(url)
        response.raise_for_status()
        results = response.json().get('items', [])
        if not results:
            bot.send_message(chat_id=message.chat.id, text="No results found for the search query.")
            return
        # Send the first 10 links
        for result in results[:10]:
            bot.send_message(chat_id=message.chat.id, text=result['link'])
    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        bot.send_message(chat_id=message.chat.id, text="Something went wrong while searching. Please try again later.")
    except Exception as err:
        logger.error(f'An unexpected error occurred: {err}')
        bot.send_message(chat_id=message.chat.id, text="An unexpected error occurred. Please try again later.")



# Define the /image command handler
@bot.message_handler(commands=['image'])
def handle_image_command(message):
    # Get the search query from the message text
    search_query = message.text[7:]

    # Send a message to indicate that the bot is searching for images
    bot.send_message(message.chat.id, "Searching for images...")

    try:
        # Make the API request to Google Custom Search API
        search_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_query}&searchType=image"
        response = requests.get(search_url)
        json_data = response.json()

        # Extract the image results from the response
        image_urls = []
        for item in json_data['items']:
            if 'link' in item:
                image_urls.append(item['link'])

        # Send the images to the user
        if image_urls:
            for url in image_urls:
                bot.send_photo(message.chat.id, url)
        else:
            bot.reply_to(message, "Sorry, no images found for your query.")
    except:
        bot.reply_to(message, "Unexpected error. Please try again later.")


@bot.message_handler(commands=['surprise'])
def send_surprise(message):
    print("Inside send_surprise function")
    response = requests.get('https://www.reddit.com/r/nosleep/new.json?sort=top', headers={'User-Agent': 'Mozilla/5.0'}).json()
    print(response)
    data = response['data']['children']
    random_post = random.choice(data)['data']
    title = random_post['title']
    text = random_post['selftext']
    link = random_post['url']
    message_to_send = f"Title: {title}\n\n{text}\n\nRead more: {link}"
    if len(message_to_send) > 4000:
        message_to_send = message_to_send[:4000] + "..."
    bot.reply_to(message, message_to_send)




@bot.message_handler(commands=['joke'])
def joke(message):
    url = 'https://official-joke-api.appspot.com/random_joke'
    response = requests.get(url)
    response.raise_for_status()
    joke_data = response.json()
    joke_setup = joke_data['setup']
    joke_punchline = joke_data['punchline']
    bot.send_message(chat_id=message.chat.id, text=f"{joke_setup}\n{joke_punchline}")





# Set up the bot and API endpoint
api_endpoint = "https://archive.org/advancedsearch.php"

# Define the command to trigger the search
@bot.message_handler(commands=['video'])
def search_video(message):
    # Set up the search parameters
    search_terms = message.text.split(' ')[1]
    params = {
        "q": search_terms,
        "output": "json",
        "mediatype": "movies",
        "rows": 5  # Limit the results to 5 videos
    }

    try:
        # Send the API request and retrieve the results
        response = requests.get(api_endpoint, params=params)
        data = response.json()

        # Parse the results and retrieve the video details
        videos = []
        for result in data["response"]["docs"]:
            video = {
                "title": result["title"],
                "description": result["description"],
                "url": f'https://archive.org/details/{result["identifier"]}',
                "image_url": f'https://archive.org/services/img/{result["identifier"]}',
            }
            videos.append(video)

        # Send the retrieved videos to the user
        for video in videos:
            # Download the video file
            video_file = requests.get(video["url"]).content

            # Send the video file to the user
            bot.send_video(chat_id=message.chat.id, data=video_file, caption=f'{video["title"]}\n{video["description"]}')

    except requests.exceptions.RequestException as e:
        # Handle the case when the request fails
        bot.reply_to(message, "Sorry, an error occurred while processing your request. Please try again later.")

    except Exception as e:
        # Handle any other exceptions that may occur
        bot.reply_to(message, "Sorry, something went wrong. Please try again later.")
        data = response.json()

# Define the '/help' command handler
@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id
    tutorial_url = "https://t.me/googlersi/18"
    bot.send_message(chat_id, f"Tutorial To Use This Bot: {tutorial_url}")

# Start the bot
bot.polling()