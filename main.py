import tkinter as tk
from tkinter import font as tkfont
import threading
from macros import macro_search
# Create main window
def create_app():
    root = tk.Tk()
    root.title("Among Us Glitched Codes Generator")

    width, height = 600, 230
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="#151515")

    default_font = tkfont.Font(family="Georgia", size=10)

    desc_text = (
        "1. Go to Settings -> Graphics.\n"
        "2. Turn off fullscreen and set the resolution to 1600x900.\n"
        "3. Paste glitched codes below, separated by spaces.\n"
        "4. Go to the title screen and push Play -> Online (if you haven't already).\n"
        "5. Press Run and wait!\n"
        "6. Once the program stops, you can set the resolution back to normal."
    )
    desc_label = tk.Label(root, text=desc_text, font=default_font, fg="#ffffff", bg="#151515", justify="left")
    desc_label.pack(padx=20, pady=(20,10), anchor="w")

    entry_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=entry_var, font=default_font, bg="#151515", fg="#ffffff", width=50)
    entry.pack(padx=20, pady=(0,10))

    def on_run():
        raw = entry_var.get().strip()
        codes = raw.split()
        t = threading.Thread(target=macro_search, args=(codes,), daemon=True)
        t.start()

    run_btn = tk.Button(root, text="Run", command=on_run, font=default_font, bg="#151515", fg="#ffffff")
    run_btn.pack(pady=(0,20))

    return root

if __name__ == "__main__":
    app = create_app()
    app.mainloop()