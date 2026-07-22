import requests

base_url = "https://pokeapi.co/api/v2"

def get_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None

pokemon_name = "pikachu"
pokemon_info = get_info(pokemon_name)

if pokemon_info:
    print(".......................")
    print(f"name: {pokemon_info['name']}")
    print(f"id: {pokemon_info['id']}")
    print(f"height: {pokemon_info['height']}")
    print(f"weight: {pokemon_info['weight']}")
else:
    print("Pokémon not found.")