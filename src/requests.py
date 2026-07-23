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



response = requests.get(
    "https://api.example.com/v1/data",
    timeout=10
)
response.raise_for_status()
data = response.json()

def fetch_all_pages(base_url: str) -> list[dict]:
    results, page = [], 1

    while True:
        resp = requests.get(
            base_url,
            params={"page": page},
            timeout=10
        )

        resp.raise_for_status()
        batch = resp.json().get("results", [])

        if not batch:
            break

        results.extend(batch)
        page += 1

    return results

headers = {
    "Authorization": f"Bearer {api_token}"
}

response = requests.post(
    "https://api.example.com/v1/records",
    json=payload,
    headers=headers,
    timeout=10
)

response.raise_for_status()