import random
import time
import os

def load_words(filename):
    """Load words and categories from file."""
    categories = {}
    with open(filename, "r") as f:
        for line in f:
            if ":" in line:
                category, words = line.strip().split(":")
                categories[category.strip()] = [w.strip().lower() for w in words.split(",")]
    return categories

def choose_difficulty():
    os.system('cls')
    levels = {"easy": 10, "medium": 7, "hard": 5}
    while True:
        choice = input("Choose difficulty (easy/medium/hard): ").lower()
        if choice in levels:
            return levels[choice]
        print("Invalid choice. Try again.")

def give_hint(word, guessed):
    """Reveal one hidden letter as a hint."""
    hidden_indices = [i for i, l in enumerate(guessed) if l == "_"]
    if hidden_indices:
        idx = random.choice(hidden_indices)
        guessed[idx] = word[idx]
    return guessed

def word_guessing_game():
    categories = load_words("words.txt")
    category = random.choice(list(categories.keys()))
    word = random.choice(categories[category])
    guessed = ["_"] * len(word)
    
    attempts = choose_difficulty()
    used_letters = set()
    hint_used = False
    score = 0

    os.system('cls')
    print("\n🎮 Welcome to the Advanced Word Guessing Game!")
    time.sleep(4)

    while attempts > 0 and "_" in guessed:
        os.system('cls')
        print(f"Category: {category}")
        print(f"You have {attempts} attempts.\n")
        print("Word:", " ".join(guessed))
        print("Used letters:", ", ".join(sorted(used_letters)) if used_letters else "None")
        guess = input("Guess a letter (or type 'hint'): ").lower()

        if guess == "hint":
            if not hint_used:
                guessed = give_hint(word, guessed)
                hint_used = True
                print("🔎 Hint used!\n")
            else:
                print("❌ You already used your hint!\n")
            continue

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.\n")
            continue

        if guess in used_letters:
            print("⚠️ You already guessed that letter!\n")
            continue

        used_letters.add(guess)

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed[i] = guess
            print("✅ Correct guess!\n")
        else:
            attempts -= 1
            print(f"❌ Wrong guess! Attempts left: {attempts}\n")

    if "_" not in guessed:
        print("🎉 Congratulations! You guessed the word:", word)
        score += 1
    else:
        print("😢 Out of attempts! The word was:", word)

    print(f"Your score: {score}")


if __name__ == "__main__":
    word_guessing_game()
