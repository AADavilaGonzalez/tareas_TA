import tkinter as tk
from collections import deque
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class TkTapeCell:
    box_id:int
    char_id:int

class TkSlideTape(tk.Canvas):

    def __init__(self, parent:tk.Widget, visible_cells:int=9,
            cell_border_width:int=5, cell_border_color:str="black",
            default_char:str="?", speed:float=200,fps:float=60,
            font:tuple[str,int,str]=("Arial", 16, "bold"),
            **kwargs) -> None:
        super().__init__(parent, **kwargs)
        if visible_cells < 1:
            raise ValueError("TkSlideTape.visible_cells must be equal to or greater than 1")
        if visible_cells%2==0:
            raise ValueError("TkSlideTape.visible_cells must be an odd number")
        self.visible_cells = visible_cells
        self.cell_border_width = cell_border_width
        self.cell_border_color = cell_border_color
        self.font = font
        self.default_char = default_char[0]

        self.speed = speed if speed >= 1 else 100 #px/frame
        self.fps = fps if fps >= 1 else 60 #fps

        self.cell_length:float = None
        self.cells:deque[TkTapeCell] = None
    
    def pack(self, **kwargs) -> None:
        super().pack(**kwargs)
        self._draw_initial_state()

    def grid(self, **kwargs) -> None:
        super().grid(**kwargs)
        self._draw_initial_state()

    def palace(self, **kwargs) -> None:
        super().place(**kwargs)
        self._draw_initial_state()

    def _draw_initial_state(self) -> None:
        self.update_idletasks()
        self.cells = deque()
        width = self.winfo_width()
        height = self.winfo_height()
        self.cell_length = width/self.visible_cells
        half_length = self.cell_length/2

        self.create_rectangle(
            (width-half_length)//2, (height-half_length)//2-self.cell_length,
            (width+half_length)//2, (height+half_length)//2-self.cell_length,
            fill="red")

        xoffset = width//2 - self.cell_length*(self.visible_cells//2+1)
        yoffset = height//2
        for _ in range(self.visible_cells+2):
            box:int = self.create_rectangle(
                (xoffset-half_length), (yoffset+half_length),
                (xoffset+half_length), (yoffset-half_length),
                width=self.cell_border_width, outline=self.cell_border_color
            )
            char:int = self.create_text(xoffset, yoffset, text=self.default_char, font=self.font)
            self.cells.append(TkTapeCell(box,char))
            xoffset+=self.cell_length

    def move_right(self, next_char:str, on_complete:Callable=None) -> None:
        width = self.winfo_width()
        self.move(self.cells[0].box_id, width+self.cell_length, 0)
        self.move(self.cells[0].char_id, width+self.cell_length, 0)

        self.itemconfig(self.cells[-1].char_id, text=next_char)
        self.cells.rotate(-1)

        animated_cells = list(self.cells)[:-1]
        framecount = round(self.fps*(self.cell_length/self.speed))
        pixels_per_frame = self.cell_length/framecount

        def slide_cells_right():
            nonlocal animated_cells, framecount, pixels_per_frame
            if framecount > 0:
                for cell in animated_cells:
                    self.move(cell.box_id, -pixels_per_frame, 0)
                    self.move(cell.char_id, -pixels_per_frame, 0)
                framecount-=1
                self.after(int((1/self.fps)*1000), slide_cells_right)
            else:
                if(on_complete):
                    on_complete()
        slide_cells_right()

    def move_left(self, next_char:str, on_complete:Callable=None) -> None:
        width = self.winfo_width()
        self.move(self.cells[-1].box_id, -width-self.cell_length, 0)
        self.move(self.cells[-1].char_id, -width-self.cell_length, 0)

        self.itemconfig(self.cells[0].char_id, text=next_char)
        self.cells.rotate(1)
        
        animated_cells = list(self.cells)[1:]
        framecount = round(self.fps*(self.cell_length/self.speed))
        pixels_per_frame = self.cell_length/framecount

        def slide_cells_left():
            nonlocal animated_cells, framecount, pixels_per_frame
            if framecount > 0:
                for cell in animated_cells:
                    self.move(cell.box_id, pixels_per_frame, 0)
                    self.move(cell.char_id, pixels_per_frame, 0)
                framecount-=1
                self.after(int((1/self.fps)*1000), slide_cells_left)
            else:
                if(on_complete):
                    on_complete()
        slide_cells_left()