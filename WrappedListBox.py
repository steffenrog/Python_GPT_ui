import tkinter as tk
from typing import Any, List, Dict


class WrappedListBox(tk.Canvas):
    def __init__(self, master: tk.Widget, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self.item_data: List[Dict[str, Any]] = []
        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event: tk.Event) -> None:
        """
        Update the width of text items when the WrappedListBox is resized.
        """
        width = event.width
        for index, data in enumerate(self.item_data):
            item_id = self.item_data[index]["id"]
            text = self.item_data[index]["text"]
            self.itemconfig(item_id, text=text, width=width)

    def insert(self, index: int, text: str, *args: Any, **kwargs: Any) -> None:
        """
        Insert a new text item at the specified index.
        """
        item_id = self.create_text(0, 0, anchor="nw", text=text, tags=("wrap",))
        self.item_data.insert(int(index), {"id": item_id, "text": text})
        self._reposition_items()

    def _reposition_items(self) -> None:
        """
        Reposition all text items to maintain the correct order.
        """
        y = 0
        for data in self.item_data:
            item_id = data["id"]
            bbox = self.bbox(item_id)
            height = bbox[3] - bbox[1]
            self.coords(item_id, 0, y)
            self.tag_raise(item_id)
            y += height

        self.configure(scrollregion=self.bbox("all"))

    def see(self, index: int) -> None:
        """
        Scroll the WrappedListBox to make the specified item visible.
        """
        bbox = self.bbox(self.item_data[index]["id"])
        self.yview_moveto(bbox[1] / self.bbox("all")[3])
