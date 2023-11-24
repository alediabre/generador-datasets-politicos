import asyncio

from utils.input_handler import options_handler
from utils.data_visualization import inicio_visualizacion
from congreso.congreso import inicio_congreso



async def inicio():

    modo = await options_handler(list("TtCcVv"),"Seleccione una opción:\nrecuperar datos de Twitter [T]\nrecuperar datos del Congreso [C]\nvisualizar los datos [V]\n",list("Tt"),list("Cc"),list("Vv"))
    
    if modo == 0:
        pass
    elif modo == 1:
        await inicio_congreso()
    else:
        await inicio_visualizacion()
    


if __name__ == "__main__":
    asyncio.run(inicio())