import random

def lifeline_50_50(options, correct_option):
    # Removes two incorrect options from the multiple-choice answers.
    incorrect_options = [opt for opt in options if opt != correct_option]
    options_to_remove = random.sample(incorrect_options, 2)
    return [opt for opt in options if opt not in options_to_remove]

def lifeline_skip_question():
    # Allows players to skip a difficult question without answering.
    return True  # Indicate that the question should be skipped

def lifeline_double_chance():
    # Lets players guess twice on a single question.
    return True  # Indicate that the player has a double chance

def lifeline_pause_timer():
    # Temporarily stops the countdown, giving players extra time to think before answering.
    return True  # Indicate that the timer should be paused

def lifeline_change_question(all_questions, current_question_index):
    # Replaces the current question with a completely new one.
    new_question_index = random.choice([i for i in range(len(all_questions)) if i != current_question_index])
    return new_question_index  # Return the index of the new question
