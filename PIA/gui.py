import tkinter as tk
from collections import deque
from dataclasses import dataclass
from typing import Callable, Any

from turing import TuringInput, TuringOutput, Symbol, State, Move, delta

GLOBAL_FONT="Arial"

def tk_widget_get_config(widget:tk.Widget) -> dict[str,str]:
    return {k:widget.cget(k) for k in widget.keys()}

def tk_widget_set_config(widget:tk.Widget, config:dict[str,str]):
    widget.configure(**config)

@dataclass
class TkTapeCell:
    box_id:int
    char_id:int

class TkSlideTape(tk.Canvas):

    def __init__(self, parent:tk.Widget, visible_cells:int=9,
            cell_border_width:int=5, cell_border_color:str="black",
            default_char:str="?", default_speed:int=200, default_fps:int=60,
            font:tuple[str,int,str]=(GLOBAL_FONT, 16, "bold"),
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

        self.speed = tk.IntVar() #px/frame
        if(default_speed > 0):
            self.speed.set(default_speed)
        else:
            self.speed.set(200)

        self.fps = tk.IntVar() #fps
        if(default_fps > 0):
            self.fps.set(default_fps)
        else:
            self.speed.set(60)

        self.cell_length:float = None
        self.cells:deque[TkTapeCell] = None
        
        self.state_label = tk.Label(
            self,
            text="qi",  # Estado inicial
            font=(GLOBAL_FONT, 14, "bold"),
            bg="red",
            fg="white",
            width=6,             
            anchor="center")

    
    def update_state_display(self, state: State) -> None:
        self.state_label.config(text=state.name)
        if state == State.qf:
            self.state_label.config(bg="green")
        else:
            self.state_label.config(bg="red")


    
    def pack(self, **kwargs) -> None:
        super().pack(**kwargs)
        self.after(100, self._draw_initial_state)

    def grid(self, **kwargs) -> None:
        super().grid(**kwargs)
        self.after(100, self._draw_initial_state)

    def palace(self, **kwargs) -> None:
        super().place(**kwargs)
        self.after(100, self._draw_initial_state)

    def _draw_initial_state(self) -> None:
        self.update_idletasks()
        self.cells = deque()
        width = self.winfo_width()
        height = self.winfo_height()
        self.cell_length = width/self.visible_cells
        half_length = self.cell_length/2

        self.state_label.place(x=(width - self.state_label.winfo_reqwidth()) // 2, y=10)

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
        fps = self.fps.get()
        framecount = round(fps*(self.cell_length/self.speed.get()))
        pixels_per_frame = self.cell_length/framecount

        def slide_cells_right():
            nonlocal animated_cells, fps, framecount, pixels_per_frame
            if framecount > 0:
                for cell in animated_cells:
                    self.move(cell.box_id, -pixels_per_frame, 0)
                    self.move(cell.char_id, -pixels_per_frame, 0)
                framecount-=1
                self.after(int((1/fps)*1000), slide_cells_right)
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
        fps = self.fps.get()
        framecount = round(fps*(self.cell_length/self.speed.get()))
        pixels_per_frame = self.cell_length/framecount

        def slide_cells_left():
            nonlocal animated_cells, fps, framecount, pixels_per_frame
            if framecount > 0:
                for cell in animated_cells:
                    self.move(cell.box_id, pixels_per_frame, 0)
                    self.move(cell.char_id, pixels_per_frame, 0)
                framecount-=1
                self.after(int((1/fps)*1000), slide_cells_left)
            else:
                if(on_complete):
                    on_complete()
        slide_cells_left()


def process_string_gui(input_entry:tk.Entry, slide_tape:TkSlideTape, success_label:tk.Label,
    success_label_default:dict[str,str]):
        invalid_chars = [c for c in input_entry.get() if c not in [s.value for s in Symbol]]
        if invalid_chars:
            success_label.config(text=f"Caracteres inválidos: {', '.join(invalid_chars)}")
            return

        tk_widget_set_config(success_label, success_label_default)

        WAIT_TIME = 333
        string:str = Symbol._.value + input_entry.get() + Symbol._.value
        turing_tape:list[str] = list(string)

        it = iter(slide_tape.cells)
        for _ in range((slide_tape.visible_cells+2)//2):
            slide_tape.itemconfig(next(it).char_id, text=slide_tape.default_char)
        for i in range(len(turing_tape)):
            try:
                slide_tape.itemconfig(next(it).char_id, text=turing_tape[i])
            except(StopIteration):
                break
        while True:
            try:
                slide_tape.itemconfig(next(it).char_id, text=slide_tape.default_char)
            except(StopIteration):
                break

        def turing_step(state:State, pos:int) -> None:
            nonlocal slide_tape
            nonlocal turing_tape
            if state == State.qf:
                slide_tape.update_state_display(state)
                success_label.config(text="Cadena Válida", bg="green", fg="white")
                return
            output:TuringOutput = delta(TuringInput(state, Symbol(turing_tape[pos])))
            if not output or pos not in range(len(turing_tape)):
                success_label.config(text="Cadena Inválida", bg="red", fg="white")
                return
            slide_tape.update_state_display(state)
            middle_cell:TkTapeCell = slide_tape.cells[(slide_tape.visible_cells+2)//2]
            slide_tape.itemconfig(middle_cell.char_id, text=output.s.value)
            turing_tape[pos]=output.s.value
            pos+=output.m
            if output.m==Move.R:
                edge_pos=pos+slide_tape.visible_cells//2
                next_char = turing_tape[edge_pos] if edge_pos in range(pos) else slide_tape.default_char
                try:
                    slide_tape.move_right(next_char, lambda:slide_tape.after(
                        WAIT_TIME,lambda:turing_step(output.q, pos)))
                except(tk.TclError):
                    return
            elif output.m==Move.L:
                edge_pos=pos-slide_tape.visible_cells//2
                next_char = turing_tape[edge_pos] if edge_pos in range(pos) else slide_tape.default_char
                try:
                    slide_tape.move_left(next_char, lambda:slide_tape.after(
                        WAIT_TIME, lambda:turing_step(output.q, pos)))
                except(tk.TclError):
                    return
            else:
                slide_tape.after(WAIT_TIME, turing_step(output.q, pos))
        turing_step(State.qi, 0)
            