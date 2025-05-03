if __name__=="__main__":
    import os
    from signal import signal, SIGINT
    from typing import Callable as fn, NamedTuple

    def get_clear()->fn:
        if os.name == "nt":
            return lambda : os.system("cls")
        else:
            return lambda : os.system("clear")
    clear:fn = get_clear()

    def handle_SIGINT(signum, handler):
        clear()
        exit()
    signal(SIGINT, handle_SIGINT)

    class Perfil(NamedTuple):
        nombres: str
        apellidos: str
        matricula: str

    class ConfigLIC(NamedTuple):
        nombre: str
        matricula: str
        iniciales_ap: str
        iniciales_ap_inv: str

    titulo:str="Analizador de Cadenas | Presione Ctrl+C para salir"

    perfiles_base:list[Perfil] = [
        Perfil("Yozedh Jahday", "Guerrero Ceja", "0123456"),
        Perfil("Aldo Adrian", "Davila Gonzalez", "1994122"),
        Perfil("Luis Fernando", "Segobia Torres", "2177528"),
        Perfil("Roberto", "Sanchez Santoyo", "2177547")
    ]

    def registrar_perfil_custom() -> Perfil:
        clear()
        print(titulo)
        print("Ingrese los siguientes datos para generar el lenguaje:")
        nombres:str=input("Nombre(s)> ")
        apellidos:str=input("Apellidos> ")
        matricula:str=input("Matricula> ")
        while not matricula.isdecimal():
            print("Introduzca una matricula valida")
            matricula:str=input("Matricula> ")
        return Perfil(nombres, apellidos, matricula)
    
    def escoger_perfil(perfiles:list[Perfil]) -> Perfil:
        clear()
        print(titulo)
        print("Escoja un perfil o cree uno para crear el L.I.C")
        for i, perfil in enumerate(perfiles, start=1):
            print(f"{i}) {perfil.nombres} {perfil.apellidos} {perfil.matricula}")
        print(f"{len(perfiles)+1}) Crear Perfil")
        while True:
            try:
                opc:int = int(input("> "))
                if 1 <= opc <= len(perfiles)+1:
                    break
            except ValueError:
                pass
            print(f"Introduzca un valor entre 1 y {len(perfiles)+1}")
        if 1 <= opc <= len(perfiles):
            return perfiles[opc-1]
        else:
            return registrar_perfil_custom()

    def generar_configuracion(perfil:Perfil) -> ConfigLIC:
        nombre=perfil.nombres.split()[0]
        nombre=nombre.lower()
        iniciales_ap="".join([apellido[0] for apellido in perfil.apellidos.split()])
        iniciales_ap=iniciales_ap.lower()
        if not perfil.matricula.isdigit():
            raise ValueError("perfil.matricula debe ser un string numerico")
        return ConfigLIC(nombre, perfil.matricula, iniciales_ap, iniciales_ap[::-1])

    def es_cadena_valida(cadena:str, config:ConfigLIC) -> bool:
        if not cadena.startswith(config.matricula):
            return False
        cadena=cadena.removeprefix(config.matricula)

        n:int=0
        while cadena.startswith(config.iniciales_ap):
            cadena=cadena.removeprefix(config.iniciales_ap)
            n+=1
        if n==0:
            return False

        if not cadena.startswith(config.matricula):
            return False
        cadena=cadena.removeprefix(config.matricula)

        m:int=0
        while cadena.startswith(config.iniciales_ap_inv):
            cadena=cadena.removeprefix(config.iniciales_ap_inv)
            m+=1
        if not m==2*n:
            return False
        
        l:int=0
        while cadena.startswith(config.nombre):
            cadena=cadena.removeprefix(config.nombre)
            l+=1
        if not l==2 or cadena:
            return False
        
        return True

    perfil:Perfil = escoger_perfil(perfiles_base)
    config:ConfigLIC = generar_configuracion(perfil)
    lic:str = ("{ " + f"{config.matricula}({config.iniciales_ap})^n{config.matricula}"
            f"({config.iniciales_ap_inv})^2n{config.nombre}{config.nombre}" + " }")
    

    while True:
        clear()
        print("Analizador de Cadenas | Presione Ctrl+C para salir")
        print(f"LIC: {lic}")
        print("Introduzca una cadena para analizar")
        cadena:str = input("> ")
        print("Cadena Valida" if es_cadena_valida(cadena, config) else "Cadena Invalida")
        input("...")