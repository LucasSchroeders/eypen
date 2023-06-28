Esse arquivo é direcionado para os desenvolvedores.

Esse projeto será desenvolvido em python, então entende-se que já está com o mesmo instalado.

Para aqueles que estão começando no projeto, siga os passos a seguir para configurar o projeto:
1. Rodar o comando `python -m venv venv` para criar um ambiente virtual:
2. Rodar o comando `pip install -r requirements.txt` para baixar todas as libs que são necessárias no projeto:
    

Para manter o projeto organizado segue algumas instuções do que fazemos nesse projeto:
1. Sempre que for fazer alguma funcionalidade nova, criar uma nova branch a partir da develop com o seguinte comando:
    - `git checkout -b feature/[nome da branch]`
2. Após finalizar a funcionalidade, abrir um PR para ser avaliado o que foi feito e, caso esteja tudo ok, mesclar na develop.
    
Segue alguns comandos básicos de git para quem não estiver familiarizado:
- Para adicionar todos os arquivos alterados/excluídos/adicionados ao commit, utilizar o comando `git add .`. Caso queria adicionar apenas um dentre os disponíveis, utilizar `git add [nome do arquivo]`
- Para criar o commit, utilizar o comando `git commit -m "[titulo do commit]"`. Há também outras variações do commit, mas esse já será o suficiente para esse projeto.
- Para subir o commit no repositório remoto, usar o comando `git push origin/[nome da branch]`
- Para atualizar o repositório local com as atualizações do repositório remoto, utilizar o comando `git pull origin/[nome da branch]`
- Para trocar de branch no repositório local, usar o comando `git checkout [nome da branch]`
- Para criar uma branch nova, a partir da branch que esteja, usar o comando `git branch [nome da branch]`
- Para criar uma branch nova, a partir da branch que esteja, e já trocar de branch, usar o comando `git checkout -b [nome da branch]`
    
