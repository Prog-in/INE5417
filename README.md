# INE5417

Este é o projeto implementado na disciplina INE5417 - Engenharia de Software I. Trata-se de um jogo de tabuleiro
chamado Qyshinsu.


## Execução do jogo

Para se executar o jogo, deve-se seguir os passos descritos nas seguintes seções. 

### Opcional: criação de um ambiente virtual

Recomenda-se a criação de um ambiente virtual para a instalação das dependências necessárias ao funcionamento do jogo.
Os passos para a sua criação estão descritos abaixo.

<ol>
    <li>Na raiz do projeto, execute o comando `python3 -m venv .venv`</li>
    <li>Ative o ambiente virtual por meio do comando `source .venv/bin/activate`</li>
</ol>

### Execução do programa

Para executar o programa, deve-se primeiro instalar as dependências necessárias por meio do comando

```bash
pip install -r requirements.txt
```

Após isso, deve-se gerar um id do jogo rodando o seguinte código:

```bash
python3 src/INE5417/config/generate_game_id.py
```

Por fim, para iniciar o programa, deve-se utilizar o comando

```bash
python3 src/main.py
```

### Observações

A depender do sistema operacional, o executável do Python pode ter nomes diferentes. Caso o comando `python3` não seja
reconhecido, recomenda-se tentar com `python`. Se ainda não for possível, verifique se o Python está instalado e
consulte a documentação do mesmo para identificar o nome do executável.
