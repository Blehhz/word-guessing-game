import random
import time
import os


def get_data(user_name):
    file_path = f"user_data/{user_name.lower()}_word_score.txt"
    if os.path.isfile(file_path):
        with open(file_path, "r") as user_file:
            file_data = user_file.read()
            return int(file_data) if file_data.strip() else 0
    return 0


def update_score(high_score, user_name):
    if not os.path.exists("user_data"):
        os.makedirs("user_data")
    file_path = f"user_data/{user_name.lower()}_word_score.txt"
    with open(file_path, "w") as user_file:
        user_file.write(str(high_score))


def load_words(filename="words.txt"):
    categories = {}
    with open(filename, "r") as f:
        for line in f:
            if ":" in line:
                category, words = line.strip().split(":")
                categories[category.strip()] = [w.strip().lower() for w in words.split(",")]
    return categories


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def welcome_message(user_name, high_score):
    clear_screen()
    print(f"Hello {user_name},")
    print("Welcome to the WORD GUESSING GAME 🎮")
    print(f"Your high score: {high_score:03d}")
    time.sleep(4)


def choose_difficulty():
    clear_screen()
    levels = {"easy": 10, "medium": 7, "hard": 5}
    while True:
        choice = input("Choose difficulty (easy/medium/hard): ").lower()
        if choice in levels:
            return levels[choice]
        print("Invalid choice. Try again.")


def give_hint(word, guessed):
    hidden_indices = [i for i, l in enumerate(guessed) if l == "_"]
    if hidden_indices:
        idx = random.choice(hidden_indices)
        guessed[idx] = word[idx]
    return guessed


def decision(word, category, attempts):
    guessed = ["_"] * len(word)
    used_letters = set()
    hint_used = False

    while attempts > 0 and "_" in guessed:
        clear_screen()
        print(f"Category: {category}")
        print(f"Attempts left: {attempts}")
        print("Word:", " ".join(guessed))
        print("Used letters:", ", ".join(sorted(used_letters)) if used_letters else "None")

        guess = input("\nGuess a letter, the whole word, or type 'hint': ").lower().strip()

        if guess == "hint":
            if not hint_used:
                guessed = give_hint(word, guessed)
                hint_used = True
                print("🔎 Hint used!")
            else:
                print("❌ You already used your hint!")
            time.sleep(1.5)
            continue

        if len(guess) > 1:
            if guess == word:
                print("🎉 You guessed the whole word correctly!")
                time.sleep(1.5)
                return "win", word
            else:
                attempts -= 1
                print(f"❌ Wrong word guess! Attempts left: {attempts}")
                time.sleep(1.5)
                continue

        if not guess.isalpha():
            print("Please enter a valid letter or word.")
            time.sleep(1.5)
            continue

        if guess in used_letters:
            print("⚠️ You already guessed that letter!")
            time.sleep(1.5)
            continue

        used_letters.add(guess)

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    guessed[i] = guess
            print("✅ Correct guess!")
        else:
            attempts -= 1
            print(f"❌ Wrong guess! Attempts left: {attempts}")
        time.sleep(0.5)

    return ("win", word) if "_" not in guessed else ("lose", word)


def result_output(result, high_score, score, word):
    clear_screen()

    title = "🎉 You guessed it!" if result == "win" else "😢 Out of attempts!"
    lines = [
        title,
        f"The word was: {word}",
        f"Current Score: {score:03d}",
        f"High Score: {high_score:03d}"
    ]

    max_length = max(len(line) for line in lines)
    box_width = max_length + 6

    border = "*" * box_width

    def center_line(text):
        return "* " + text.center(box_width - 4) + " *"

    print(border)
    for line in lines:
        print(center_line(line))
    print(border)


def play_again(user_name):
    while True:
        choice = input("\nDo you want to play again? (y/n): ").lower()
        if choice in ("y", "n"):
            if choice == "y":
                return True
            else:
                clear_screen()
                print(f"Thank you for playing {user_name}!")
                return False
        print("Invalid input. Choose 'y' for Yes or 'n' for No.")


def main():
    user_name = input("Enter your name: ")
    high_score = get_data(user_name)
    score = 0

    welcome_message(user_name, high_score)
    categories = load_words("words.txt")

    while True:
        category = random.choice(list(categories.keys()))
        word = random.choice(categories[category])
        attempts = choose_difficulty()

        result, final_word = decision(word, category, attempts)

        if result == "win":
            score += 1
        else:
            score = 0

        if score > high_score:
            high_score = score
            update_score(high_score, user_name)

        result_output(result, high_score, score, final_word)

        if not play_again(user_name):
            break


if __name__ == "__main__":
    main()
