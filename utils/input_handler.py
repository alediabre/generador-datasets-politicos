from utils.colores_consola import bcolors

async def options_handler(options,question,*args):
    '''
    Manejador de opciones que se le proporcionan al usuario.
    Recibe la lista de opciones posibles a elegir (options).
    Recibe la pregunta a mostrar en pantalla para el usuario (question).
    Recibe una serie de argumentos sin nombre que determinarán lo que devuelve la función según lo que el usuario responda.
    Si el usuario responde con algo contenid en el "arg 0", devuelve 0
    '''
    answer = ""
    while answer not in options:
        answer = input(f"{bcolors.BOLD}{question}{bcolors.ENDC}")
    for i,arg in enumerate(args):
        if answer in arg:
            return i
        

async def list_options_handler(options,question,extra=None,verbose=True):
    '''
    Manejador de opciones que se le proporcionan al usuario, recibe una lista de opciones.
    Imprime en pantalla todas las opciones posibles con su índice.
    Devuelve el índice introducido por el usuario.
    Si extra se añade como parámetro, se habilita una nueva opción aparte de la lista options, que será la opción 0
    Si se pasa como parámetro verbose=False, no se muestran las opciones en pantalla
    '''
    if extra != None:
        print(f'{bcolors.BOLD}{bcolors.OKBLUE}0 {extra}{bcolors.ENDC}')
        inicio = 0
    else: inicio = 1

    if verbose == True:
        for i,option in enumerate(options):
            print(f'{bcolors.BOLD}{bcolors.OKCYAN}{i+1} {option}{bcolors.ENDC}')
        print("")
        
    answer = -1
    while answer not in range(inicio,len(options)+1):
        answer = input(f"{bcolors.BOLD}{question}{bcolors.ENDC}")
        answer = int(answer) if answer.isnumeric() else -1 #Evita errores al introducer cadenas no numericas
    return answer