import os
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button, Scrollbar, Text
from tkinterdnd2 import TkinterDnD, DND_FILES
from email import policy
from email.parser import BytesParser

from utils import save_window_position, load_window_position, register_to_redmine


# File to store the window position


def main():
    # Load the last window position
    last_x, last_y = load_window_position()

    # Use TkinterDnD.Tk instead of tk.Tk
    root = TkinterDnD.Tk()
    root.title("My GUI Application")
    root.geometry(f"400x50+{last_x}+{last_y}")  # Set the window size and position
    root.overrideredirect(True)  # Hide the window header

    # Set the window to always be on top
    root.wm_attributes("-topmost", True)


    # Temporarily disable overrideredirect and re-enable it
    # root.overrideredirect(False)
    # root.update_idletasks()  # Force the window manager to update
    # root.overrideredirect(True)

    # Enable dragging
    def start_move(event):
        root.x = event.x
        root.y = event.y

    def do_move(event):
        x = root.winfo_pointerx() - root.x
        y = root.winfo_pointery() - root.y
        root.geometry(f"+{x}+{y}")
        update_position_label(x, y)

    def end_move(event):
        # Save the window position when dragging ends
        x = root.winfo_x()
        y = root.winfo_y()
        save_window_position(x, y)

    root.bind("<Button-1>", start_move)
    root.bind("<B1-Motion>", do_move)
    root.bind("<ButtonRelease-1>", end_move)

    # Create a right-click menu
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="終了", command=root.destroy)

    def show_menu(event):
        menu.post(event.x_root, event.y_root)

    root.bind("<Button-3>", show_menu)  # Bind right-click to show the menu

    # Label to display the current position
    position_label = tk.Label(root, text="Position: (0, 0)")
    position_label.pack(pady=10)

    def update_position_label(x, y):
        position_label.config(text=f"Position: ({x}, {y})")

    # Label to display the dropped file type
    label = tk.Label(root, text="Drag and drop files here", wraplength=300)
    label.pack(pady=20)

    def show_eml_content(subject, body):
        """Custom dialog to display EML content."""
        dialog = Toplevel(root)
        dialog.title("EML File Content")
        dialog.geometry("1200x600")

        # ダイアログの幅を取得
        dialog.update_idletasks()  # ウィジェットのサイズを更新
        dialog_width = dialog.winfo_width()
        wrap_length = int(dialog_width * 0.9)  # ダイアログ幅の90%

        Label(dialog, text=f"Subject: {subject}", wraplength=wrap_length, anchor="w", justify="left").pack(pady=10, padx=10)

        # スクロールバー付きのテキストウィジェットを作成
        text_frame = tk.Frame(dialog)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = Text(text_frame, wrap="word", yscrollcommand=scrollbar.set, height=20)
        text_widget.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=text_widget.yview)

        # テキストウィジェットに本文を挿入
        text_widget.insert("1.0", body)
        # text_widget.config(state="disabled")  # 編集不可に設定

        # Add a button to register the content to Redmine
        def add_to_redmine():
            try:
                string_body = text_widget.get("1.0", "end-1c")  # Get the content from the text widget
                register_to_redmine(subject, string_body)
#                 # messagebox.showinfo("Success", "Content added to Redmine successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add to Redmine: {e}")

        Button(dialog, text="Add to Redmine", command=add_to_redmine).pack(pady=5)
        Button(dialog, text="Close", command=dialog.destroy).pack(pady=5)

        # Wait until the dialog is closed
        dialog.transient(root)  # Make the dialog appear above the main window
        dialog.grab_set()       # Prevent interaction with the main window
        root.wait_window(dialog)  # Wait until the dialog is closed

    def on_drop(event):
        # Get the dropped file paths and remove surrounding braces
        file_paths = event.data.strip().strip("{}").split("} {")
        for file_path in file_paths:
            # Extract the file extension
            file_extension = os.path.splitext(file_path)[1]
            # Update the label with the file type
            label.config(text=f"Dropped file type: {file_extension}")

            # If the file is an eml file, parse and display its content
            if file_extension.lower() == ".eml":
                try:
                    with open(file_path, "rb") as f:
                        msg = BytesParser(policy=policy.default).parse(f)
                    subject = msg["subject"] or "No Subject"
                    body = msg.get_body(preferencelist=("plain")).get_content() if msg.get_body() else "No Content"
                    
                    # 非同期的にダイアログを表示
                    root.after(100, lambda: show_eml_content(subject, body))

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to read EML file: {e}")
        
        # メイン画面にフォーカスを戻す
        root.focus_force()

    # Enable the root window to accept file drops
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    root.mainloop()


if __name__ == "__main__":
    main()