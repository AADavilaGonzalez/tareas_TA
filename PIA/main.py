DEFAULT_DPI:int = 96
scaling:float = 1.0

import tkinter as tk
from turing import Symbol
from gui import TkSlideTape, process_string_gui, tk_widget_get_config, tk_widget_set_config

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
    success_label_default = tk_widget_get_config(success_label)

    tape_gui = TkSlideTape(root, 9, default_char=Symbol._.value,
        width=300, height=150, background="white", default_speed=100, default_fps=30)
    
    prompt_label = tk.Label(root, text="Ingrese una\nCadena")
    input_field = tk.Entry(root)

    speed_scale = tk.Scale(root, from_=30, to=300, orient="horizontal",
        variable=tape_gui.speed, command=lambda val:tape_gui.speed.set(int(float(val))))
    speed_label = tk.Label(root, text="Velocidad de\nla Cinta")       
    ok_button = tk.Button(root, text="Validar", command=lambda:process_string_gui(
        input_field,tape_gui,success_label, success_label_default))

    language_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
    success_label.grid(row=0, column=3, columnspan=2, sticky="nsew")
    tape_gui.grid(row=1, column=0, columnspan=5, sticky="nsew")
    prompt_label.grid(row=2, column=0, sticky="nsew")
    input_field.grid(row=2, column=1, sticky="nsew")
    ok_button.grid(row=2, column=2, sticky="nsew")
    speed_label.grid(row=2, column=3, sticky="nsew")
    speed_scale.grid(row=2, column=4, sticky="nsew")

    tk.mainloop()

