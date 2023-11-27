document.addEventListener('DOMContentLoaded', function () {
    celdasExpansibles()
    agregarColumnas()
    botonOrdenar()
    botonModificar()
    botonSalir()
})


function celdasExpansibles(){
    const celdasExpansibles = document.querySelectorAll('#tabla_dinamica td')
    celdasExpansibles.forEach(celda => {
        celda.addEventListener('click', function () {
            this.classList.toggle('expanded')
        })
    })
}


function agregarColumnas() {
    const tabla = document.querySelector('#tabla_dinamica table')
    const filas = tabla.querySelectorAll('tbody tr')
    filas.forEach(fila => {
        const celdaPortapapeles = fila.insertCell()
        celdaPortapapeles.innerHTML = `<a href="#"><i class="fa-regular fa-copy"></i></a>`
        celdaPortapapeles.addEventListener('click', function() {
            copiarTextoDeColumna(fila,2)
        })
        const celdaEliminar = fila.insertCell()
        celdaEliminar.innerHTML = `<a href="#"><i class="fa-regular fa-trash-can"></i></a>`
        celdaEliminar.addEventListener('click', function(){
            const index = fila.childNodes[1].textContent
            fila.remove()
        })
    })
}


function copiarTextoDeColumna(fila, columnaIndex) {
    const textoACopiar = fila.querySelectorAll('td')[columnaIndex].textContent
    navigator.clipboard.writeText(textoACopiar)
}


function ordenarPorColumna(index) {
    var table, rows, switching, i, x, y, shouldSwitch
    table = document.querySelector("#tabla_dinamica table")
    switching = true
    while (switching) {
      switching = false
      rows = table.rows
      for (i = 1; i < (rows.length - 1); i++) {
        shouldSwitch = false
        x = rows[i].getElementsByTagName("TD")[index]
        y = rows[i + 1].getElementsByTagName("TD")[index]
        // Comprueba si las dos filas intercambian lugares
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch = true
          break
        }
      }
      if (shouldSwitch) {
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i])
        switching = true
      }
    }
}


function botonOrdenar(){
    var col = 0
    const boton = document.querySelector('#boton_ordenar')
    boton.addEventListener('click', function(){
        col = (col + 1) % 2;
        if (col === 1){
            boton.innerHTML = `Ordenar por Orador <i class="fa-solid fa-user"></i>`
        }else{
            boton.innerHTML = `Ordenar por Documento <i class="fa-solid fa-file"></i>`
        }
        ordenarPorColumna(col)
    }) 
}

function botonModificar(){
    document.getElementById('boton_modificar').addEventListener('click', function() {
        fetch('/deleteRows', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error('Error al detener el servidor:', error);
            });
    })
}

function botonSalir(){
    document.getElementById('boton_salir').addEventListener('click', function() {
        fetch('/stopServer', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error('Error al detener el servidor:', error);
            });
    })
}
