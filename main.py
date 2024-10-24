import tkinter as tk
from data import define_questions
from tkinter import messagebox, simpledialog

# Question Data Structure: Category -> [(Question, Answer, Points), ...]
jeopardy_questions = define_questions()

# Player data
players = [{"name": "Player 1", "score": 0}, {"name": "Player 2", "score": 0}]
current_player_index = 0
current_question = None
stealing_player = None
steal_attempt = False
round_type = "regular"  # Tracks the current round type

# Function to prompt the opponent for an answer to steal
def steal_attempt_window():
    steal_window = tk.Toplevel(window)
    steal_window.title("Steal Attempt")
    steal_window.configure(bg="blue")

    steal_label = tk.Label(steal_window,
                           text=f"Steal Attempt by {players[stealing_player]['name']}. Enter your answer:",
                           font=("Arial", 16), bg="blue", fg="white")
    steal_label.pack(pady=10)

    steal_answer_entry = tk.Entry(steal_window, font=("Arial", 16), width=30)
    steal_answer_entry.pack(pady=10)

    steal_submit_button = tk.Button(steal_window, text="Submit",
                                    command=lambda: handle_steal_answer(steal_answer_entry.get().strip().lower(),
                                                                        steal_window), font=("Arial", 16), bg="gold",
                                    fg="black")
    steal_submit_button.pack(pady=10)


# Function to handle the steal answer and scoring
def handle_steal_answer(answer, window):
    global stealing_player
    correct_answer = current_question[1].lower()

    if answer == correct_answer:
        points_stolen = current_question[2]
        players[stealing_player]['score'] += points_stolen
        feedback_label.config(
            text=f"{players[stealing_player]['name']} answered correctly! They gained {points_stolen} points.")
    else:
        points_stolen = current_question[2]
        players[stealing_player]['score'] -= points_stolen
        feedback_label.config(
            text=f"{players[stealing_player]['name']} answered wrong! They lost {points_stolen} points.")

    window.destroy()  # Close the steal window
    # Reset for next question
    reset_for_next_question()


# Function to reset for the next question
def reset_for_next_question():
    global current_question
    current_question = None
    switch_player()
    board_frame.grid(row=0, column=0, sticky="nsew")
    question_screen.grid_forget()



# Function to handle switching turns between players
def switch_player():
    global steal_attempt
    if steal_attempt:
        steal_attempt = False  # Reset steal attempt
        return
    global current_player_index
    current_player_index = (current_player_index + 1) % 2
    update_player_label()

# Function to update the player turn display
def update_player_label():
    player_turn_label.config(text=f"{players[current_player_index]['name']}'s Turn")
    score_label.config(
        text=f"{players[0]['name']}: {players[0]['score']} | {players[1]['name']}: {players[1]['score']}")

# Function to select a question
def select_question(category, index):
    global current_question
    question_data = jeopardy_questions[category][index]
    current_question = question_data

    # Hide the main board and show the question screen
    board_frame.grid_forget()
    question_screen.grid(row=0, column=0, sticky="nsew")

    # Adjust point value for Double Jeopardy
    if round_type == "double":
        question_data = (question_data[0], question_data[1], question_data[2] * 2)

    question_label.config(text=f"Question: {question_data[0]} (Points: {question_data[2]})")
    answer_entry.delete(0, tk.END)

    # Reset feedback label
    feedback_label.config(text="")
    # Disable the button after it's clicked
    question_buttons[category][index].config(state=tk.DISABLED)

# Function to check the answer
def check_answer():
    global current_question, stealing_player
    if current_question:
        player_answer = answer_entry.get().strip().lower()
        correct_answer = current_question[1].lower()
        question_value = current_question[2]

        if player_answer == correct_answer:
            players[current_player_index]['score'] += question_value
            feedback_label.config(text=f"Correct! You earned {question_value} points.")
            # Player gets to control the board again, so do not switch
            switch_player()  # Only switch if the answer was incorrect
        else:
            players[current_player_index]['score'] -= question_value
            feedback_label.config(
                text=f"Wrong! You lost {question_value} points. {players[(current_player_index + 1) % 2]['name']} can steal!")

            # Ask the opponent if they want to steal
            if messagebox.askyesno("Steal Opportunity",
                                   f"{players[(current_player_index + 1) % 2]['name']}, do you want to try to steal?"):
                stealing_player = (current_player_index + 1) % 2
                steal_attempt_window()  # Open a window for stealing answer
                return

        # Check if all questions have been answered
        if all(btn['state'] == 'disabled' for category in question_buttons.values() for btn in category):
            messagebox.showinfo("All Questions Answered", "Time for Final Jeopardy!")
            start_final_jeopardy()  # Start Final Jeopardy round
        else:
            current_question = None
            reset_for_next_question()


# Function to start the game
def start_game():
    players[0]["name"] = player1_entry.get()
    players[1]["name"] = player2_entry.get()
    start_screen.grid_forget()
    board_frame.grid(row=0, column=0, sticky="nsew")
    update_player_label()

# Test button to trigger end game
def trigger_end_game():
    players[0]['score'] = 300  # Set score for Player 1
    players[1]['score'] = 2500  # Set score for Player 2
    reset_game()  # Call the reset_game function to show final scoreboard


# Function to start Double Jeopardy
def start_double_jeopardy():
    global round_type
    round_type = "double"
    reset_for_next_question()
    messagebox.showinfo("Double Jeopardy!", "All questions are worth double points now!")

# Function to start Final Jeopardy
def start_final_jeopardy():
    global round_type
    round_type = "final"
    for player in players:
        wager = ask_wager(player['name'])
        if wager is not None:
            player['wager'] = wager
        else:
            player['wager'] = 0
    # Now show the Final Jeopardy question
    show_final_jeopardy_question()

# Function to ask player for wager in Final Jeopardy
def ask_wager(player_name):
    wager = simpledialog.askinteger("Wager", f"{player_name}, how much do you want to wager? (Current score: {players[current_player_index]['score']})", minvalue=0, maxvalue=players[current_player_index]['score'])
    return wager

# Function to show the Final Jeopardy question
def show_final_jeopardy_question():
    global current_question
    final_question = ("Gender roles may or may not exist for pokemon. However, different genders have unique characteristics. The same can be said for pokemon's mascot, Pikachu. What is the difference between a male and female pikachu?", "heart tail", 500)  # Example question

    current_question = final_question
    board_frame.grid_forget()
    final_jeopardy_screen.grid(row=0, column=0, sticky="nsew")
    final_question_label.config(text=f"Final Jeopardy Question: {final_question[0]} ")

    # Reset answer entry fields for both players
    final_answer_entry1.delete(0, tk.END)
    final_answer_entry2.delete(0, tk.END)

    # Enable both answer entry fields
    final_answer_entry1.config(state=tk.NORMAL)
    final_answer_entry2.config(state=tk.NORMAL)

# Function to check Final Jeopardy answer
def check_final_answer():
    correct_answer = current_question[1].lower()

    # Check Player 1's answer
    player1_answer = final_answer_entry1.get().strip().lower()
    player1_wager = players[0].get('wager', 0)

    if player1_answer == correct_answer:
        players[0]['score'] += player1_wager
        feedback_label.config(text=f"{players[0]['name']} answered correctly! They earned {player1_wager} points.")
    else:
        players[0]['score'] -= player1_wager
        feedback_label.config(text=f"{players[0]['name']} answered wrong! They lost {player1_wager} points.")

    # Check Player 2's answer
    player2_answer = final_answer_entry2.get().strip().lower()
    player2_wager = players[1].get('wager', 0)

    if player2_answer == correct_answer:
        players[1]['score'] += player2_wager
        feedback_label.config(text=f"{players[1]['name']} answered correctly! They earned {player2_wager} points.")
    else:
        players[1]['score'] -= player2_wager
        feedback_label.config(text=f"{players[1]['name']} answered wrong! They lost {player2_wager} points.")

    display_final_scoreboard()

def display_final_scoreboard():
    board_frame.grid_forget()
    final_scoreboard_screen = tk.Frame(window, bg="blue")
    final_scoreboard_screen.grid(row=0, column=0, sticky="nsew")

    winner = max(players, key=lambda player: player['score'])

    scoreboard_label = tk.Label(final_scoreboard_screen, text="Final Scoreboard", font=("Arial", 24), bg="blue", fg="white")
    scoreboard_label.pack(pady=20)

    for player in players:
        score_label = tk.Label(final_scoreboard_screen, text=f"{player['name']}: {player['score']} points", font=("Arial", 18), bg="blue", fg="white")
        score_label.pack(pady=10)

    winner_label = tk.Label(final_scoreboard_screen, text=f"The Winner is: {winner['name']}!", font=("Arial", 18), bg="green", fg="black")
    winner_label.pack(pady=20)

    # Optionally, add a button to restart the game or exit
    restart_button = tk.Button(final_scoreboard_screen, text="Restart Game", command=reset_game, font=("Arial", 18), bg="gold", fg="black")
    restart_button.pack(pady=20)

def show_final_scoreboard():
    scoreboard_message = "Final Scores:\n\n"
    winner = None
    highest_score = -float('inf')

    for player in players:
        scoreboard_message += f"{player['name']}: {player['score']} points\n"
        if player['score'] > highest_score:
            highest_score = player['score']
            winner = player['name']

    if winner:
        scoreboard_message += f"\nWinner: {winner}!"

    messagebox.showinfo("Final Scoreboard", scoreboard_message)

# Function to reset the game after Final Jeopardy
def reset_game():
    global round_type
    round_type = "regular"
    for player in players:
        player['wager'] = 0
    show_final_scoreboard()  # Show final scoreboard before resetting for a new game
    reset_for_next_question()
    board_frame.grid(row=0, column=0, sticky="nsew")
    messagebox.showinfo("Game Over", "Thanks for playing!")

# Initialize tkinter window
window = tk.Tk()
window.title("Iskander's Jeopardy-uru")
window.configure(bg="blue")

# Start screen for entering player names
start_screen = tk.Frame(window, bg="blue")
start_screen.grid(row=0, column=0, sticky="nsew")

welcome_label = tk.Label(start_screen, text="Welcome to Jeopardy!", font=("Arial", 24), bg="blue", fg="white")
welcome_label.pack(pady=20)

player1_label = tk.Label(start_screen, text="Enter Player 1 Name:", font=("Arial", 18), bg="blue", fg="white")
player1_label.pack(pady=5)
player1_entry = tk.Entry(start_screen, font=("Arial", 18))
player1_entry.pack(pady=5)

player2_label = tk.Label(start_screen, text="Enter Player 2 Name:", font=("Arial", 18), bg="blue", fg="white")
player2_label.pack(pady=5)
player2_entry = tk.Entry(start_screen, font=("Arial", 18))
player2_entry.pack(pady=5)

start_button = tk.Button(start_screen, text="Start Game", command=start_game, font=("Arial", 18), bg="gold", fg="black")
start_button.pack(pady=20)

test_button = tk.Button(start_screen, text="Trigger End Game", command=trigger_end_game, font=("Arial", 18), bg="red", fg="white")
test_button.pack(pady=20)

# Main game board
board_frame = tk.Frame(window, bg="blue")

# Player turn and score display at the top
score_label = tk.Label(board_frame, text="", font=("Arial", 18), bg="blue", fg="white")
score_label.grid(row=0, column=0, columnspan=5, pady=10)

# Player turn display
player_turn_label = tk.Label(board_frame, text="", font=("Arial", 18), bg="blue", fg="white")
player_turn_label.grid(row=1, column=0, columnspan=5)

# Create a dictionary to store the buttons for each category
question_buttons = {}

# Display categories and point values
for category_index, (category, questions) in enumerate(jeopardy_questions.items()):
    # Add category label
    category_label = tk.Label(board_frame, text=category, font=("Arial", 14, "bold"), bg="blue", fg="white")
    category_label.grid(row=2, column=category_index, padx=10, pady=5)

    # Initialize list for buttons in this category
    question_buttons[category] = []

    # Create buttons for each question (100, 200, 300, 400, 500 points)
    for question_index, (question, answer, points) in enumerate(questions):
        btn = tk.Button(board_frame, text=f"${points}", width=10, height=2,
                        bg="gold", fg="black", font=("Arial", 12, "bold"),
                        command=lambda cat=category, idx=question_index: select_question(cat, idx))
        btn.grid(row=question_index + 3, column=category_index, padx=5,
                 pady=5)
        question_buttons[category].append(btn)

# Question screen to display questions
question_screen = tk.Frame(window, bg="blue")

question_label = tk.Label(question_screen, text="", font=("Arial", 18), bg="blue", fg="white", wraplength=500)
question_label.pack(pady=20)

answer_entry = tk.Entry(question_screen, font=("Arial", 18), width=30)
answer_entry.pack(pady=10)

submit_button = tk.Button(question_screen, text="Submit Answer", command=check_answer, font=("Arial", 18), bg="gold",
                          fg="black")
submit_button.pack(pady=10)

feedback_label = tk.Label(question_screen, text="", font=("Arial", 16), bg="blue", fg="white")
feedback_label.pack(pady=20)

# Final Jeopardy Screen
final_jeopardy_screen = tk.Frame(window, bg="blue")

final_question_label = tk.Label(final_jeopardy_screen, text="", font=("Arial", 18), bg="blue", fg="white", wraplength=500)
final_question_label.pack(pady=20)

# Entry for Player 1's answer
final_answer_entry1 = tk.Entry(final_jeopardy_screen, font=("Arial", 18), width=30)
final_answer_entry1.pack(pady=10)

# Entry for Player 2's answer
final_answer_entry2 = tk.Entry(final_jeopardy_screen, font=("Arial", 18), width=30)
final_answer_entry2.pack(pady=10)

final_submit_button = tk.Button(final_jeopardy_screen, text="Submit Answer", command=check_final_answer, font=("Arial", 18), bg="gold", fg="black")
final_submit_button.pack(pady=10)

# Run the GUI loop
window.mainloop()
