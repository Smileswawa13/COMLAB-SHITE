# Module for writing scores to a file and reading them back.
import os
scorefile = os.path.join(os.path.dirname(__file__), "resources/highscore.txt")
playerfile = os.path.join(os.path.dirname(__file__), "resources/players.txt")

# Magload sa skore
def load_score():
    """ Returns the highest score, or 0 if no one has scored yet """
    try:
        with open(scorefile) as file:
            scores = sorted([int(score.strip())
                             for score in file.readlines()
                             if score.strip().isdigit()], reverse=True)
    except IOError:
        scores = []

    return scores[0] if scores else 0

def load_score_with_player():
    """ Returns a tuple of the highest score and the corresponding player, or (0, None) if no one has scored yet """
    try:
        with open(scorefile) as file:
            scores = {line.split(":")[0]: int(line.split(":")[1]) for line in file.readlines()}
        if scores:
            highest_score_player = max(scores, key=scores.get)
            return scores[highest_score_player], highest_score_player
        else:
            return 0, None
    except IOError:
        return 0, None

# I-save ang skore
def get_current_player():
    try:
        with open(playerfile, "r") as file:
            return file.readline().strip()
    except Exception as e:
        print(f"Error reading current player: {e}")
        return None

def write_score(score):
    try:
        username = get_current_player()
        if not username:
            raise ValueError("No current player found")

        # Read existing scores
        if os.path.exists(scorefile):
            with open(scorefile, "r") as file:
                scores = {line.split(":")[0]: int(line.split(":")[1]) for line in file.readlines()}
        else:
            scores = {}

        # Update the score for the given username
        scores[username] = max(score, scores.get(username, 0))

        # Write updated scores back to the file
        with open(scorefile, "w") as file:
            for user, score in scores.items():
                file.write(f"{user}:{score}\n")
    except Exception as e:
        print(f"Error writing score: {e}")