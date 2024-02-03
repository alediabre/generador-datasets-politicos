import asyncio

from utils.input_handler import options_handler
from editor.dataset_editor import inicio_visualizacion
from congreso.congreso import inicio_congreso
from twitter.twitter import inicio_twitter



async def inicio():

    modo = await options_handler(list("TtCcEe"),"Seleccione una opción:\nrecuperar datos de Twitter [T]\nrecuperar datos del Congreso [C]\neditar el dataset [E]\n",list("Tt"),list("Cc"),list("Ee"))
    
    if modo == 0:
        await inicio_twitter()
    elif modo == 1:
        await inicio_congreso()
    else:
        await inicio_visualizacion()
    


if __name__ == "__main__":
    asyncio.run(inicio())