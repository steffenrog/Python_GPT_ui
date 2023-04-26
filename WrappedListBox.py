import tkinter as tk



class WrappedListBox(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.item_data = []
        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        width = event.width
        for index, data in enumerate(self.item_data):
            item_id = self.item_data[index]["id"]
            text = self.item_data[index]["text"]
            self.itemconfig(item_id, text=text, width=width)

    def insert(self, index, text, *args, **kwargs):
        item_id = self.create_text(0, 0, anchor="nw", text=text, tags=("wrap",))
        self.item_data.insert(int(index), {"id": item_id, "text": text})
        self._reposition_items()


    def _reposition_items(self):
        y = 0
        for data in self.item_data:
            item_id = data["id"]
            bbox = self.bbox(item_id)
            height = bbox[3] - bbox[1]
            self.coords(item_id, 0, y)
            self.tag_raise(item_id)
            y += height

        self.configure(scrollregion=self.bbox("all"))

    def see(self, index):
        bbox = self.bbox(self.item_data[index]["id"])
        self.yview_moveto(bbox[1] / self.bbox("all")[3])
