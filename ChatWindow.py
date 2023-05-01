import tkinter as tk
import textwrap
from WrappedListBox import WrappedListBox
from utils import generate_message
import threading


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
        self.input_box.focus_set()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)




    def _create_message_list(self):
        self.message_list_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.message_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 0))

        self.message_list = tk.Text(self.message_list_frame, wrap="word", state="disabled", width=80, height=20)
        self.message_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.message_list.tag_configure("bold", font=("Helvetica", 10, "bold"))
        self.message_list.tag_configure("italic", font=("Helvetica", 10, "italic"))



        self.scrollbar = tk.Scrollbar(self.message_list_frame, command=self.message_list.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_list.config(yscrollcommand=self.scrollbar.set)



    def _create_input_frame(self):
        self.input_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.input_frame.pack(fill=tk.X, padx=20, pady=(10, 20))

        self.input_box = tk.Text(self.input_frame, wrap="word", width=50, height=4)
        self.input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))

        self.input_box.bind("<Return>", self.handle_enter_key)  
        self.input_box.bind("<Shift-Return>", self.handle_shift_enter_key)  


        
    # Add these two new methods to handle the keypress events
    def handle_enter_key(self, event):
        self.send_message()
        return "break"  # Prevents the default behavior (new line) and stops other bindings from being triggered

    def handle_shift_enter_key(self, event):
        self.input_box.insert(tk.INSERT, "\n")
        return "break"  # Prevents the default behavior (new line) and stops other bindings from being triggered





    def send_message(self):
        message = self.input_box.get("1.0", tk.END).strip()
        self.input_box.delete("1.0", tk.END)

        if message:
            self.update_message_list("You: " + message)

            response_thread = threading.Thread(target=self.generate_response, args=(message,))
            response_thread.start()




    def generate_response(self, message):
        response_generator = generate_message(message)

        # Add "AI: " prefix only once
        first_chunk = next(response_generator)
        self.root.after_idle(self.update_message_list, "AI: " + first_chunk)

        # Append the rest of the chunks without the "AI: " prefix and without a newline
        for partial_response in response_generator:
            self.root.after_idle(lambda: self.update_message_list(partial_response, newline=False))


    def update_message_list(self, message, newline=True):
        tag = None
        if "AI:" in message:
            tag = "normal"
        elif "You:" in message:
            tag = "bold"

        self.message_list.configure(state="normal")
        if newline:
            self.message_list.insert(tk.END, message + "\n", tag)
        else:
            self.message_list.insert(tk.END, message, tag)
        self.message_list.configure(state="disabled")
        self.message_list.see(tk.END)



    def on_close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
