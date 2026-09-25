def get_evens(nums: list[int]) -> list[int]:
    even_num = []
    for num in nums:
        if num % 2 == 0:
            even_num.append(num)
    return even_num

def count_frequency(text: str) -> dict[str, int]:
    frequency = {}
    for item in text:
        frequency[item] = frequency.get(item, 0) + 1 
    return frequency

def sum_key_values(dict_list: list[dict], target_key: str) -> int:
    total = 0
    for item in dict_list:
        if target_key in item:
            total += item[target_key]
    return total

def remove_duplicates(items: list[str]) -> list[str]:
    cleaned = []
    for item in items:
        if item not in cleaned:
            cleaned.append(item)
    return cleaned

def reverse_words(sentence: str) -> str:
    words = sentence.split()
    return " ".join(reversed(words))

def top_category_spend(transactions: list[dict], category: str) -> float:
    total = 0.0
    for item in transactions:
        if item.get('category') == category and item.get('status') == 'completed':
            total += item.get('amount', 0.0)
    return total

def count_word_frequency(words: list[str]) -> dict[str, int]:
    frequency = {}
    for item in words:
        frequency[item] = frequency.get(item, 0) + 1 
    return frequency

def reverse_string(text: str) -> str:
    return text[::-1]
