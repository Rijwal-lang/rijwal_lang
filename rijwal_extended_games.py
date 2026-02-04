#!/usr/bin/env python3
"""
RIJWAL_LANG EXTENDED GAMES - v0.17+
====================================

5 Additional Games:
1. Snake - Classic snake game
2. Pong - Two-player tennis
3. Puzzle - Memory/matching puzzle
4. Code Challenge - Programming challenges
5. Math Race - Quick math competition

Total: 10 games in IDE sidebar
"""

import random
import time
from datetime import datetime

# ============================================================================
# BASE GAME CLASS
# ============================================================================

class ExtendedGamePlugin:
    """Base class for extended games."""
    
    def __init__(self, name, version="1.0"):
        self.name = name
        self.version = version
        self.score = 0
        self.game_state = "ready"
        self.start_time = None
        self.end_time = None
        
    def play(self):
        """Play the game. Override in subclasses."""
        raise NotImplementedError
        
    def get_score(self):
        """Get current score."""
        return self.score
        
    def reset(self):
        """Reset game state."""
        self.score = 0
        self.game_state = "ready"
        self.start_time = None
        self.end_time = None
        
    def start_timer(self):
        """Start game timer."""
        self.start_time = time.time()
        
    def end_timer(self):
        """End game timer and return elapsed time."""
        self.end_time = time.time()
        return self.end_time - self.start_time if self.start_time else 0


# ============================================================================
# SNAKE GAME
# ============================================================================

class SnakeGame(ExtendedGamePlugin):
    """Classic Snake game."""
    
    def __init__(self):
        super().__init__("Snake", "1.0")
        self.width = 20
        self.height = 20
        self.snake = [(10, 10), (10, 11), (10, 12)]
        self.food = self._spawn_food()
        self.direction = "up"
        self.next_direction = "up"
        self.game_over = False
        self.score = 0
        
    def _spawn_food(self):
        """Spawn food at random location."""
        while True:
            food = (random.randint(0, self.width - 1), 
                   random.randint(0, self.height - 1))
            if food not in self.snake:
                return food
                
    def set_direction(self, direction):
        """Set snake direction (up, down, left, right)."""
        # Prevent reversing into self
        opposite = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        if direction != opposite.get(self.direction):
            self.next_direction = direction
            
    def update(self):
        """Update game state."""
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        if self.direction == "up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "left":
            new_head = (head_x - 1, head_y)
        elif self.direction == "right":
            new_head = (head_x + 1, head_y)
            
        # Check collisions
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake):
            self.game_over = True
            self.game_state = "game_over"
            return
            
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self._spawn_food()
        else:
            self.snake.pop()
            
    def get_state(self):
        """Get current game state for rendering."""
        return {
            "snake": self.snake,
            "food": self.food,
            "score": self.score,
            "game_over": self.game_over,
            "width": self.width,
            "height": self.height
        }
        
    def play(self):
        """Play snake game."""
        self.game_state = "playing"
        self.start_timer()
        return f"Snake Game Started! Score: {self.score}"


# ============================================================================
# PONG GAME
# ============================================================================

class PongGame(ExtendedGamePlugin):
    """Two-player Pong tennis game."""
    
    def __init__(self):
        super().__init__("Pong", "1.0")
        self.width = 80
        self.height = 20
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = 1
        self.ball_dy = 1
        self.paddle1_y = self.height // 2
        self.paddle2_y = self.height // 2
        self.paddle_height = 4
        self.score1 = 0
        self.score2 = 0
        
    def move_paddle(self, player, direction):
        """Move paddle (player 1 or 2, direction: up or down)."""
        if player == 1:
            if direction == "up":
                self.paddle1_y = max(0, self.paddle1_y - 2)
            elif direction == "down":
                self.paddle1_y = min(self.height - self.paddle_height, 
                                    self.paddle1_y + 2)
        elif player == 2:
            if direction == "up":
                self.paddle2_y = max(0, self.paddle2_y - 2)
            elif direction == "down":
                self.paddle2_y = min(self.height - self.paddle_height, 
                                    self.paddle2_y + 2)
                
    def update(self):
        """Update ball position."""
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Bounce off top/bottom
        if self.ball_y <= 0 or self.ball_y >= self.height - 1:
            self.ball_dy = -self.ball_dy
            
        # Bounce off paddle 1
        if (self.ball_x <= 1 and 
            self.paddle1_y <= self.ball_y <= self.paddle1_y + self.paddle_height):
            self.ball_dx = -self.ball_dx
            self.score1 += 1
            
        # Bounce off paddle 2
        if (self.ball_x >= self.width - 2 and 
            self.paddle2_y <= self.ball_y <= self.paddle2_y + self.paddle_height):
            self.ball_dx = -self.ball_dx
            self.score2 += 1
            
        # Out of bounds
        if self.ball_x < 0 or self.ball_x > self.width:
            self._reset_ball()
            
    def _reset_ball(self):
        """Reset ball to center."""
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-1, 1])
        
    def play(self):
        """Play pong game."""
        self.game_state = "playing"
        self.start_timer()
        return f"Pong Game Started! Player 1 vs Player 2"


# ============================================================================
# PUZZLE GAME
# ============================================================================

class PuzzleGame(ExtendedGamePlugin):
    """Memory/matching puzzle game."""
    
    def __init__(self):
        super().__init__("Puzzle", "1.0")
        self.grid_size = 4  # 4x4 grid
        self.cards = self._create_cards()
        self.revealed = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.matched = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.first_card = None
        self.second_card = None
        self.score = 0
        self.moves = 0
        
    def _create_cards(self):
        """Create shuffled card grid."""
        symbols = ['🌟', '🎨', '🎮', '🎯', '🎪', '🎭', '🎲', '🎸']
        cards = symbols + symbols  # Pairs
        random.shuffle(cards)
        grid = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                row.append(cards[i * self.grid_size + j])
            grid.append(row)
        return grid
        
    def reveal_card(self, row, col):
        """Reveal a card at position."""
        if self.revealed[row][col] or self.matched[row][col]:
            return False
            
        self.revealed[row][col] = True
        
        if self.first_card is None:
            self.first_card = (row, col)
            return True
        else:
            self.second_card = (row, col)
            self.moves += 1
            
            # Check match
            r1, c1 = self.first_card
            r2, c2 = self.second_card
            
            if self.cards[r1][c1] == self.cards[r2][c2]:
                # Match!
                self.matched[r1][c1] = True
                self.matched[r2][c2] = True
                self.score += 10
                self.first_card = None
                self.second_card = None
                return True
            else:
                # No match - hide cards
                self.revealed[r1][c1] = False
                self.revealed[r2][c2] = False
                self.first_card = None
                self.second_card = None
                return False
                
    def is_complete(self):
        """Check if puzzle is complete."""
        for row in self.matched:
            for matched in row:
                if not matched:
                    return False
        return True
        
    def play(self):
        """Play puzzle game."""
        self.game_state = "playing"
        self.start_timer()
        return f"Puzzle Game Started! Find matching pairs!"


# ============================================================================
# CODE CHALLENGE GAME
# ============================================================================

class CodeChallengeGame(ExtendedGamePlugin):
    """Programming challenge mini-game."""
    
    def __init__(self):
        super().__init__("Code Challenge", "1.0")
        self.challenges = [
            {
                "title": "Reverse String",
                "description": "Reverse the string 'hello'",
                "hint": "Use reverse() function",
                "answer": "olleh",
                "points": 10
            },
            {
                "title": "Sum List",
                "description": "Sum of [1, 2, 3, 4, 5]",
                "hint": "Use sum() or loop",
                "answer": "15",
                "points": 10
            },
            {
                "title": "Factorial 5",
                "description": "Calculate 5!",
                "hint": "5 * 4 * 3 * 2 * 1",
                "answer": "120",
                "points": 15
            },
            {
                "title": "Fibonacci",
                "description": "7th Fibonacci number",
                "hint": "0, 1, 1, 2, 3, 5, 8...",
                "answer": "13",
                "points": 20
            },
            {
                "title": "Prime Check",
                "description": "Is 17 prime?",
                "hint": "Only divisible by 1 and itself",
                "answer": "yes",
                "points": 15
            }
        ]
        self.current_challenge = None
        self.completed = 0
        self.score = 0
        
    def get_next_challenge(self):
        """Get next challenge."""
        if self.completed < len(self.challenges):
            self.current_challenge = self.challenges[self.completed]
            return self.current_challenge
        return None
        
    def check_answer(self, answer):
        """Check if answer is correct."""
        if not self.current_challenge:
            return False
            
        if str(answer).lower().strip() == self.current_challenge["answer"].lower():
            self.score += self.current_challenge["points"]
            self.completed += 1
            return True
        return False
        
    def play(self):
        """Play code challenge game."""
        self.game_state = "playing"
        self.start_timer()
        return f"Code Challenge Started! {len(self.challenges)} challenges await!"


# ============================================================================
# MATH RACE GAME
# ============================================================================

class MathRaceGame(ExtendedGamePlugin):
    """Quick math competition."""
    
    def __init__(self, duration=30):
        super().__init__("Math Race", "1.0")
        self.duration = duration
        self.current_problem = None
        self.problems_solved = 0
        self.score = 0
        self.correct_answers = 0
        self.time_remaining = duration
        
    def _generate_problem(self):
        """Generate random math problem."""
        operators = ['+', '-', '*', '/']
        operator = random.choice(operators)
        
        if operator == '+':
            a, b = random.randint(1, 100), random.randint(1, 100)
            answer = a + b
        elif operator == '-':
            a, b = random.randint(1, 100), random.randint(1, 100)
            answer = a - b
        elif operator == '*':
            a, b = random.randint(1, 12), random.randint(1, 12)
            answer = a * b
        else:  # division
            a = random.randint(1, 12) * random.randint(1, 10)
            b = random.randint(1, 12)
            answer = a // b
            
        problem = f"{a} {operator} {b}"
        return {"problem": problem, "answer": answer}
        
    def get_problem(self):
        """Get next math problem."""
        self.current_problem = self._generate_problem()
        return self.current_problem["problem"]
        
    def check_answer(self, answer):
        """Check if answer is correct."""
        if not self.current_problem:
            return False
            
        try:
            answer_int = int(float(answer))
            if answer_int == self.current_problem["answer"]:
                self.score += 10
                self.correct_answers += 1
                self.problems_solved += 1
                return True
        except:
            pass
        return False
        
    def update_time(self, elapsed):
        """Update remaining time."""
        self.time_remaining = max(0, self.duration - elapsed)
        return self.time_remaining <= 0
        
    def play(self):
        """Play math race game."""
        self.game_state = "playing"
        self.start_timer()
        return f"Math Race Started! {self.duration}s to solve as many as possible!"


# ============================================================================
# EXTENDED GAME MANAGER
# ============================================================================

class ExtendedGameManager:
    """Manages all extended games."""
    
    def __init__(self):
        self.games = {
            "snake": SnakeGame(),
            "pong": PongGame(),
            "puzzle": PuzzleGame(),
            "code_challenge": CodeChallengeGame(),
            "math_race": MathRaceGame()
        }
        self.current_game = None
        self.high_scores = {game: 0 for game in self.games}
        
    def get_game(self, game_name):
        """Get game by name."""
        return self.games.get(game_name.lower())
        
    def start_game(self, game_name):
        """Start a game."""
        game = self.get_game(game_name)
        if game:
            self.current_game = game
            game.reset()
            return game.play()
        return None
        
    def get_high_scores(self):
        """Get high scores for all games."""
        scores = {}
        for game_name, game in self.games.items():
            scores[game_name] = {
                "high_score": self.high_scores[game_name],
                "current_score": game.get_score()
            }
        return scores
        
    def update_high_score(self, game_name, score):
        """Update high score if current score is higher."""
        if score > self.high_scores.get(game_name, 0):
            self.high_scores[game_name] = score
            
    def get_statistics(self):
        """Get game statistics."""
        return {
            "total_games": len(self.games),
            "games_available": list(self.games.keys()),
            "high_scores": self.high_scores,
            "last_played": self.current_game.name if self.current_game else None
        }


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    print("Extended Games for Rijwal_Lang")
    print("=" * 50)
    print()
    
    manager = ExtendedGameManager()
    
    # List available games
    print("Available Games:")
    for game_name, game in manager.games.items():
        print(f"  - {game.name} ({game.version})")
    print()
    
    # Start a game
    print("Starting Snake Game...")
    print(manager.start_game("snake"))
    print()
    
    # Get statistics
    stats = manager.get_statistics()
    print(f"Total Games: {stats['total_games']}")
    print(f"Games: {', '.join(stats['games_available'])}")
