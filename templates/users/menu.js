
//Seleciona os itens clicando
var menuItem = document.querySelectorAll('.menu-item')

function selectLink(){
    menuItem.forEach((item)=>
        item.classList.remove('ativo')
    )
    this.classList.add('ativo')
     
}

menuItem.forEach((item)=>
    item.addEventListener('click', selectLink)
)

//Expandir o menu

var expandbutton = document.querySelector('#expand-button')
var sidebar = document.querySelector('.sidebar')

expandbutton.addEventListener('click', function(){
    sidebar.classList.toggle('expandir')
})
