import tkinter

ordered_result = False
save_result = False
target_result = False
length_result = 5
searcher_result = False
audior_result = False
audio_air_result = False
mnemonicr_result = False
cycles_result = 1
keyword_result = ""

def clear_screen():
    """Remove all widgets from the main window."""
    for widget in root.winfo_children():
        widget.destroy()

def submit_initial_state():
    global ordered_result
    global save_result
    global target_result
    global length_result
    global searcher_result
    global audio_result
    global audio_ai_result
    global mnemonic_result
    global cycles_result
    global keyword_result

    ordered_result = ordered.get()
    save_result = save.get()
    target_result = target.get()
    searcher_result = searcher.get()
    audio_result = audio.get()
    audio_ai_result = audio.get()
    mnemonic_result = mnemonic.get()
    cycles_result= cycles.get()
    keyword_result= mnemonic_string.get()

    clear_screen()


root = tkinter.Tk()
root.title("Indonesian Learning Application")
root.configure(bg="lightblue")

width, height = 900, 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width - width) / 2)
y = int((screen_height - height) / 2)
root.geometry(f"{width}x{height}+{x}+{y}")

#Placing the widgets

frame_checkboxes1 = tkinter.Frame(root)
frame_checkboxes1.pack(pady=10, padx=10)

ordered = tkinter.BooleanVar(value=False)
ordered_checkbox = tkinter.Checkbutton(frame_checkboxes1, text="Ordered", variable=ordered)
ordered_checkbox.pack(padx=20, pady=10, side='left')

save = tkinter.BooleanVar(value=False)
save_checkbox = tkinter.Checkbutton(frame_checkboxes1, text="Save results", variable=save)
save_checkbox.pack(padx=20, pady=10, side='left')

target = tkinter.BooleanVar(value=False)
target_checkbox = tkinter.Checkbutton(frame_checkboxes1, text="Answer with target language", variable=target)
target_checkbox.pack(padx=20, pady=10, side='left')

searcher = tkinter.BooleanVar(value=False)
searcher_checkbox = tkinter.Checkbutton(frame_checkboxes1, text="Search for a word", variable=searcher)
searcher_checkbox.pack(padx=20, pady=10, side='left')

frame_checkboxes2 = tkinter.Frame(root)
frame_checkboxes2.pack(pady=10, padx=10)

audio = tkinter.BooleanVar(value=False)
audio_checkbox = tkinter.Checkbutton(frame_checkboxes2, text="Find audio in natural language", variable=audio)
audio_checkbox.pack(padx=20, pady=10, side='left')

audio_ai = tkinter.BooleanVar(value=False)
audio_ai_checkbox = tkinter.Checkbutton(frame_checkboxes2, text="Find artificial audio (higher chance of existence)", variable=audio_ai)
audio_ai_checkbox.pack(padx=20, pady=10,side='left')

mnemonic = tkinter.BooleanVar(value=False)
mnemonic_checkbox = tkinter.Checkbutton(frame_checkboxes2, text="Mnemonic", variable=mnemonic,)
mnemonic_checkbox.pack(padx=20, pady=10, side='left')

frame_cycles = tkinter.Frame(root)
frame_cycles.pack(pady=10, padx=10)

cycles_label = tkinter.Label(frame_cycles, text='Number of Cycles:')
cycles_label.pack(side='left')
cycles = tkinter.Entry(frame_cycles)
cycles.pack(side='left')

frame_mnemonic_string = tkinter.Frame(root)
frame_mnemonic_string.pack(pady=10, padx=10)

mnemonic_string_label = tkinter.Label(frame_mnemonic_string, text='Mnemonic:')
mnemonic_string_label.pack(side='left')
mnemonic_string = tkinter.Entry(frame_mnemonic_string)
mnemonic_string.pack(side='left')

begin_button = tkinter.Button(text="Begin", font=("Ariel", 25), command=submit_initial_state)
begin_button.pack()

root.mainloop()
