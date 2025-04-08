import tkinter as tk
from tkinter import font, colorchooser, filedialog
from datetime import datetime

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Notepad")
        self.root.geometry("800x600")
        self.current_font = font.Font(family="Arial", size=12)
        self.setup_ui()
        
    def setup_ui(self):
        # Toolbar
        toolbar = tk.Frame(self.root, bg="#f0f0f0", padx=5, pady=5)
        toolbar.pack(fill=tk.X)
        
        # Formatting buttons
        self.bold_btn = tk.Button(toolbar, text="B", command=self.toggle_bold)
        self.bold_btn.pack(side=tk.LEFT, padx=2)
        
        self.italic_btn = tk.Button(toolbar, text="I", command=self.toggle_italic)
        self.italic_btn.pack(side=tk.LEFT, padx=2)
        
        # Font size
        self.font_size = tk.StringVar()
        size_menu = tk.OptionMenu(toolbar, self.font_size, "12", "14", "16", "18", "20", command=self.change_font_size)
        size_menu.pack(side=tk.LEFT, padx=2)
        self.font_size.set("12")
        
        # Color picker
        self.color_btn = tk.Button(toolbar, text="🎨", command=self.choose_color)
        self.color_btn.pack(side=tk.LEFT, padx=2)
        
        # Action buttons
        self.copy_btn = tk.Button(toolbar, text="📋 Copy", command=self.copy_text)
        self.copy_btn.pack(side=tk.LEFT, padx=2)
        
        self.paste_btn = tk.Button(toolbar, text="📄 Paste", command=self.paste_text)
        self.paste_btn.pack(side=tk.LEFT, padx=2)
        
        self.save_btn = tk.Button(toolbar, text="💾 Save", command=self.save_file)
        self.save_btn.pack(side=tk.LEFT, padx=2)
        
        # Text editor
        self.text_area = tk.Text(
            self.root,
            wrap=tk.WORD,
            font=self.current_font,
            padx=10,
            pady=10,
            selectbackground="#a6d2ff"
        )
        self.text_area.pack(expand=True, fill=tk.BOTH)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Keyboard shortcuts
        self.root.bind("<Control-b>", lambda e: self.toggle_bold())
        self.root.bind("<Control-i>", lambda e: self.toggle_italic())
        
    def toggle_bold(self):
        new_weight = "bold" if self.current_font.cget("weight") == "normal" else "normal"
        self.current_font.configure(weight=new_weight)
        self.update_text_format()
        
    def toggle_italic(self):
        new_slant = "italic" if self.current_font.cget("slant") == "roman" else "roman"
        self.current_font.configure(slant=new_slant)
        self.update_text_format()
        
    def change_font_size(self, size):
        self.current_font.configure(size=int(size))
        self.update_text_format()
        
    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_font.configure(foreground=color)
            self.update_text_format()
            
    def update_text_format(self):
        self.text_area.configure(font=self.current_font)
        self.status_bar.config(text=f"Font: {self.current_font.actual()}")
        
    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_area.selection_get())
        self.status_bar.config(text="Text copied to clipboard")
        
    def paste_text(self):
        try:
            self.text_area.insert(tk.INSERT, self.root.clipboard_get())
        except tk.TclError:
            self.status_bar.config(text="Clipboard is empty")
            
    def save_file(self):
        content = self.text_area.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialfile=f"note_{datetime.now().strftime('%Y-%m-%d')}"
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            self.status_bar.config(text=f"File saved: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()