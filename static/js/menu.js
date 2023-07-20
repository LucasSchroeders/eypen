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

var expandButton = document.querySelector('#expand-btn')
var menuSide = document.querySelector('.sidebar')

expandButton.addEventListener('click', function(){
    menuSide.classList.toggle('expandir')
})
