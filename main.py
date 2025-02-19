import pygame
import random
import sys
from pygame import mixer
import os
from end import main as end_game
from highscore import save_high_score

from easy import easy_questions
from medium import medium_questions
from hard import hard_questions
from lifeline import lifeline_50_50, lifeline_skip_question, lifeline_double_chance, lifeline_pause_timer, lifeline_change_question

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load assets
background_image = pygame.image.load("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/background.jpg")
winner_background_image = pygame.image.load("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/winner.jpg")
correct_sound = mixer.Sound("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/correct.wav")
wrong_sound = mixer.Sound("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/wrong.mp3")
mixer.music.load("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/music.wav")
mixer.music.play(-1)  # Play background music in a loop

# Load custom fonts
knightwarrior_font = pygame.font.Font("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/KnightWarrior.otf", 28)
big_knightwarrior_font = pygame.font.Font("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/KnightWarrior.otf", 40)
question_font = pygame.font.Font("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/CaviarDreams_Bold.ttf", 28)
golden_font = pygame.font.Font("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/CaviarDreams_Bold.ttf", 28)
winner_font = pygame.font.Font("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/KnightWarrior.otf", 60)

# ---------------------------
# Pygame Setup and Constants
# ---------------------------
#game window
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_CHARCOAL = (54, 69, 79)
YELLOW = (255, 255, 0)
GOLDEN = (255, 215, 0)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 40)

# ---------------------------
# Helper: Number to Words
# ---------------------------
def num_to_words(n):
    # A simple converter for numbers up to billions.
    if n == 0:
        return "zero"
    
    under_20 = ["", "one", "two", "three", "four", "five", "six", "seven",
                "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
                "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
            "eighty", "ninety"]
    thousands = ["", "thousand", "million", "billion"]

    def words(num, idx=0):
        if num == 0:
            return []
        elif num < 20:
            return [under_20[num]] + ([thousands[idx]] if thousands[idx] else [])
        elif num < 100:
            return [tens[num // 10]] + words(num % 10, 0) + ([thousands[idx]] if thousands[idx] and num % 10 == 0 else [])
        else:
            return [under_20[num // 100]] + ["hundred"] + words(num % 100, 0) + ([thousands[idx]] if thousands[idx] and num % 100 == 0 else [])
    
    result = []
    idx = 0
    while n:
        n, rem = divmod(n, 1000)
        if rem:
            result = words(rem, idx) + result
        idx += 1
    return " ".join([w for w in result if w])

def format_prize(n):
    # Returns a string with NPR and words (e.g., "NPR 1,000 – One Thousand Nepalese Rupees")
    return f"NPR {n:,} – {num_to_words(n).capitalize()}"

# ---------------------------
# Function: Generate Options for a Question
# ---------------------------
def get_options(question_data):
    # Always include the correct answer and choose 3 random wrong answers from the set of 5.
    wrong_options = random.sample(question_data["wrong"], 3)
    options = wrong_options + [question_data["correct"]]
    random.shuffle(options)
    return options

# ---------------------------
# UI Helper: Draw Text Centered
# ---------------------------
def draw_text_center(surface, text, font, color, center):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(center=center)
    surface.blit(text_obj, rect)

# ---------------------------
# UI Helper: Draw Text Centered with Line Breaks
# ---------------------------
def draw_text_center_multiline(surface, text, font, color, center, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width, _ = font.size(word + ' ')
        if current_width + word_width > max_width:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width
        else:
            current_line.append(word)
            current_width += word_width

    lines.append(' '.join(current_line))

    total_height = len(lines) * font.get_linesize()
    start_y = center[1] - total_height // 2

    for i, line in enumerate(lines):
        text_obj = font.render(line, True, color)
        rect = text_obj.get_rect(center=(center[0], start_y + i * font.get_linesize()))
        surface.blit(text_obj, rect)

# ---------------------------
# Button Class
# ---------------------------
class Button:
    def __init__(self, text, font, color, rect, bg_color=GRAY):
        self.text = text
        self.font = font
        self.color = color
        self.rect = pygame.Rect(rect)
        self.bg_color = bg_color
        self.text_surf = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ---------------------------
# Main Game Loop
# ---------------------------
def ask_username():
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    pygame.display.set_caption("Enter Username")

    input_box = pygame.Rect(500, 400, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)

    # Load background image for username screen
    background_image = pygame.image.load("/home/bishal-shrestha/MyProjects/UbuntuPythonFiles/Files/assets/user.jpg")

    while True:
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(background_image, (screen.get_width(), screen.get_height())), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Display prompt text
        prompt_surf = golden_font.render("Enter a Username", True, GOLDEN)
        prompt_rect = prompt_surf.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(prompt_surf, prompt_rect)

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

def main():
    from gamemanager import end_screen  # Import inside function to avoid circular import

    global screen, screen_width, screen_height, questions_options, current_question_index, timer_paused, total_questions, question_start_time, double_chance_used, double_chance_attempts, all_questions

    # For each category, select a fixed number of questions.
    selected_easy = random.sample(easy_questions, 3)
    selected_medium = random.sample(medium_questions, 6)
    selected_hard = random.sample(hard_questions, 6)

    # Combine in order: Easy (1-3), Medium (4-9), Hard (10-15)
    all_questions = selected_easy + selected_medium + selected_hard

    # Ensure all questions are unique
    unique_questions = []
    for q in all_questions:
        if q not in unique_questions:
            unique_questions.append(q)
    all_questions = unique_questions

    # Prize levels for each correct answer (15 questions)
    prize_levels = [25000, 50000, 100000, 200000, 400000, 800000, 1600000, 3200000, 6400000, 12800000, 25600000, 51200000, 102400000, 204800000, 700000000]

    username = ask_username()
    current_question_index = 0
    total_questions = len(all_questions)
    current_prize = 0
    running = True
    selected_option = None  # to store clicked option
    feedback = ""
    show_feedback = False
    feedback_timer = 0
    selected_option_index = 0  # to store the index of the selected option
    locked_option = False  # to indicate if an option is locked
    lifelines_used = {
        "50_50": False,
        "skip": False,
        "double_chance": False,
        "pause_timer": False,
        "change_question": False
    }
    lifelines_used_count = 0  # to count the number of lifelines used for the current question
    double_chance_used = False  # to track if double chance is used
    double_chance_attempts = 0  # to track the number of attempts for double chance
    paused_time = 0  # to track paused time
    timer_paused = False  # to track if the timer is paused

    # Timer: Set start time for the current question
    question_start_time = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    # Pre-calculate options for each question.
    questions_options = []
    for q in all_questions:
        questions_options.append(get_options(q))
    
    while running:
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(background_image, (screen_width, screen_height)), (0, 0))  # Draw background image
        
        # Determine the time limit based on current question index.
        if current_question_index < 3:
            time_limit = 15
        elif current_question_index < 9:
            time_limit = 20
        else:
            time_limit = 30
        
        # Calculate elapsed time (in seconds) for the current question.
        if not timer_paused:
            elapsed_time = (pygame.time.get_ticks() - question_start_time - paused_time) / 1000
        else:
            elapsed_time = paused_time / 1000
        time_left = max(0, time_limit - int(elapsed_time))
        
        # Check if time has run out for the current question.
        if elapsed_time > time_limit and not show_feedback:
            feedback = "Time's up! Game Over."
            show_feedback = True
            feedback_timer = pygame.time.get_ticks()
        
        # Display timer on the screen (top-right corner).
        timer_text = font.render(f"Time Left: {time_left}s", True, GOLDEN)
        screen.blit(timer_text, (screen_width - 150, 20))

        # Draw Quit button below the timer
        quit_button = Button("Quit", font, BLACK, (screen_width - 150, 70, 100, 40), bg_color=YELLOW)
        quit_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN and not show_feedback:
                if event.key == pygame.K_DOWN:
                    selected_option_index = (selected_option_index + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option_index = (selected_option_index - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if locked_option:
                        selected_option = options[selected_option_index]
                        # Check if answer is correct
                        correct_answer = all_questions[current_question_index]["correct"]
                        if selected_option == correct_answer:
                            feedback = "Correct!"
                            current_prize = prize_levels[current_question_index]
                            correct_sound.play()  # Play correct sound effect
                            if double_chance_used:
                                lifelines_used["double_chance"] = True  # Mark double chance as used
                            show_feedback = True
                            feedback_timer = pygame.time.get_ticks()
                        else:
                            if double_chance_used and double_chance_attempts < 1:
                                double_chance_attempts += 1
                                feedback = "Wrong Answer! Try Again."
                                wrong_sound.play()  # Play wrong sound effect
                                locked_option = False
                                show_feedback = False
                            else:
                                feedback = "Wrong Answer! Game Over."
                                wrong_sound.play()  # Play wrong sound effect
                                show_feedback = True
                                feedback_timer = pygame.time.get_ticks()
                    else:
                        locked_option = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if quit_button.is_clicked((mx, my)):
                    running = False
                    pygame.quit()
                    sys.exit()
                if not show_feedback:
                    for i, button in enumerate(option_buttons):
                        if button.is_clicked((mx, my)):
                            if locked_option:
                                selected_option = button.text
                                selected_option_index = i
                                # Check if answer is correct
                                correct_answer = all_questions[current_question_index]["correct"]
                                if selected_option == correct_answer:
                                    feedback = "Correct!"
                                    current_prize = prize_levels[current_question_index]
                                    correct_sound.play()  # Play correct sound effect
                                    if double_chance_used:
                                        lifelines_used["double_chance"] = True  # Mark double chance as used
                                    show_feedback = True
                                    feedback_timer = pygame.time.get_ticks()
                                else:
                                    if double_chance_used and double_chance_attempts < 1:
                                        double_chance_attempts += 1
                                        feedback = "Wrong Answer! Try Again."
                                        wrong_sound.play()  # Play wrong sound effect
                                        locked_option = False
                                        show_feedback = False
                                    else:
                                        feedback = "Wrong Answer! Game Over."
                                        wrong_sound.play()  # Play wrong sound effect
                                        show_feedback = True
                                        feedback_timer = pygame.time.get_ticks()
                            else:
                                selected_option_index = i
                                locked_option = True
                            break
                    for lifeline_button in lifeline_buttons:
                        if lifeline_button.is_clicked((mx, my)) and lifeline_button.active and lifelines_used_count < 3:
                            if confirm_lifeline_use(lifeline_button.text):
                                lifeline_button.action()
                                lifeline_button.active = False
                                lifelines_used[lifeline_button.key] = True
                                lifelines_used_count += 1
                            break

        # If all questions answered, display winning message
        if current_question_index >= total_questions:
            screen.fill(BLACK)
            screen.blit(pygame.transform.scale(winner_background_image, (screen_width, screen_height)), (0, 0))  # Draw winner background image
            draw_text_center(screen, "Congratulations, you are a winner!", winner_font, GOLDEN, (screen_width//2, screen_height//2 - 40))
            prize_text = format_prize(current_prize)
            draw_text_center(screen, f"Your prize: {prize_text}", big_knightwarrior_font, GOLDEN, (screen_width//2, screen_height - 40))
            pygame.display.update()
            winner_screen = True
            while winner_screen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        save_high_score(username, current_prize, current_question_index)
                        winner_screen = False
                        end_screen()
            running = False
            continue

        # Display current question and options.
        qdata = all_questions[current_question_index]
        options = questions_options[current_question_index]

        # Draw question number in the leftmost corner.
        question_number_text = font.render(f"Question {current_question_index + 1} / {total_questions}", True, GOLDEN)
        screen.blit(question_number_text, (20, 20))

        # Display the question text using question_font
        draw_text_center_multiline(screen, qdata["question"], golden_font, GOLDEN, (screen_width//2, screen_height//2 - 200), screen_width - 100)
        
        # Draw option buttons
        option_buttons = []
        start_y = screen_height // 2 - 100
        gap = 60
        for i, option in enumerate(options):
            if show_feedback:
                if option == correct_answer:
                    bg_color = GREEN
                elif option == selected_option:
                    bg_color = RED
                else:
                    bg_color = GRAY
            else:
                bg_color = YELLOW if locked_option and i == selected_option_index else (BLUE if i == selected_option_index else GRAY)
            rect = pygame.Rect(screen_width // 2 - 300, start_y + i * gap, 600, 40)
            button = Button(option, font, BLACK, rect, bg_color=bg_color)
            option_buttons.append(button)
            button.draw(screen)

        # Display prize money in the upper center
        prize_text_number = f"NPR {current_prize:,}"
        draw_text_center(screen, prize_text_number, golden_font, GOLDEN, (screen_width//2, 40))

        # Display prize money in words in the center of the bottom
        prize_text_words = num_to_words(current_prize).capitalize()
        draw_text_center(screen, prize_text_words, golden_font, GOLDEN, (screen_width//2, screen_height - 40))

        # Draw lifeline buttons
        lifeline_buttons = []
        lifeline_texts = ["50-50", "Skip", "Double Chance", "Pause Timer", "Change Question"]
        lifeline_keys = ["50_50", "skip", "double_chance", "pause_timer", "change_question"]
        lifeline_actions = [
            lambda: use_lifeline_50_50(options, qdata["correct"]),
            lambda: use_lifeline_skip_question(),
            lambda: use_lifeline_double_chance(),
            lambda: use_lifeline_pause_timer(),
            lambda: use_lifeline_change_question()
        ]
        for i, (text, key, action) in enumerate(zip(lifeline_texts, lifeline_keys, lifeline_actions)):
            bg_color = WHITE if lifelines_used[key] else YELLOW
            if i < 3:
                rect = pygame.Rect(screen_width - 170, start_y + i * gap, 150, 40)
            else:
                rect = pygame.Rect(20, start_y + (i - 3) * gap, 150, 40)
            button = Button(text, font, BLACK, rect, bg_color=bg_color)
            button.action = action
            button.active = not lifelines_used[key]
            button.key = key
            lifeline_buttons.append(button)
            button.draw(screen)

        # If feedback needs to be shown (Correct / Wrong / Time's up)
        if show_feedback:
            draw_text_center(screen, feedback, big_font, GREEN if feedback=="Correct!" else RED, (screen_width//2, start_y + 4 * gap + 40))
            # Show feedback for 1.5 seconds before proceeding.
            if pygame.time.get_ticks() - feedback_timer > 1500:
                if feedback == "Correct!":
                    current_question_index += 1
                    # Reset question start time for the next question.
                    question_start_time = pygame.time.get_ticks()
                    paused_time = 0
                    timer_paused = False
                    double_chance_used = False
                    double_chance_attempts = 0
                else:
                    # Game over, so display final prize and then break.
                    draw_text_center(screen, f"Final Prize: {format_prize(current_prize)}", big_font, GREEN, (screen_width//2, start_y + 4 * gap + 100))
                    pygame.display.update()
                    pygame.time.delay(3000)
                    save_high_score(username, current_prize, current_question_index)
                    end_game()
                    running = False
                show_feedback = False
                selected_option = None
                locked_option = False
                lifelines_used_count = 0  # Reset lifeline usage count for the next question

        pygame.display.update()
        clock.tick(30)

def confirm_lifeline_use(lifeline_name):
    # Display confirmation dialog for lifeline use
    # Return True if user confirms, otherwise False
    return True  # For simplicity, always return True in this example

def use_lifeline_50_50(options, correct_option):
    global questions_options, current_question_index
    questions_options[current_question_index] = lifeline_50_50(options, correct_option)

def use_lifeline_skip_question():
    global current_question_index, total_questions
    current_question_index = (current_question_index + 1) % total_questions

def use_lifeline_double_chance():
    global double_chance_used, double_chance_attempts
    double_chance_used = True
    double_chance_attempts = 0

def use_lifeline_pause_timer():
    global paused_time, timer_paused, question_start_time
    if not timer_paused:
        paused_time = pygame.time.get_ticks() - question_start_time
        timer_paused = True
    else:
        question_start_time = pygame.time.get_ticks() - paused_time
        timer_paused = False

def use_lifeline_change_question():
    global questions_options, current_question_index, all_questions
    current_question = all_questions[current_question_index]
    remaining_questions = [q for q in all_questions if q != current_question and q["question"] != current_question["question"]]
    new_question = random.choice(remaining_questions)
    all_questions[current_question_index] = new_question
    questions_options[current_question_index] = get_options(new_question)

if __name__ == "__main__":
    # For each category, select a fixed number of questions.
    selected_easy = random.sample(easy_questions, 3)
    selected_medium = random.sample(medium_questions, 6)
    selected_hard = random.sample(hard_questions, 6)

    # Combine in order: Easy (1-3), Medium (4-9), Hard (10-15)
    all_questions = selected_easy + selected_medium + selected_hard

    # Ensure all questions are unique
    unique_questions = []
    for q in all_questions:
        if q not in unique_questions:
            unique_questions.append(q)
    all_questions = unique_questions

    # Prize levels for each correct answer (15 questions)
    prize_levels = [25000, 50000, 100000, 200000, 400000, 800000, 1600000, 3200000, 6400000, 12800000, 25600000, 51200000, 102400000, 204800000, 700000000]

    main()
