def count_words(text: str):
    cleaned_text = ''.join(filter(lambda char: char.isalnum() or char.isspace(), text))
    return len(cleaned_text.split())