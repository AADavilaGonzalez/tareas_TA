from enum import Enum, IntEnum
from typing import NamedTuple

class State(Enum):
    qi = "qi"
    q1 = "q1"
    q2 = "q2"
    q3 = "q3"
    q4 = "q4"
    q5 = "q5"
    qf = "qf"

class Symbol(Enum):
    a = "a"
    b = "b"
    _ = "_" 

class Move(IntEnum):
    L = -1
    S = 0
    R = 1

    def reverse(self):
        return -self

class TuringInput(NamedTuple):
    q:State
    s:Symbol

class TuringOutput(NamedTuple):
    q:State
    s:Symbol
    m:Move


def seek_blank(input:TuringInput, direction:Move,
    q_next:State ,allowed:list[Symbol]):
    
    if input.s == Symbol._:
        return TuringOutput(q_next, Symbol._, direction.reverse())
    elif input.s in allowed:
        return TuringOutput(input.q, input.s, direction)
    return None


def delta(input:TuringInput)->TuringOutput:
    match input:

        case TuringInput(State.qi, Symbol._):
            return TuringOutput(State.q1, Symbol._, Move.R)
        
        case TuringInput(State.q1, x):
            match x:
                case Symbol._:
                    return TuringOutput(State.qf, Symbol._, Move.S)
                case Symbol.a:
                    return TuringOutput(State.q2, Symbol._, Move.R)
                case Symbol.b:
                    return TuringOutput(State.q5, Symbol._, Move.R)

        case TuringInput(State.q2, x):
            return seek_blank(input, Move.R, State.q3, [Symbol.a, Symbol.b])

        case TuringInput(State.q3, Symbol.b):
            return TuringOutput(State.q4, Symbol._, Move.L)

        case TuringInput(State.q4, x):
            return seek_blank(input, Move.L, State.q1, [Symbol.a, Symbol.b])

        case TuringInput(State.q5, x):
            match x:
                case Symbol.b:
                    return TuringOutput(State.q5, Symbol._, Move.R)
                case Symbol._:
                    return TuringOutput(State.qf, Symbol._, Move.S)
                
    return None

def process_string(string:str) -> bool:
    pos:int = 0
    tape:list[str] = list(string)
    state:State = State.qi
    while state!=State.qf:
        try:
            output:TuringOutput = delta(TuringInput(state, Symbol(tape[pos])))
            tape[pos]=output.s.value
            pos+=output.m
            state=output.q
        except(ValueError,AttributeError,IndexError):
            return False
    return True

import tkinter as tk

class TkTuringMachine(tk.Frame):
    
    def __init__(self, parent, slots=5,**kwargs):
        super().__init__(parent, **kwargs)

        for()
