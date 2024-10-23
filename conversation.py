from __future__ import annotations

from dataclasses import dataclass

from .shared import *

class Conversation:
    @dataclass
    class Cell:
        parent: Conversation
        item: ConversationItem
        prev: ItemID | None
        next_: ItemID | None
    
        def nextCell(self):
            if self.next_ is None:
                raise StopIteration
            return self.parent.cells[self.next_]
    
    def __init__(self):
        self.cells: tp.Dict[ItemID, Conversation.Cell] = {}
        self.root: ItemID | None = None
    
    def insertAfter(
        self, item: ConversationItem, 
        previous_item_id: ItemID | None, 
    ):
        if previous_item_id is None:
            assert self.root is None
            self.root = item.id_
            self.cells[item.id_] = self.Cell(
                self, item, None, None,
            )
            return
        prevCell = self.cells[previous_item_id]
        next_id = prevCell.next_
        cell = self.Cell(self, item, previous_item_id, next_id)
        self.cells[item.id_] = cell
        prevCell.next_ = item.id_
        if next_id is not None:
            self.cells[next_id].prev = item.id_
    
    def __iter__(self):
        item_id = self.root
        while item_id is not None:
            cell = self.cells[item_id]
            yield cell.item
            item_id = cell.next_
