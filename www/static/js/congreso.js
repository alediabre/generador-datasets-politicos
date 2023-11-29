import * as func from './funciones.js'

var indicesEliminados = []

document.addEventListener('DOMContentLoaded', function () {
    func.celdasExpansibles()
    agregarColumnas()
    botonOrdenarDocumentoyOrador()
    botonModificar()
    func.barraBusqueda(2, actualizarInfoCongreso)
    func.filtroPalabras(150, actualizarInfoCongreso)
    actualizarInfoCongreso()
})


function agregarColumnas() {
    const tabla = document.querySelector('#tabla_dinamica table')
    const filas = tabla.querySelectorAll('tbody tr')
    filas.forEach(fila => {
        /*Copiar la columna de texto al portapapeles*/
        const celdaPortapapeles = fila.insertCell()
        celdaPortapapeles.innerHTML = `<a href="#"><i class="fa-regular fa-copy"></i></a>`
        celdaPortapapeles.addEventListener('click', function() {
            func.copiarTextoDeColumna(fila,2)
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

function botonOrdenarDocumentoyOrador(){
    var col = 0
    const boton = document.querySelector('#boton_ordenar')
    boton.addEventListener('click', function(){
        col = (col + 1) % 2;
        if (col === 1){
            boton.innerHTML = `Ordenar por Orador <i class="fa-solid fa-user"></i>`
        }else{
            boton.innerHTML = `Ordenar por Documento <i class="fa-solid fa-file"></i>`
        }
        func.ordenarPorColumna(col)
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


function actualizarInfoCongreso(){
    const table = document.querySelector("#tabla_dinamica table")
    var tr = Object.values(table.getElementsByTagName("tr")).filter(function(r){return r.style.display != 'none'})
    tr.shift() /*Se omite el primer elemento porque es la cabecera de la tabla*/
    var numElem = tr.length
    var oradores = tr.map(function(r){return r.getElementsByTagName("td")[0].textContent})
    var numOrad = Array.from(new Set(oradores)).length
    var documentos = tr.map(function(r){return r.getElementsByTagName("td")[1].textContent})
    var numDoc = Array.from(new Set(documentos)).length
    
    const info = document.querySelectorAll(".info p span")
    info[0].textContent = numOrad
    info[1].textContent = numDoc
    info[2].textContent = numElem
}