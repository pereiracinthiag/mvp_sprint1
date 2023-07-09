/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/medidores';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.medidores.forEach(item => insertList(item.tag, item.descricao, item.instalacao))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()


/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputProduct, inputQuantity, inputPrice) => {
  const formData = new FormData();
  formData.append('tag', inputProduct);
  formData.append('descricao', inputQuantity);
  formData.append('codigo_instalacao', inputPrice);
  console.log(formData)
  let url = 'http://127.0.0.1:5000/medidor';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}


/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/medidor?tag=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = () => {
  let inputProduct = document.getElementById("newInput").value;
  let inputQuantity = document.getElementById("newQuantity").value;
  let inputPrice = document.getElementById("newPrice").value;

  if (inputProduct === '') {
    alert("Escreva a tag do nome medidor!");
  } else if (isNaN(inputPrice)) {
    alert("Instalação é um código numérico!");
  } else {
    insertList(inputProduct, inputQuantity, inputPrice)
    postItem(inputProduct, inputQuantity, inputPrice)
    alert("Medidor adicionado!")
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (nameProduct, quantity, price) => {
  var item = [nameProduct, quantity, price]
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1))
  document.getElementById("newInput").value = "";
  document.getElementById("newQuantity").value = "";
  document.getElementById("newPrice").value = "";

  removeElement()
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir certificados do medidor clicado
  --------------------------------------------------------------------------------------
*/
const insertCertificados = (id_certificado) => {
  var item = [id_certificado]
  var lista = document.getElementById('mycerts');

  for (var i = 0; i < item.length/2; i++) {
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(id_certificado))
    lista.appendChild(li)
  }

}

/* --------------------------------------------------------------------------------------
Função para buscar a lista de certificados de um medidor específico 
--------------------------------------------------------------------------------------
*/

const getCertificados = (item) => {
  let url = 'http://127.0.0.1:5000/medidor?tag=' + item;
  fetch(url, {
    method: 'get'
  })
    .then((response) => response.json())
    .then(result => { 
      
      console.log(result.certificados)
      result.certificados.forEach(item => insertCertificados(item.id_certificado))
    
    });

}



/* --------------------------------------------------------------------------------------
Função para "escutar" click em um item da tabela e apresentar os certificados correspondentes
--------------------------------------------------------------------------------------
*/

let btn = document.querySelector("#myTable")

btn.addEventListener("click", () => {

  var node = document.getElementById("mycerts")
  node.innerHTML = ''

  var tag
  var td = event.target;
  while (td !== this && !td.matches("tr")) {
      td = td.parentNode;
  }
  if (td === this) {
      console.log("No table cell found");
  } else {
    tag = td.children[0].textContent
    console.log(tag)
  }




  getCertificados(tag);
  

})

