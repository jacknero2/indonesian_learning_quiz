#!/usr/bin/env python3

import csv
import os
import random
import webbrowser
import pandas
import tkinter as tk
import tkinter.font as tkFont  # Import tkinter font module
import pygame
from PIL import Image, ImageTk

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# --------------------------------------
# GLOBAL MNEMONIC FILE (kept the same for simplicity)
# --------------------------------------
mnemonic_file = "mnemonics.csv"
mnemonics = []
# Ensure the mnemonic file exists
with open(mnemonic_file, "a"):
    pass

with open(mnemonic_file, "r", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        mnemonics.append(row)

result_file = "results.txt"

# --------------------------------------
# HELPER FUNCTIONS
# --------------------------------------
def search(word: str, dataset: list) -> list:
    """Check if 'word' is in 'dataset'. Return [True, row, indexes] or [False, []]."""
    indexes = [idx for idx, sublist in enumerate(dataset) if word in sublist]
    if not indexes:
        return [False, []]
    return [True, dataset[indexes[0]], indexes]

def open_audio(audio: bool, audio_ai: bool, word: str, language: str) -> None:
    """
    Open relevant audio websites if enabled.
    For Indonesian, the URLs use "#ind" and "indonesian" paths;
    for Italian, we use "#it" and "italian".
    """
    if language.lower() == "indonesian":
        url_forvo = f"https://forvo.com/word/{word}/#ind"
        url_howtopronounce = f"https://www.howtopronounce.com/indonesian/{word}"
    elif language.lower() == "italian":
        url_forvo = f"https://forvo.com/word/{word}/#it"
        url_howtopronounce = f"https://www.howtopronounce.com/italian/{word}"
    else:
        url_forvo = f"https://forvo.com/word/{word}/"
        url_howtopronounce = f"https://www.howtopronounce.com/english/{word}"
    if audio:
        webbrowser.open(url_forvo)
    if audio_ai:
        webbrowser.open(url_howtopronounce)

def overwrite_mnemonic(word: str, new_mnemonic: str):
    """
    Overwrite or add a mnemonic for 'word' with 'new_mnemonic'
    (no extra prompts—just do it if the user typed something).
    """
    found = search(word, mnemonics)
    if not found[0]:
        with open(mnemonic_file, "a", newline="") as f:
            f.write(f"{word},{new_mnemonic}\n")
        mnemonics.append([word, new_mnemonic])
    else:
        info = pandas.read_csv(mnemonic_file, header=None, names=["word", "mnemonic"])
        row_index = found[2][0]
        info.loc[row_index, "mnemonic"] = new_mnemonic
        info.to_csv(mnemonic_file, index=False)
        mnemonics[row_index] = [word, new_mnemonic]

def play_local_sound(sound_file: str):
    """Play a sound file using pygame's mixer."""
    try:
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
    except Exception as e:
        print(f"Error playing {sound_file}: {e}")

# --------------------------------------
# TKINTER APP
# --------------------------------------
class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Set the default font for all widgets to Courier
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Courier", size=16)

        # Start with the main window hidden
        self.withdraw()
        # Open your image (using a PNG is recommended on macOS)
        icon_img = Image.open("open.ico")  # Use your PNG file with rounded edges

        # Resize the image to a suitable size for macOS title bar icons (try 64x64)
        icon_img = icon_img.resize((64, 64), Image.LANCZOS)

        # Convert the resized image to a Tkinter PhotoImage
        icon_photo = ImageTk.PhotoImage(icon_img)

        # Set the icon for your Tkinter app; also keep a reference to prevent garbage collection
        self.icon_photo = icon_photo
        self.iconphoto(True, self.icon_photo)

        # Set the overall background to light blue
        self.configure(bg="light blue")
        
        # Define window dimensions
        width = 800
        height = 600

        # Calculate the center position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set geometry and center the window
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title("Language Quiz")
        
        # Bring window to the front and force focus
        self.lift()
        self.attributes("-topmost", True)
        self.focus_force()
        self.after(500, lambda: self.attributes("-topmost", False))

        # "CLI flags" as instance variables
        self.ordered = False
        self.save = False
        self.target = False
        self.audio = False
        self.audio_ai = False
        self.mnemonic = False
        self.cycles = 1
        self.length = 5
        self.keyword = ""
        # New variable for language selection
        self.version = "Indonesian"  # default value
        
        # Quiz data will be loaded later based on version
        self.data = []
        
        # Quiz data
        self.score = 0
        self.review_words = []
        self.current_cycle = 0
        self.current_question = 0
        self.answer_checked = False  # State variable for two-step submission

        # Frames
        self.config_frame = None
        self.quiz_frame = None
        self.results_frame = None

        # Load feedback images and scale them down
        self.happy_img = tk.PhotoImage(file="audio-visual-library/happy_penguin.png").subsample(4, 4)
        self.sad_img = tk.PhotoImage(file="audio-visual-library/sad_penguin.png").subsample(4, 4)

        # Show splash screen first
        self.show_splash_screen()

    def show_splash_screen(self):
        """Display the splash screen with open.png and bold 'PengLang' in Courier font."""
        self.splash = tk.Toplevel(self)
        self.splash.overrideredirect(True)  # Remove window decorations
        self.splash.attributes("-topmost", True)
        
        width, height = 800, 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        self.splash.configure(bg="light blue")
        
        canvas = tk.Canvas(self.splash, width=width, height=height, highlightthickness=0, bg="light blue")
        canvas.pack()

        try:
            self.splash_img = tk.PhotoImage(file="audio-visual-library/open.png")
        except Exception as e:
            print(f"Error loading open.png: {e}")
            self.splash_img = None
        
        if self.splash_img:
            canvas.create_image(width // 2, height // 2, image=self.splash_img)
        else:
            canvas.create_text(width // 2, height // 2, text="Welcome!",
                               font=("Courier", 24), fill="black")
        
        canvas.create_text(width // 2, height // 2, text="PengLang",
                           font=("Courier", 150, "bold"), fill="#C99700", anchor="center")
        
        self.splash.update()  # Force the splash screen to render

        play_local_sound("audio-visual-library/open.mp3")
        
        # After 3 seconds, start fading out the splash screen
        self.after(3000, lambda: self.fade_out_splash(1.0))

    def fade_out_splash(self, alpha):
        """Gradually reduce the splash screen opacity to create a fade-out effect."""
        alpha -= 0.05
        if alpha <= 0:
            self.splash.destroy()
            self.deiconify()  # Show the main window
            self.show_language_menu()  # Show language selection next
        else:
            self.splash.attributes("-alpha", alpha)
            self.after(50, lambda: self.fade_out_splash(alpha))

    def show_language_menu(self):
        """Show a separate language selection menu before quiz configuration."""
        self.lang_menu = tk.Toplevel(self)
        self.lang_menu.title("Select Language")
        self.lang_menu.configure(bg="light blue")
        self.lang_menu.geometry("400x200")
        # Center the language menu on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (200 // 2)
        self.lang_menu.geometry(f"400x200+{x}+{y}")

        tk.Label(self.lang_menu, text="Select Quiz Language", font=("Courier", 18, "bold"),
                 bg="light blue", fg="black").pack(pady=20)

        self.lang_var = tk.StringVar(value=self.version)
        tk.Radiobutton(self.lang_menu, text="Indonesian", variable=self.lang_var,
                       value="Indonesian", font=("Courier", 14), bg="light blue", fg="black")\
            .pack(anchor="w", padx=40)
        tk.Radiobutton(self.lang_menu, text="Italian", variable=self.lang_var,
                       value="Italian", font=("Courier", 14), bg="light blue", fg="black")\
            .pack(anchor="w", padx=40)

        tk.Button(self.lang_menu, text="Continue", command=self.language_selected,
                  font=("Courier", 16), bg="light blue", fg="black")\
            .pack(pady=20)

        # Make sure this menu stays on top until selection is made.
        self.lang_menu.attributes("-topmost", True)

    def language_selected(self):
        """Callback when a language is selected; save selection and close menu."""
        self.version = self.lang_var.get()
        self.lang_menu.destroy()
        self.build_config_screen()

    def build_config_screen(self):
        """Screen to let the user set quiz options (language already chosen)."""
        if self.config_frame:
            self.config_frame.destroy()

        self.config_frame = tk.Frame(self, bg="light blue")
        self.config_frame.pack(padx=20, pady=20)

        tk.Label(self.config_frame, text="Quiz Configuration", font=("Courier", 18, "bold"),
                 bg="light blue", fg="black").pack(pady=10)

        self.ordered_var = tk.BooleanVar(value=self.ordered)
        tk.Checkbutton(self.config_frame, text="Ordered", variable=self.ordered_var,
                       bg="light blue", fg="black").pack(anchor="w")

        self.save_var = tk.BooleanVar(value=self.save)
        tk.Checkbutton(self.config_frame, text="Save results", variable=self.save_var,
                       bg="light blue", fg="black").pack(anchor="w")

        self.target_var = tk.BooleanVar(value=self.target)
        tk.Checkbutton(self.config_frame, text="Answer in target language", variable=self.target_var,
                       bg="light blue", fg="black").pack(anchor="w")

        self.audio_var = tk.BooleanVar(value=self.audio)
        tk.Checkbutton(self.config_frame, text="Audio Forvo", variable=self.audio_var,
                       bg="light blue", fg="black").pack(anchor="w")

        self.audio_ai_var = tk.BooleanVar(value=self.audio_ai)
        tk.Checkbutton(self.config_frame, text="Audio AI", variable=self.audio_ai_var,
                       bg="light blue", fg="black").pack(anchor="w")

        self.mnemonic_var = tk.BooleanVar(value=self.mnemonic)
        tk.Checkbutton(self.config_frame, text="Add Mnemonic", variable=self.mnemonic_var,
                       bg="light blue", fg="black").pack(anchor="w")

        tk.Label(self.config_frame, text="Quiz Length:", bg="light blue", fg="black")\
            .pack(anchor="w", pady=(10,0))
        self.length_var = tk.IntVar(value=self.length)
        tk.Entry(self.config_frame, textvariable=self.length_var, width=5, bg="white", fg="black")\
            .pack(anchor="w", pady=(0,10))

        tk.Label(self.config_frame, text="Number of Cycles:", bg="light blue", fg="black")\
            .pack(anchor="w")
        self.cycles_var = tk.IntVar(value=self.cycles)
        tk.Entry(self.config_frame, textvariable=self.cycles_var, width=5, bg="white", fg="black")\
            .pack(anchor="w", pady=(0,10))

        tk.Label(self.config_frame, text="Keyword to search:", bg="light blue", fg="black")\
            .pack(anchor="w")
        self.keyword_var = tk.StringVar(value=self.keyword)
        tk.Entry(self.config_frame, textvariable=self.keyword_var, width=20, bg="white", fg="black")\
            .pack(anchor="w", pady=(0,10))

        tk.Button(self.config_frame, text="Start Quiz", command=self.start_quiz,
                  font=("Courier", 16), bg="light blue", fg="black")\
            .pack(pady=10)

    def start_quiz(self):
        """Grab user settings, load the proper CSV file, do optional search, then begin the quiz."""
        self.ordered = self.ordered_var.get()
        self.save = self.save_var.get()
        self.target = self.target_var.get()
        self.audio = self.audio_var.get()
        self.audio_ai = self.audio_ai_var.get()
        self.mnemonic = self.mnemonic_var.get()
        self.length = self.length_var.get()
        self.cycles = self.cycles_var.get()
        self.keyword = self.keyword_var.get()

        data_file = "indonesian_data.csv" if self.version.lower() == "indonesian" else "italian_data.csv"
        self.data = []
        try:
            with open(data_file, "r", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.data.append(row)
        except Exception as e:
            print(f"Error loading {data_file}: {e}")
            return

        if self.keyword:
            found = search(self.keyword, self.data)
            if found[0]:
                tk.Label(self.config_frame, text=f"'{self.keyword}' is in the database.",
                         fg="green", bg="light blue", font=("Courier", 12))\
                    .pack()
            else:
                tk.Label(self.config_frame, text=f"'{self.keyword}' is NOT in the database.",
                         fg="red", bg="light blue", font=("Courier", 12))\
                    .pack()

        self.score = 0
        self.review_words = []
        self.current_cycle = 0
        self.current_question = 0

        self.config_frame.destroy()
        self.build_quiz_screen()

    def build_quiz_screen(self):
        """Create the quiz screen layout."""
        self.quiz_frame = tk.Frame(self, bg="light blue")
        self.quiz_frame.pack(padx=20, pady=20)

        self.cycle_label = tk.Label(self.quiz_frame, text="", font=("Courier", 16, "bold"),
                                    bg="light blue", fg="black")
        self.cycle_label.pack()

        self.question_label = tk.Label(self.quiz_frame, text="", font=("Courier", 16, "bold"),
                                       bg="light blue", fg="black")
        self.question_label.pack(pady=(10, 5))

        self.prompt_label = tk.Label(self.quiz_frame, text="", font=("Courier", 16),
                                     bg="light blue", fg="black")
        self.prompt_label.pack()

        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(self.quiz_frame, textvariable=self.answer_var, width=40,
                                     bg="white", fg="black")
        self.answer_entry.pack(pady=5)
        self.answer_entry.bind("<Return>", lambda event: self.submit_answer())

        if self.mnemonic:
            self.mnemonic_label = tk.Label(self.quiz_frame, text="Mnemonic (optional):",
                                           font=("Courier", 16), bg="light blue", fg="black")
            self.mnemonic_label.pack()
            self.mnemonic_entry = tk.Entry(self.quiz_frame, width=40,
                                           bg="white", fg="black")
            self.mnemonic_entry.pack(pady=5)
            self.mnemonic_entry.bind("<Return>", lambda event: self.submit_answer())

        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Courier", 16),
                                       bg="light blue", fg="black")
        self.feedback_label.pack(pady=5)

        self.image_label = tk.Label(self.quiz_frame, bg="light blue")
        self.image_label.pack(pady=5)

        self.submit_button = tk.Button(self.quiz_frame, text="Submit", command=self.submit_answer,
                                       font=("Courier", 16), bg="light blue", fg="black")
        self.submit_button.pack(pady=10)

        self.update_cycle_label()
        self.show_question()

    def update_cycle_label(self):
        self.cycle_label.config(text=f"Cycle {self.current_cycle + 1} of {self.cycles}")

    def show_question(self):
        self.image_label.config(image="")
        self.feedback_label.config(text="")  # Clear feedback for next question
        self.answer_checked = False

        if self.current_question >= self.length:
            self.current_cycle += 1
            if self.current_cycle >= self.cycles:
                self.show_results()
                return
            else:
                self.current_question = 0
                self.update_cycle_label()

        question_num = self.current_question + 1
        self.question_label.config(text=f"Question {question_num}/{self.length}")

        if self.ordered:
            idx = self.current_question
        else:
            idx = random.randint(0, len(self.data) - 1)

        self.current_data_index = idx

        if self.target:
            question_text = f"What is '{self.data[idx][2]}' in {self.version}?"
        else:
            question_text = f"What is '{self.data[idx][1]}' in English?"

        self.prompt_label.config(text=question_text)
        self.answer_var.set("")
        self.answer_entry.focus()

        if self.mnemonic:
            self.mnemonic_entry.delete(0, tk.END)


    def submit_answer(self):
        if not self.answer_checked:
            user_answer = self.answer_var.get().strip().lower()
            idx = self.current_data_index

            if self.target:
                correct_answer = self.data[idx][1].lower()
            else:
                correct_answer = self.data[idx][2].lower()

            if user_answer == correct_answer:
                self.feedback_label.config(text="Correct!", fg="green")
                self.score += 1
                play_local_sound("audio-visual-library/correct.mp3")
                self.image_label.config(image=self.happy_img)
            else:
                responses = [
                    f"Incorrect, '{correct_answer}' is the correct answer...",
                    f"Incorrect, '{correct_answer}' is the right choice...",
                    f"Incorrect, '{correct_answer}' is correct—are you even trying...?"
                ]
                msg = random.choice(responses)
                self.feedback_label.config(text=msg, fg="red")
                if self.data[idx] not in self.review_words:
                    self.review_words.append(self.data[idx])
                play_local_sound("audio-visual-library/incorrect.mp3")
                self.image_label.config(image=self.sad_img)

            # Always use the chosen language word (assumed at index 1)
            word_for_audio = self.data[idx][1]
            open_audio(self.audio, self.audio_ai, word_for_audio, self.version)

            if self.mnemonic:
                new_mn = self.mnemonic_entry.get().strip()
                if new_mn:
                    overwrite_mnemonic(self.data[idx][1], new_mn)

            self.answer_checked = True

        else:
            self.current_question += 1
            self.show_question()

    def show_results(self):
        self.quiz_frame.destroy()
        self.results_frame = tk.Frame(self, bg="light blue")
        self.results_frame.pack(padx=20, pady=20)

        play_local_sound("audio-visual-library/ending.mp3")

        total_questions = self.length * self.cycles
        results_lines = [
            "Quiz Complete!",
            f"Total Questions: {total_questions}",
            f"Score: {self.score}/{total_questions}",
            "Review Words:"
        ]
        for row in self.review_words:
            results_lines.append(f"  {row[1]} : {row[2]}")

        results_label = tk.Label(self.results_frame, text="\n".join(results_lines),
                                  justify="left", font=("Courier", 16),
                                  bg="light blue", fg="black")
        results_label.pack()

        if self.save:
            with open(result_file, "a") as f:
                f.write("\nResults\n")
                f.write(f"\tLength of quiz: {total_questions}\n")
                f.write(f"\tScore: {self.score}/{total_questions}\n")
                f.write("\tReview words:\n")
                for row in self.review_words:
                    f.write(f"\t\t{row[1]} : {row[2]}\n")

            tk.Label(self.results_frame, text="(Results saved to results.txt)",
                     font=("Courier", 16), bg="light blue", fg="black")\
                .pack(pady=5)

        tk.Button(self.results_frame, text="Close", command=self.destroy,
                  font=("Courier", 16), bg="light blue", fg="black")\
            .pack(pady=10)

# --------------------------------------
# MAIN
# --------------------------------------
if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
