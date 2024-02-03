
function celdasExpansibles(){
    const celdasExpansibles = document.querySelectorAll('#tabla_dinamica td')
    celdasExpansibles.forEach(celda => {
        celda.addEventListener('click', function () {
            this.classList.toggle('expanded')
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



function buscarTexto(columna, funcionActualizarDatos) {
    var input, table, tr, td, i, txtValue;
    input = document.getElementById("buscadorTexto").value
    table = document.querySelector("#tabla_dinamica table")
    tr = table.getElementsByTagName("tr")
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[columna]
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
    funcionActualizarDatos()
}

function barraBusqueda(funcionActualizarDatos){
    const barra = document.querySelector('#buscadorTexto')
    const columna = barra.dataset.columna
    barra.addEventListener('keyup', function(){
        buscarTexto(columna,funcionActualizarDatos)
    })
}


function wordCount(str) {
    return str.split(' ')
           .filter(function(n) { return n != '' })
           .length
}

function filtroPalabras(max, funcionActualizarDatos){
    const slider = document.getElementById("rangoPalabras")
    const output = document.getElementById("numPalabras")
    const columna = slider.dataset.columna
    output.innerHTML = slider.value;

    slider.oninput = function() {
        var input = parseInt(this.value)
        const table = document.querySelector("#tabla_dinamica table")
        const tr = table.getElementsByTagName("tr")
        if (input === max){
            output.innerHTML = "Sin filtro"
            for (i = 1; i < tr.length; i++) {
                tr[i].style.display = ''
            }
        }else{
            output.innerHTML = input
            for (var i = 1; i < tr.length; i++) {
                const td = tr[i].getElementsByTagName("td")[columna]
                var textValue = td.textContent || td.innerText
                if (wordCount(textValue) > input){
                    tr[i].style.display = 'none'
                }else{
                    tr[i].style.display = ''
                }
            }
        }
        funcionActualizarDatos()
    }
}


export {celdasExpansibles, copiarTextoDeColumna, ordenarPorColumna, barraBusqueda, filtroPalabras}