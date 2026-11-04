def filter_and_double(numbers):
    result = []
    for num in numbers:
        if num > 10:
            result.append(num *= 2)
    return result

result_df = salary_df[salary_df["salary"] > 50000 ]["salary"].mean()

def get_evens(numbers):
    return [num for num in numbers if num % 2 == 0]

