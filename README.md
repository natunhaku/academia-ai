# Academia AI 🏋️🤖

## Sobre o projeto

O **Academia AI** é um agente inteligente criado para auxiliar usuários na criação de treinos e na consulta de informações presentes em documentos de treinamento.

O agente utiliza Inteligência Artificial para conversar com o usuário em linguagem natural, entender seus objetivos e fornecer orientações relacionadas a exercícios físicos.

Além disso, o usuário pode enviar documentos em **PDF** contendo informações sobre seus treinos. O Academia AI processa esses documentos e utiliza uma base vetorial para consultar as informações antes de responder perguntas específicas sobre o treino enviado.

Este projeto foi desenvolvido como parte do **Challenge Agente de IA – Tech Builder ONE**, da Alura em parceria com a Oracle.

---

## Funcionalidades

* Conversação em linguagem natural.
* Criação de sugestões de treino.
* Consulta de documentos enviados pelo usuário.
* Upload de arquivos PDF.
* Extração de texto dos documentos.
* Geração de embeddings.
* Busca semântica utilizando Vector Store.
* Memória de conversa.
* Respostas utilizando Google Gemini.
* Orientações sobre execução de exercícios.

---

## Arquitetura
### Workflow no n8n

A arquitetura do agente foi construída no n8n, integrando o Google Gemini, memória de conversa, embeddings e busca vetorial para consulta aos documentos enviados pelo usuário.

![Workflow do Academia AI no n8n](screenshots/workflow-n8n.png)

---
O fluxo principal do projeto funciona da seguinte forma:

```text
Usuário
   ↓
Chat Trigger
   ↓
Verificação de arquivo
   ↓
AI Agent
   ↓
Google Gemini
   ↓
Memória da conversa
   ↓
Vector Store
   ↓
Resposta ao usuário
```

Quando um documento é enviado:

```text
PDF
 ↓
Extração do texto
 ↓
Preparação dos dados
 ↓
Embeddings Gemini
 ↓
Vector Store
 ↓
Consulta pelo AI Agent
```

---

## Tecnologias utilizadas

* n8n
* Google Gemini
* Inteligência Artificial Generativa
* Embeddings
* Vector Store
* RAG (Retrieval-Augmented Generation)
* Git
* GitHub
* Visual Studio Code

---

## Estrutura do projeto

```text
academia-ia/
│
├── docs/
│
├── n8n/
│   └── academia-ai.json
│
├── screenshots/
│
├── .env.example
├── .gitignore
└── README.md
```

---

## Como executar

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Abra o n8n

Utilize uma instalação local ou uma instância do n8n.

### 3. Importe o workflow

No n8n:

1. Acesse a área de workflows.
2. Escolha a opção de importar workflow.
3. Selecione:

```text
n8n/academia-ai.json
```

### 4. Configure o Google Gemini

Crie sua própria credencial da API do Google Gemini dentro do n8n.

As chaves de API não são armazenadas neste repositório.

### 5. Execute o workflow

Após configurar as credenciais, execute o workflow e utilize o chat do agente.

---

## Exemplos de perguntas

O usuário pode perguntar:

```text
Crie um treino de peito e bíceps para mim.
```

```text
Como executar corretamente o supino com halteres?
```

```text
Quantas séries de agachamento existem no meu treino?
```

```text
Quais exercícios para costas aparecem no documento que enviei?
```

Quando uma pergunta estiver relacionada ao documento enviado, o agente consulta a base vetorial antes de produzir a resposta.

---

## Segurança

As credenciais utilizadas para acessar serviços externos não são armazenadas diretamente no código do projeto.

Cada usuário que importar o workflow deverá configurar suas próprias credenciais no n8n.

---

## Autor

**Natanael Barbosa de Sousa**

Projeto desenvolvido para o Challenge Agente de IA do programa **Tech Builder ONE – Alura + Oracle**.
