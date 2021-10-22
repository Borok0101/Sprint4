var correo = document.getElementById('correo');
var nnombre = document.getElementById('nombre');
var contraseña = document.getElementById('contra');
var error = document.getElementById('Error');
error.style.color='blue';



function enviar(){
    
    var menErro=[];
    if(correo.value ===null || correo.value===''){
      
        menErro.push('Ingrese su correo');
    }
    if(nnombre.value ===null || nnombre.value===''){
      
        menErro.push('Ingrese su nombre de usuario');
    }
    if(contraseña.value ===null || contraseña.value===''){
        menErro.push('Ingrese su contraseña');
    }

   error.innerHTML= menErro.join(', ');


    return false;
    }
    
   