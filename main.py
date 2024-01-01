import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()

        # Snake initialization with head and tail
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"

        # Food initialization
        self.food = self.create_food()

        # Score variables
        self.score = 0
        self.score_label = tk.Label(self.master, text="Score: {}".format(self.score))
        self.score_label.pack()

        # AI Snake initialization
        self.ai_snake = [(300, 300), (310, 300), (320, 300)]
        self.ai_direction = "Left"

        self.master.bind("<KeyPress>", self.change_direction)

        self.update()

    def create_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red", tags="food")
        return food

    def move_snake(self, snake):
        head = snake[0]
        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        # Remove the tail if not consuming food
        if snake[0] not in self.canvas.coords(self.food):
            snake.pop()

        # Check for collisions
        if (
            new_head in snake
            or new_head[0] < 0
            or new_head[1] < 0
            or new_head[0] >= 400
            or new_head[1] >= 400
        ):
            self.game_over()

        snake.insert(0, new_head)

    def update(self):
        self.move_snake(self.snake)
        self.move_snake(self.ai_snake)

        head = self.snake[0]

        # Check for food collision
        if head in self.canvas.coords(self.food):
            self.score += 1
            self.score_label.config(text="Score: {}".format(self.score))
            self.snake.append((0, 0))  # Just to increase the length
            self.canvas.delete("food")
            self.food = self.create_food()

        # Draw the snake
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake")

        # Draw the AI snake
        self.canvas.delete("ai_snake")
        for segment in self.ai_snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="blue", tags="ai_snake")

        # Update the canvas
        self.master.after(200, self.update)

    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

    def game_over(self):
        self.canvas.create_text(200, 200, text="Game Over", font=("Helvetica", 16), fill="white")
        self.master.after_cancel(self.update_id)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
