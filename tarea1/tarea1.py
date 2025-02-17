if __name__=="__main__":
    import os
    import re
    from signal import signal, SIGINT
    from typing import Callable as fn, NamedTuple
    
    def handleSIGINT(signum, handler)->None:
        clear()
        exit()
    signal(SIGINT, handleSIGINT)
    
    def getClear()->fn:
        if os.name == "nt":
            return lambda : os.system("cls")
        else:
            return lambda : os.system("clear")
    clear:fn = getClear()
    
    class Perfil(NamedTuple):
        nombre:str
        matricula:str
    perfiles:tuple[Perfil] = (Perfil("Aldo Adrian Davila Gonzalez", "1994122"),
                              Perfil("Luis Fernando Segobia Torres", "2177528"),
                              Perfil("Roberto Sanchez Santoyo", "2177547"))
    
    titulo:str = "Programa de Validacion de Cadenas | introduzca Ctrl+C para salir"

    clear()
    print(titulo)
    print("Seleccione un perfil para generar el lenguaje regular:")
    for i, perfil in enumerate(perfiles):
        print(f"{i+1}) Nombre:{perfil.nombre}, Matricula:{perfil.matricula}")
    print(f"{len(perfiles)+1}) Perfil Custom")

    while(True):
        try:
            opc = int(input("> "))
            if(opc >= 1 and opc <= len(perfiles)+1):
                break
            else:
                print("Elija una opcion valida")
        except ValueError:
            print("Elija una opcion valida")
    
    if(opc==len(perfiles)+1):
        while(True):
            nom = input("Nombre: ")
            if(all(c.isalpha() for c in nom)):
                break
            else:
                print("No se permiten caracteres no alfabeticos")
        while(True):
            mat = input("Matricula: ")
            if(all(d.isdigit() for d in mat)):
                break
            else:
                print("Solo se permiten caracteres numericos")
        perfil = Perfil(nom, mat)
    else:
        perfil = perfiles[opc-1]

    iniciales:str = ''.join([c.lower() for c in re.findall(r"\b[A-Za-z]", perfil.nombre)])
    c:str = ''.join(sorted(list({c.lower() for c in perfil.nombre if c.isalpha()})))
    d:str = ''.join(sorted(list({d for d in perfil.matricula if d.isdigit})))
    a:str = c + d
    alfabeto:str = "{" + ", ".join(c+d) + ", ." + "}"
    c = "[" + c + "]"
    d = "[" + d + "]"
    a = "[" + a + "]"

    patron:str = f"{d}(\.?{a}+)*\.?{iniciales}(\.?{a}+)*.{perfil.matricula}"
    regex:re.Pattern = re.compile(patron)

    while True:
        clear()
        print(titulo)
        print(f"Lenguaje Regular: {patron}")
        print(f"Alfabeto: {alfabeto}")
        entrada:str = input("Cadena: ")
        salida:str = None
        if(regex.fullmatch(entrada)):
            salida = "Si"
        else:
            salida = "No"
        print(f"Es cadena Valida?: {salida}")
        input()

        