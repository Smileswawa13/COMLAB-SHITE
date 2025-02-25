import sys
import random
from string import printable
from collections import defaultdict

# Initialize the tutorial_words dictionary
words = defaultdict(set)

def generate_words_tutorial():
    """
    Generate a list of tutorial_words from the tutorial_words dictionary.

    Returns:
    list: A list of randomly selected tutorial_words.
    """
    try:
        from words import tutorial_words as word_dict
        all_words = [word for word_list in word_dict.values() for word in word_list]
        return random.sample(all_words, min(len(all_words), 100))  # Adjust the number of tutorial_words as needed
    except ImportError:
        return []


import random

def generate_words_stage1():
    """
    Generate lists of words from the stage1_words, bonus_words, and bossfight_bonus dictionaries.

    Returns:
    tuple: Three lists of words for stage1, bonus, and bossfight.
    """
    try:
        from words import stage1_words, bonus_words, bossfight_bonus

        stage1_list = [word for word_list in stage1_words.values() for word in word_list]
        bonus_list = [word for word_list in bonus_words.values() for word in word_list]
        bossfight_list = [word for word_list in bossfight_bonus.values() for word in word_list]

        random.shuffle(stage1_list)
        random.shuffle(bonus_list)
        random.shuffle(bossfight_list)

        return stage1_list, bonus_list, bossfight_list
    except ImportError:
        return [], [], []

def generate_words_stage2():
    """
    Generate lists of words from the stage1_words, bonus_words, and bossfight_bonus dictionaries.

    Returns:
    tuple: Three lists of words for stage1, bonus, and bossfight.
    """
    try:
        from words import stage2_words, bonus_words, bossfight_bonus

        stage1_list = [word for word_list in stage2_words.values() for word in word_list]
        bonus_list = [word for word_list in bonus_words.values() for word in word_list]
        bossfight_list = [word for word_list in bossfight_bonus.values() for word in word_list]

        random.shuffle(stage1_list)
        random.shuffle(bonus_list)
        random.shuffle(bossfight_list)

        return stage1_list, bonus_list, bossfight_list
    except ImportError:
        return [], [], []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python genwords.py <dictfile>")
        sys.exit(1)

    dictfile = sys.argv[1]

    # Read and process dictionary file
    with open(dictfile) as file:
        wordlist = [w.strip().lower() for w in file.read().split()]

    random.shuffle(wordlist)
    wordlist = list(filter(lambda w: all(c in printable for c in w), wordlist))
    wordlist = wordlist[:1300]

    # Group tutorial_words by length
    for word in wordlist:
        words[len(word)].add(word)

    # Write processed tutorial_words to tutorial_words.py
    with open("words.py", "w") as file:
        file.write("tutorial_words = {\n")
        for length, word_set in words.items():
            file.write(f"    {length}: {sorted(word_set)},\n")
        file.write("}\n")