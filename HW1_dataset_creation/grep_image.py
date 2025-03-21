import os
import time
import requests
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options  

pokemon_names = [
    "Bulbasaur", "Charmander",
    "Squirtle",  "Caterpie",  
    "Weedle", "Pidgey", "Rattata", 
    "Spearow",  "Ekans", "Pikachu",
    "Sandshrew", "Nidoran", "Clefairy", "Vulpix", "Jigglypuff",  "Zubat", "Oddish",  
    "Paras",  "Venonat",  "Diglett",  "Meowth", 
     "Psyduck", "Mankey",  "Growlithe",  
    "Poliwag",  "Abra",  "Machop",  "Bellsprout", "Tentacool", 
    "Geodude", "Ponyta",  "Slowpoke", 
     "Magnemite", "Farfetch'd", "Doduo", "Seel", 
     "Grimer",  "Shellder",  "Gastly", 
    "Onix", "Drowzee",  "Krabby",  "Voltorb",  "Exeggcute",  "Cubone",  "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", 
     "Rhyhorn", "Chansey", "Tangela", "Kangaskhan", "Horsea", 
     "Goldeen", "Staryu", "Mr. Mime", "Scyther", "Jynx", 
    "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp","Lapras", 
    "Ditto", "Eevee", "Vaporeon", 
    "Jolteon", "Flareon", "Porygon", "Omanyte", 
    "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", 
    "Dratini",  "Mewtwo", "Mew"
]

chrome_options = Options()
chrome_options.add_argument("--disable-gpu") 
chrome_options.add_argument("--no-sandbox") 
chrome_options.add_argument("--headless")

download_folder = "dataset/pokemon"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

driver = webdriver.Chrome(options=chrome_options)

for pokemon in pokemon_names:
    print(f"Searching for {pokemon}")
    pokemon += " pokemon"
    pokemon_folder = os.path.join(download_folder, pokemon)
    if not os.path.exists(pokemon_folder):
        os.makedirs(pokemon_folder)

    driver.get("https://www.google.com/imghp")

    search_box = driver.find_element(By.NAME, "q")
    search_box.clear()
    search_box.send_keys(pokemon)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

    scroll_count = 0
    max_scrolls = 6
    image_elements = driver.find_elements(By.CSS_SELECTOR, "img[class='YQ4gaf']")

    while scroll_count < max_scrolls:
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[class='YQ4gaf']")))

        image_elements = driver.find_elements(By.CSS_SELECTOR, "img[class='YQ4gaf']")
        scroll_count += 1

    print(f"Found {len(image_elements)} images for {pokemon}")

    downloaded_images = set()
    count = 1  # Reset counter for each pokemon
    for img in image_elements[:120]:
        try:
            img_url = img.get_attribute("src")
            if not img_url:
                continue
            if img_url in downloaded_images:
                continue
            downloaded_images.add(img_url)
            if img_url.startswith("data:image"):
                img_data = base64.b64decode(img_url.split(",")[1])
            else:
                response = requests.get(img_url, timeout=5)
                if response.status_code == 200:
                    img_data = response.content
                else:
                    continue
            img_path = os.path.join(pokemon_folder, f"{pokemon}_{count}.jpg")
            with open(img_path, "wb") as f:
                f.write(img_data)

            print(f"Saved: {img_path}")
            count += 1

        except Exception as e:
            print(f"Failed to download image {count}: {e}")

driver.quit()
print("Image download completed!")
