DEFAULT_DPI:int = 96
scaling:float = 1.0

import tkinter as tk
from turing import Symbol, State, Move, TuringOutput, TuringInput, delta
from gui import TkSlideTape, TkTapeCell

if __name__=="__main__":
    
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=5)
    root.rowconfigure(2, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)
    root.columnconfigure(4, weight=1)

    language_label = tk.Label(root, text=r"L={a^(n)b^(n+m) | n y m >=0}", font=("Arial", 24, "bold"))
    success_label = tk.Label(root, text="Analizador\nde Cadenas")
    prompt_label = tk.Label(root, text="Ingrese una\nCadena")
    input_field = tk.Entry(root)
    speed_scale = tk.Scale(root, from_=30, to=300, orient="horizontal")

    tape_gui = TkSlideTape(root, 9, default_char=Symbol._.value,
        width=300, height=150, background="white", speed=50, fps=30)

    def process_string_gui(slide_tape:TkSlideTape, entry:tk.Entry):
        string:str = Symbol._.value + entry.get() + Symbol._.value
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
            if state==State.qf:
                success_label.config(text="Cadena Valida")
                return 
            output:TuringOutput = delta(TuringInput(state, Symbol(turing_tape[pos])))
            if not output or pos not in range(len(turing_tape)):
                success_label.config(text="Cadena Invalida")
                return
            middle_cell:TkTapeCell = slide_tape.cells[(slide_tape.visible_cells+2)//2]
            slide_tape.itemconfig(middle_cell.char_id, text=output.s.value)
            turing_tape[pos]=output.s.value
            pos+=output.m
            if output.m==Move.R:
                edge_pos=pos+slide_tape.visible_cells//2
                next_char = turing_tape[edge_pos] if edge_pos in range(pos) else slide_tape.default_char
                slide_tape.move_right(next_char, lambda:slide_tape.after(500,lambda:turing_step(output.q, pos)))
            elif output.m==Move.L:
                edge_pos=pos-slide_tape.visible_cells//2
                next_char = turing_tape[edge_pos] if edge_pos in range(pos) else slide_tape.default_char
                slide_tape.move_left(next_char, lambda:slide_tape.after(500, lambda:turing_step(output.q, pos)))
            else:
                slide_tape.after(500, turing_step(output.q, pos))
        turing_step(State.qi, 0)        


    def reset_to_default():
        pass

    ok_button = tk.Button(root, text="Validar", command=lambda:process_string_gui(tape_gui, input_field))
    cancel_button = tk.Button(root, text="Cancelar", command=reset_to_default)

    language_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
    success_label.grid(row=0, column=3, columnspan=2, sticky="nsew")
    tape_gui.grid(row=1, column=0, columnspan=5, sticky="nsew")
    prompt_label.grid(row=2, column=0, sticky="nsew")
    input_field.grid(row=2, column=1, sticky="nsew")
    ok_button.grid(row=2, column=2, sticky="nsew")
    cancel_button.grid(row=2, column=3, sticky="nsew")
    speed_scale.grid(row=2, column=4, sticky="nsew")

    tk.mainloop()

