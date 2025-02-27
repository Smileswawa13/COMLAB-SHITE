# Module sa pagsulat ng mga score sa isang file at pagbabasa nila muli.
import sys
import random
from string import printable
from collections import defaultdict

# Initialize the tutorial_words dictionary
words = defaultdict(set)

# Mao ni sila mag generate us listahan nga random para gamiton sa dula
def generate_words_tutorial():
    """
    Generate lists of words from the tutorial_words and bonus_words dictionaries.

    Returns:
    two lists of words for tutorial and bonus.
    """
    try:
        from words import tutorial_words, bonus_words

        tutorial_list = [word for word_list in tutorial_words.values() for word in word_list]
        bonus_list = [word for word_list in bonus_words.values() for word in word_list]

        random.shuffle(tutorial_list)
        random.shuffle(bonus_list)

        return tutorial_list, bonus_list
    except ImportError:
        return [], []

def generate_words_stage1():
    """
    Generate lists of words from the stage1_words, and bonus_words dictionaries.

    Returns:
    two lists of words for stage1, bonus.
    """
    try:
        from words import stage1_words, bonus_words

        stage1_list = [word for word_list in stage1_words.values() for word in word_list]
        bonus_list = [word for word_list in bonus_words.values() for word in word_list]

        random.shuffle(stage1_list)
        random.shuffle(bonus_list)

        return stage1_list, bonus_list
    except ImportError:
        return [], []


def generate_words_stage2():
    """
    Generate lists of words from the stage2_words and bonus_words dictionaries.

    Returns:
    Two lists of words for stage2 and bonus.
    """
    try:
        from words import stage2_words, bonus_words

        stage2_list = [word for word_list in stage2_words.values() for word in word_list]
        bonus_list = [word for word_list in bonus_words.values() for word in word_list]

        random.shuffle(stage2_list)
        random.shuffle(bonus_list)

        return stage2_list, bonus_list
    except ImportError:
        return [], []

def generate_words_stage3():
    """
    Generate lists of words from the stage3_words and bonus_words dictionaries.

    Returns:
    Two lists of words for stage3 and bonus.
    """
    try:
        from words import stage3_words, bonus_words

        stage3_list = [word for word_list in stage3_words.values() for word in word_list]
        bonus_list = [word for word_list in bonus_words.values() for word in word_list]

        random.shuffle(stage3_list)
        random.shuffle(bonus_list)

        return stage3_list, bonus_list
    except ImportError:
        return [], []

# Holder of Reality
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