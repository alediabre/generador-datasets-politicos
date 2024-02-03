import * as func from './funciones.js'

var indicesEliminados = []

document.addEventListener('DOMContentLoaded', function () {
    func.celdasExpansibles()
    agregarColumnas()
    botonModificar()
    func.barraBusqueda(actualizarInfo)
    func.filtroPalabras(150, actualizarInfo)
    actualizarInfo()
    switch (window.contexto) {
        case 'congreso':
            botonOrdenarDocumentoyOrador('Orador','Documento')
        case 'twitter':
            botonOrdenarAutor()
    }
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

function botonOrdenarDocumentoyOrador(opcion1,opcion2){
    var col = 0
    const boton = document.querySelector('#boton_ordenar')
    boton.addEventListener('click', function(){
        col = (col + 1) % 2;
        if (col === 1){
            boton.innerHTML = `Ordenar por ${opcion1} <i class="fa-solid fa-user"></i>`
        }else{
            boton.innerHTML = `Ordenar por ${opcion2} <i class="fa-solid fa-file"></i>`
        }
        func.ordenarPorColumna(col)
    }) 
}

function botonOrdenarAutor(){
    const boton = document.querySelector('#boton_ordenar')
    boton.addEventListener('click', function(){
        func.ordenarPorColumna(0)
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


function actualizarInfo(){
    const table = document.querySelector("#tabla_dinamica table")
    var tr = Object.values(table.getElementsByTagName("tr")).filter(function(r){return r.style.display != 'none'})
    tr.shift() /*Se omite el primer elemento porque es la cabecera de la tabla*/
    var numElem = tr.length
    var col1 = tr.map(function(r){return r.getElementsByTagName("td")[0].textContent})
    var distinct_col1 = Array.from(new Set(col1)).length
    var col2 = tr.map(function(r){return r.getElementsByTagName("td")[1].textContent})
    var distinct_col2 = Array.from(new Set(col2)).length
    
    const info = document.querySelectorAll(".info p span")
    info[0].textContent = numElem
    info[1].textContent = distinct_col1
    if (info[2]){
        info[2].textContent = distinct_col2
    }
}