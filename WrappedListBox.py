import tkinter as tk
from typing import Any, List, Dict

# WrappedListBox class definition
#
# A class that inherits from tkinter.Canvas, providing a listbox with wrapped text.


class WrappedListBox(tk.Canvas):

    # Constructor for the WrappedListBox class.
    #
    # @param master The parent widget.
    # @param args Additional arguments.
    # @param kwargs Additional keyword arguments.
    def __init__(self, master: tk.Widget, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)

        self.item_data: List[Dict[str, Any]] = []
        self.text_tags = {}  # Store the text tags and their configurations

        self.bind("<Configure>", self._on_configure)

    # Event handler for WrappedListBox resize.
    #
    # Updates the width of text items when the WrappedListBox is resized.
    # @param event The event information.
    def _on_configure(self, event: tk.Event) -> None:
        """
        Update the width of text items when the WrappedListBox is resized.
        """
        width = event.width
        for index, data in enumerate(self.item_data):
            item_id = self.item_data[index]["id"]
            text = self.item_data[index]["text"]
            self.itemconfig(item_id, text=text, width=width)

    # Inserts a new text item into the WrappedListBox.
    #
    # @param index The position at which the text should be inserted.
    # @param text The text to be inserted.
    # @param tags A list of tags to apply to the text.
    # @param args Additional arguments.
    # @param kwargs Additional keyword arguments.
    def insert(self, index: int, text: str, tags: List[str] = [], *args: Any, **kwargs: Any) -> None:
        item_id = self.create_text(
            0, 0, anchor="nw", text=text, tags=("wrap",))
        index = int(index) if index != tk.END else len(self.item_data)
        self.item_data.insert(index, {"id": item_id, "text": text})
        self._apply_tags(item_id, tags)
        self._reposition_items()

    # Apply the specified tags to the given item ID.
    #
    # @param item_id The ID of the text item to apply the tags to.
    # @param tags The list of tags to apply.
    def _apply_tags(self, item_id: int, tags: List[str]) -> None:
        """
        Apply the specified tags to the given item ID.
        """
        for tag in tags:
            if tag in self.text_tags:
                self.itemconfig(item_id, **self.text_tags[tag])

    # Reposition all text items to maintain the correct order.
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

    # Scrolls the WrappedListBox to make the specified item visible.
    #
    # @param index The index of the item to make visible.
    def see(self, index: int) -> None:
        if index == tk.END:
            index = len(self.item_data) - 1
        bbox = self.bbox(self.item_data[index]["id"])
        self.yview_moveto(bbox[1] / self.bbox("all")[3])

    # Configures the tag options for text items.
    #
    # @param tag The tag name to configure.
    # @param args Additional arguments.
    # @param kwargs Additional keyword arguments containing the options for the tag.
    def tag_configure(self, tag: str, *args: Any, **kwargs: Any) -> None:
        self.text_tags[tag] = kwargs
