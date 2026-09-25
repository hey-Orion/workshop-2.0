def get_events(numbers: list[int]) -> list[int]:
    event_num = []
    for num in numbers:
        if num % 2 == 0:
            event_num.append(num)
    return event_num


def word_fre(words: list[str]) -> dict[str, int]:
    counts = {}
    for item in words:
        counts[item] = counts.get(item, 0) + 1 
    return counts


def sum_key_values(records: list[dict], key: str) -> float:
    total = 0
    for r in records:
        if key in records:
            total += r[key]
    return total 


def remove_duplicates(items: list) -> list:
    seen = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen

def reverse_str(s: str) -> str:
    return s[::-1]
