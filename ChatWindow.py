import tkinter as tk
import textwrap
from WrappedListBox import WrappedListBox
from utils import generate_message



class ChatWindow:
    def __init__(self):
        self._create_ui()

    def _create_ui(self):
        self.root = tk.Tk()
        self.root.title("Chat with OpenAI")
        self.root.geometry("800x600")
        self.root.configure(bg="#F0F0F0")

        self._create_message_list()
        self._create_input_frame()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _create_message_list(self):
        self.message_list_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.message_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 0))

        self.message_list = WrappedListBox(self.message_list_frame, width=80, height=20)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.message_list_frame, command=self.message_list.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    def _create_input_frame(self):
        self.input_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.input_frame.pack(fill=tk.X, padx=20, pady=(10, 20))

        self.input_box = tk.Text(self.input_frame, wrap="word", width=50, height=4)
        self.input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

        self.input_box.bind("<Return>", self.handle_enter_key)  # Add this line
        self.input_box.bind("<Shift-Return>", self.handle_shift_enter_key)  # Add this line

        
    # Add these two new methods to handle the keypress events
    def handle_enter_key(self, event):
        self.send_message()
        return "break"  # Prevents the default behavior (new line)

    def handle_shift_enter_key(self, event):
        self.input_box.insert(tk.INSERT, "\n")
        return "break"  # Prevents the default behavior (new line)

    def send_message(self):
        message = self.input_box.get("1.0", tk.END).strip()
        self.input_box.delete("1.0", tk.END)

        if message:
            self.message_list.insert(len(self.message_list.item_data), "You: " + message)
            self.message_list.see(len(self.message_list.item_data) - 1)

            response = generate_message(message)
            wrapped_response = '\n'.join(textwrap.wrap(response, 75))

            self.message_list.insert(len(self.message_list.item_data), "AI: " + wrapped_response)
            self.message_list.see(len(self.message_list.item_data) - 1)

    def on_close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
