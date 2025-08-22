const { useContext } = require("react");

function excluirUsuario(id,cpf) {
      if(!confirm(`Tem certeza que deseja excluir o usuario ${cpf}`)){
    
       return
    }
    
   fetch(`/usuario/${id}`,{
      method: 'DELETE'
    })
  .then(response => {
      return response.json().then(data=>{
        if(!response.ok){
          throw new Error(data.erro ||"Erro desconhecido")
        }
       
        return data;
      })
    })
  
    .then(data => {
      alert(data.message);
      const linha=document.getElementById('linha-'+id)
      if (linha)linha.remove();
    })
    .catch(error => {
      console.error("Erro na requisição",error)
      alert("Errro ao excluir usuario"+error.message)

    })
}

function editarUsuario(id,nome,cpf,email,idade) {

const linha = document.getElementById(`linha-${id}`); 
const tdElements = linha.querySelectorAll('td');
  
document.getElementById(`nome-${id}`)=nome.setAttribute("contenteditable", "true"); 
document.getElementById(`cpf-${id}`)=cpf.setAttribute("contenteditable", "true"); 
document.getElementById(`email-${id}`)=email.setAttribute("contenteditable", "true"); 
document.getElementById(`idade-${id}`)=idade.setAttribute("contenteditable", "true"); 

  

   [nome, cpf, email, idade].addEventListener("blur",  function (event) {
        event.preventDefault();
      
            const nome = nomeEl.textContent;
            const cpf = cpfEl.textContent;
            const email = emailEl.textContent;
            const idade = idadeEl.textContent;
  
      fetch(`/usuario/${id}`, {
        method: 'PUT',
        headers: {
           'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id,
            nome,
            cpf,
            email,
            idade
        }),
    })
     
    })
  })

  .then(response => {
      return response.json().then(data=>{
        if(!response.ok){
          throw new Error(data.erro ||"Erro desconhecido")
        }
       
        return data;
      })
    })
  
    .then(data => {
     console.log('atualizado')

  
    })
    .catch(error => {
      console.error("Erro na requisição",error)
      alert("Errro ao atualizar"+error.message)

    })
    


}