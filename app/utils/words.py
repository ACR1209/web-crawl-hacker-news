from app.models.story import Story

def count_words(text: str)->int:
    """
        Count the number of words in a given text.

        The function is implemented according to 
        'When counting words, consider only the spaced words and exclude any symbols. 
        For instance, the phrase “This is - a self-explained example” 
        should be counted as having 5 words.'
        
        Parameters:
        - text (str): The input string from which words are to be counted.

        Returns:
        - int: The number of words in the cleaned text.
    """
    cleaned_text = ''.join(filter(lambda char: char.isalnum() or char.isspace(), text))
    return len(cleaned_text.split())

def within_word_range(story: Story, count_words_min: int, count_words_max: int)->bool:
    """
        Determine if the word count of a story's title falls within a specified range.

                Parameters:
        - story (Story): The story object containing the title to be evaluated.
        - count_words_min (int): The minimum word count (inclusive). If this value is less than 0, it is treated as 0.
        - count_words_max (int | None): The maximum word count (inclusive). If this value is None, there is no upper limit.

        Returns:
        - bool: True if the word count of the story's title is within the specified range, False otherwise.
    """
    word_count = count_words(story.title)
    return count_words_min <= word_count and (count_words_max is None or word_count <= count_words_max)