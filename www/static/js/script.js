var indicesEliminados = []

document.addEventListener('DOMContentLoaded', function () {
    celdasExpansibles()
    agregarColumnas()
    botonOrdenar()
    botonModificar()
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
        /*Copiar la columna de texto al portapapeles*/
        const celdaPortapapeles = fila.insertCell()
        celdaPortapapeles.innerHTML = `<a href="#"><i class="fa-regular fa-copy"></i></a>`
        celdaPortapapeles.addEventListener('click', function() {
            copiarTextoDeColumna(fila,2)
        })
        /*Eliminar la fila y almacenar indice eliminado en indicesEliminados*/
        const celdaEliminar = fila.insertCell()
        celdaEliminar.innerHTML = `<a href="#"><i class="fa-regular fa-trash-can"></i></a>`
        celdaEliminar.addEventListener('click', function(){
            const index = parseInt(fila.childNodes[1].textContent)
            const numEliminados = indicesEliminados.push(index)
            document.querySelector('#boton_modificar span').textContent = numEliminados
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
        fetch('/deleteRows', {
             method: 'POST',
             headers: {'Content-Type': 'application/json'},
             body: JSON.stringify({ 'filas': indicesEliminados }), })
            .then(response => response.json())
            .then(data => {
                alert(data.message)
                indicesEliminados = []
                document.querySelector('#boton_modificar span').textContent = 0
            })
            .catch(error => {
                console.error('Error del servidor:', error)
            })
    })
}

function buscarTexto() {
    var input, table, tr, td, i, txtValue;
    input = document.getElementById("buscadorTexto").value
    table = document.querySelector("#tabla_dinamica table")
    tr = table.getElementsByTagName("tr")
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[2]
        if (td) {
            txtValue = td.textContent || td.innerText
            var index = txtValue.indexOf(input)
            if (index > -1) {
                // Fragmento coincidente
                var before = txtValue.substring(0, index)
                var match = txtValue.substring(index, index + input.length)
                var after = txtValue.substring(index + input.length)
                td.innerHTML = before + "<span class='resaltado'>" + match + "</span>" + after
                tr[i].style.display = ""
            } else {
                // No hay coincidencia
                td.innerHTML = txtValue
                tr[i].style.display = "none"
            }
        }       
    }
}

