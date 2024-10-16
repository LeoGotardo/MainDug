
# MainDug
Este projeto é um **Gerenciador de Senhas** desenvolvido em Python utilizando a biblioteca `tkinter` para a interface gráfica. A aplicação permite que os usuários gerenciem suas senhas de forma segura, gerando, armazenando e controlando credenciais de login para diversos sites. O projeto utiliza **SQLite** como banco de dados local para armazenar as credenciais de maneira simples e eficaz.

O projeto é dividido em quatro módulos principais:
- `append.py`: Gerencia operações no banco de dados e criptografia.
- `controller.py`: Atua como controlador, gerenciando a lógica entre o modelo e a visualização.
- `model.py`: Contém os modelos de dados e operações como gerenciamento de usuários, armazenamento de senhas e criptografia.
- `view.py`: Gerencia os componentes de interface gráfica da aplicação.

## Tabela de Conteúdos
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
  - [Pré-requisitos](#pré-requisitos)
  - [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
- [Uso](#uso)
  - [Executando a Aplicação](#executando-a-aplicação)
  - [Autenticação de Usuário](#autenticação-de-usuário)
  - [Gerenciamento de Senhas](#gerenciamento-de-senhas)
  - [Geração de Senhas](#geração-de-senhas)
  - [Personalização](#personalização)
- [Descrição dos Arquivos](#descrição-dos-arquivos)
  - [`append.py`](#appendpy)
  - [`controller.py`](#controllerpy)
  - [`model.py`](#modelpy)
  - [`view.py`](#viewpy)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## Funcionalidades

- **Autenticação de Usuário**: Usuários podem se cadastrar, fazer login e armazenar suas credenciais.
- **Gerenciamento de Senhas**: Adicionar, deletar, atualizar e visualizar senhas salvas.
- **Geração de Senhas**: Gerador de senhas integrado com critérios personalizáveis (tamanho, símbolos, números, etc.).
- **Criptografia**: Senhas são armazenadas de forma segura utilizando criptografia AES fornecida pela biblioteca `cryptography`.
- **Suporte ao Clipboard**: Usuários podem copiar credenciais para a área de transferência para rápido acesso.
- **Personalização da Interface**: Modos claro e escuro, além de personalização de cores da interface.

## Instalação

### Pré-requisitos

- Python 3.x instalado em seu sistema.
- As seguintes bibliotecas Python são necessárias:
  - `cryptography`
  - `sqlite3`
  - `hashlib`
  - `pyperclip`
  - `tkinter`
  - `Pillow`
  - `customtkinter`
  - `CTkColorPicker`
  - `CTkTable`

  Você pode instalar as dependências com o seguinte comando:

  ```bash
  pip install -r requirements.txt
  ```

### Configuração do Banco de Dados

A aplicação utiliza **SQLite** como banco de dados local para armazenar as informações dos usuários e suas senhas. O banco de dados é automaticamente configurado na primeira vez que a aplicação é executada, não sendo necessário realizar configurações adicionais.

## Uso

### Executando a Aplicação

Para iniciar a aplicação, execute o arquivo `view.py`:

```bash
python view.py
```

### Autenticação de Usuário

- **Cadastro**: Novos usuários podem se cadastrar fornecendo um login único e uma senha.
- **Login**: Usuários existentes podem fazer login com suas credenciais.
- **Criptografia de Senhas**: As senhas dos usuários são criptografadas antes de serem armazenadas no banco de dados SQLite.

### Gerenciamento de Senhas

- **Adicionar Nova Senha**: Usuários podem adicionar um novo login de site, junto com o nome do site, nome de usuário e senha.
- **Editar Senha**: Usuários podem editar as credenciais armazenadas para qualquer site.
- **Excluir Senha**: Usuários podem excluir uma senha da lista.
- **Copiar para o Clipboard**: Copie rapidamente as credenciais para a área de transferência para uso fácil.

### Geração de Senhas

- Usuários podem gerar uma nova senha aleatória utilizando o gerador de senhas.
- Personalize o tamanho da senha e os caracteres incluídos (maiúsculas, minúsculas, números, símbolos).

### Personalização

- **Modo Claro/Escuro**: Alternar entre temas claro e escuro.
- **Seletor de Cores**: Usuários podem escolher uma cor personalizada para o tema da interface.

## Descrição dos Arquivos

### `append.py`

Este script gerencia as interações com o banco de dados SQLite, incluindo a adição de usuários e o armazenamento de senhas criptografadas. Utiliza a biblioteca `cryptography` para criptografar e descriptografar as senhas.

### `controller.py`

O controlador serve como intermediário entre o modelo e a visualização. Ele processa a entrada do usuário, interage com o modelo para operações de dados e atualiza a visualização conforme necessário.

### `model.py`

Contém a lógica para o gerenciamento de usuários e senhas, incluindo:
- Autenticação de usuários (login, cadastro).
- Armazenamento e recuperação de senhas.
- Criptografia e descriptografia de dados sensíveis.
- Gerenciamento de conexões e consultas ao banco de dados SQLite.

### `view.py`

Implementa a interface gráfica do usuário (GUI) usando `tkinter` e `customtkinter`. Permite que os usuários interajam com a aplicação, fornecendo funcionalidades como login, gerenciamento de senhas e mais.

## Contribuindo

1. Faça um fork do repositório.
2. Crie uma nova branch (`git checkout -b feature-branch`).
3. Faça suas alterações.
4. Commit suas mudanças (`git commit -m 'Add some feature'`).
5. Envie para a branch (`git push origin feature-branch`).
6. Abra um pull request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
