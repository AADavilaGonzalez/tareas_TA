import tkinter as tk
from typing import Self

class AppManager:
    DEFAULT_DPI:int = 96
    _instance:Self = None
    _initialized:bool = False

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if self._initialized:
            return
        root = tk.Tk()
        self.scaling = root.winfo_fpixels("1i")/self.DEFAULT_DPI