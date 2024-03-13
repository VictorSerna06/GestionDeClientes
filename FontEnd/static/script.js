// Al cargar toda la página web se ejecuta la siguiente función
document.addEventListener('DOMContentLoaded', iniciar);

// Variable que contiene la URL 
const URL_API = 'http://localhost:3000/api/';

var clientes = [];

function iniciar(){
    buscar();
}

// Buarcar información de los clientes
async function buscar(){
    var url = URL_API + 'clientes';
    var res = await fetch(url,{
        "method": 'GET',
        "headers": {
            "Content-Type": 'application/json'
        }
    })

    clientes = await res.json();
    var html = '';
    for(cliente of clientes){
        var fila = 
        `<tr>
        <td>${cliente.Nombre}</td>
        <td>${cliente.Apellido}</td>
        <td>${cliente.Email}</td>
        <td>${cliente.Telefono}</td>
        <td>${cliente.Direccion}</td>
        <td>
            <button class="btnEditar" onclick="editar(${cliente.id})">Editar</button>
            <button class="btnEliminar" onclick="eliminar(${cliente.id})">Eliminar</button>
        </td>
        </tr>`
        html = html + fila;
    }
    document.querySelector('#clientes > tbody').outerHTML = html;
}

// Agregar un nuevo Cliente
function agregarCliente(){
    limpiarFormulario()
    abrirFormulario()
}

// Abrir el Formulario
function abrirFormulario(){
    document.getElementById('formulario').style.display = "block";
}

// Cerrar formulario
function cerrarFormulario(){
    document.getElementById('formulario').style.display = 'none';
}

// Guardar un nuevo cliente o modificar un cliente
async function guardar(){
    var datos = {
        "Nombre":document.getElementById('txtNombre').value.toUpperCase(),
        "Apellido":document.getElementById('txtApellido').value.toUpperCase(),
        "Email":document.getElementById('txtEmail').value,
        "Telefono":document.getElementById('txtTelefono').value,
        "Direccion":document.getElementById('txtDireccion').value.toUpperCase()
    }

    var id = document.getElementById('txtId').value;
    if(id != ''){
        datos.id = id
    }

    var url = URL_API + 'clientes'
    await fetch(url,{
        "method": 'POST',
        "body": JSON.stringify(datos),
        "headers": {
            "Content-Type": 'application/json'
        }
    })
    window.location.reload();
}

// Eliminar el registro de un cliente
async function eliminar(id){
    respuesta = confirm('¿Deseas eliminar el registro de este cliente?')
    if(respuesta == true){
        var url = URL_API + 'clientes/' + id
        await fetch(url,{
            "method": 'DELETE',
            "headers": {
                "Content-Type": 'application/json'
            }
        })
        window.location.reload();
    }
}

// Editar el registro de un cliente
function editar(id){
    abrirFormulario();
    var cliente = clientes.find(x => x.id == id)
    document.getElementById('txtId').value = cliente.id
    document.getElementById('txtNombre').value = cliente.Nombre
    document.getElementById('txtApellido').value = cliente.Apellido
    document.getElementById('txtEmail').value = cliente.Email
    document.getElementById('txtTelefono').value = cliente.Telefono
    document.getElementById('txtDireccion').value = cliente.Direccion
}

// Borrar los datos del formulario
function limpiarFormulario(){
    document.getElementById('txtId').value = ""
    document.getElementById('txtNombre').value = ""
    document.getElementById('txtApellido').value = ""
    document.getElementById('txtEmail').value = ""
    document.getElementById('txtTelefono').value = ""
    document.getElementById('txtDireccion').value = ""
}