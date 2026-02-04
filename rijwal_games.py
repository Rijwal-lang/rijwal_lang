#!/usr/bin/env python3
"""
Rijwal_Lang Game Plugin System & Library
Built-in Games: Tic-Tac-Toe, Snake, Hangman, Number Guess, Memory Match
Purpose: Break/Refresh your mind while coding!

Version: 1.0
"""

import random
import os

class GamePlugin:
    """Base class for all games"""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.score = 0
        self.running = True
    
    def play(self):
        raise NotImplementedError
    
    def reset(self):
        self.score = 0


class TicTacToe(GamePlugin):
    """Classic Tic-Tac-Toe game"""
    
    def __init__(self):
        super().__init__("Tic-Tac-Toe", "Beat the AI in Tic-Tac-Toe!")
        self.board = [' ' for _ in range(9)]
        self.human = 'X'
        self.ai = 'O'
    
    def print_board(self):
        print("\n")
        for i in range(3):
            print(f" {self.board[i*3]} | {self.board[i*3+1]} | {self.board[i*3+2]} ")
            if i < 2:
                print("-----------")
    
    def check_winner(self, player):
        win_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in win_combos:
            if all(self.board[i] == player for i in combo):
                return True
        return False
    
    def ai_move(self):
        available = [i for i in range(9) if self.board[i] == ' ']
        if available:
            move = random.choice(available)
            self.board[move] = self.ai
    
    def play(self):
        print("=== TIC-TAC-Toe ===")
        self.print_board()
        
        while self.running:
            try:
                move = int(input("Your move (0-8): "))
                if self.board[move] != ' ':
                    print("Position taken!")
                    continue
                
                self.board[move] = self.human
                self.print_board()
                
                if self.check_winner(self.human):
                    print("You win!")
                    self.score += 1
                    break
                
                self.ai_move()
                self.print_board()
                
                if self.check_winner(self.ai):
                    print("AI wins!")
                    break
                
                if ' ' not in self.board:
                    print("Draw!")
                    break
                    
            except (ValueError, IndexError):
                print("Invalid input!")


class NumberGuessingGame(GamePlugin):
    """Guess the secret number"""
    
    def __init__(self):
        super().__init__("Number Guess", "Guess the secret number!")
        self.secret = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 7
    
    def play(self):
        print("=== NUMBER GUESSING GAME ===")
        print(f"I'm thinking of a number between 1 and 100!")
        print(f"You have {self.max_attempts} attempts.\n")
        
        while self.attempts < self.max_attempts:
            try:
                guess = int(input(f"Attempt {self.attempts + 1}/{self.max_attempts} - Guess: "))
                self.attempts += 1
                
                if guess == self.secret:
                    print(f"🎉 Correct! You guessed it in {self.attempts} attempts!")
                    self.score = self.max_attempts - self.attempts + 1
                    break
                elif guess < self.secret:
                    print(f"Too low! Try higher.")
                else:
                    print(f"Too high! Try lower.")
                    
            except ValueError:
                print("Please enter a valid number!")
        else:
            print(f"Game Over! The number was {self.secret}")


class HangmanGame(GamePlugin):
    """Hangman word guessing game"""
    
    def __init__(self):
        super().__init__("Hangman", "Guess the word!")
        self.words = ["python", "programming", "rijwal", "language", "computer", "algorithm", "developer"]
        self.word = random.choice(self.words).upper()
        self.guessed = set()
        self.wrong = set()
        self.max_wrong = 6
    
    def print_hangman(self):
        stages = [
            "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
            "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n========="
        ]
        return stages[len(self.wrong)]
    
    def get_word_display(self):
        return ' '.join(c if c in self.guessed else '_' for c in self.word)
    
    def play(self):
        print("=== HANGMAN ===\n")
        
        while len(self.wrong) < self.max_wrong:
            print(self.print_hangman())
            print(f"\nWord: {self.get_word_display()}")
            print(f"Wrong guesses: {len(self.wrong)}/{self.max_wrong}")
            print(f"Guessed: {' '.join(sorted(self.guessed))}\n")
            
            guess = input("Guess a letter: ").upper()
            
            if guess in self.guessed or guess in self.wrong:
                print("Already guessed!")
                continue
            
            if guess in self.word:
                self.guessed.add(guess)
                if all(c in self.guessed for c in self.word):
                    print(f"🎉 You won! The word was: {self.word}")
                    self.score = self.max_wrong - len(self.wrong)
                    break
            else:
                self.wrong.add(guess)
        else:
            print(f"Game Over! The word was: {self.word}")


class MemoryMatchGame(GamePlugin):
    """Memory matching game"""
    
    def __init__(self):
        super().__init__("Memory Match", "Match the pairs!")
        self.pairs = ['🌟', '🌟', '🎮', '🎮', '🚀', '🚀', '💎', '💎', 
                      '🎨', '🎨', '🔥', '🔥', '⚡', '⚡', '🌈', '🌈']
        random.shuffle(self.pairs)
        self.revealed = [False] * 16
        self.matches = 0
    
    def print_board(self):
        print("\n")
        for i in range(16):
            if self.revealed[i]:
                print(self.pairs[i], end=' ')
            else:
                print('?', end=' ')
            if (i + 1) % 4 == 0:
                print()
    
    def play(self):
        print("=== MEMORY MATCH ===")
        print("Match pairs of emojis! Positions: 0-15 (4x4 grid)\n")
        
        attempts = 0
        while self.matches < 8:
            self.print_board()
            
            try:
                first = int(input("First card (0-15): "))
                second = int(input("Second card (0-15): "))
                
                if first < 0 or first > 15 or second < 0 or second > 15 or first == second:
                    print("Invalid positions!")
                    continue
                
                attempts += 1
                
                if self.pairs[first] == self.pairs[second]:
                    self.revealed[first] = True
                    self.revealed[second] = True
                    self.matches += 1
                    print("✓ Match found!")
                else:
                    print("✗ No match. Try again!")
                    
            except (ValueError, IndexError):
                print("Invalid input!")
        
        self.print_board()
        print(f"🎉 You won in {attempts} attempts!")
        self.score = 50 - attempts


class QuickMathGame(GamePlugin):
    """Quick math challenge"""
    
    def __init__(self):
        super().__init__("Quick Math", "Solve equations fast!")
        self.time_limit = 30
        self.correct = 0
    
    def generate_problem(self):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(['+', '-', '*'])
        
        if op == '+':
            answer = a + b
        elif op == '-':
            answer = a - b
        else:
            answer = a * b
        
        return f"{a} {op} {b}", answer
    
    def play(self):
        print("=== QUICK MATH ===")
        print(f"Solve as many as you can in 30 seconds!\n")
        
        import time
        start_time = time.time()
        
        while time.time() - start_time < self.time_limit:
            problem, answer = self.generate_problem()
            
            try:
                user_answer = int(input(f"{problem} = "))
                if user_answer == answer:
                    print("✓ Correct!")
                    self.correct += 1
                else:
                    print(f"✗ Wrong! Answer was {answer}")
            except ValueError:
                print("Invalid input!")
        
        print(f"\n🎉 You solved {self.correct} problems!")
        self.score = self.correct


class GameManager:
    """Manages all games"""
    
    def __init__(self):
        self.games = {
            "tictactoe": TicTacToe(),
            "guess": NumberGuessingGame(),
            "hangman": HangmanGame(),
            "memory": MemoryMatchGame(),
            "quickmath": QuickMathGame(),
        }
    
    def list_games(self):
        print("\n=== AVAILABLE GAMES ===")
        for key, game in self.games.items():
            print(f"• {game.name}: {game.description}")
        print()
    
    def play_game(self, game_name):
        if game_name.lower() in self.games:
            game = self.games[game_name.lower()]
            try:
                game.play()
                print(f"\nYour Score: {game.score}")
                return True
            except KeyboardInterrupt:
                print("\nGame cancelled!")
                return False
        else:
            print(f"Game '{game_name}' not found!")
            return False


# Standalone game launcher
if __name__ == "__main__":
    manager = GameManager()
    
    while True:
        manager.list_games()
        choice = input("Enter game name (or 'quit' to exit): ").strip().lower()
        
        if choice == 'quit':
            print("Thanks for playing!")
            break
        
        manager.play_game(choice)
