<h1 align="center">
  <br>
  ⌚ Bulova Collection Manager
  <br>
</h1>

<h4 align="center">Uma plataforma full-stack sofisticada para gestão de catálogo e vitrine de relógios de luxo.</h4>

<p align="center">
  <a href="#-sobre">Sobre</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-tecnologias">Tecnologias</a> •
  <a href="#-estrutura-de-dados">Database</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Back--End-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Tailwind_CSS-Front--End-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
</p>

---

## 📖 Sobre

O **Bulova Collection Manager** é uma aplicação web desenvolvida para oferecer uma experiência visual imersiva na exibição de relógios, combinada com um sistema de gerenciamento robusto. O projeto se destaca pelo uso de **Tailwind CSS** para criar interfaces modernas com efeitos de vidro (glassmorphism), gradientes e animações 3D, enquanto o backend em **Flask** garante o processamento eficiente de dados e uploads.

A aplicação foi desenhada pensando tanto na experiência do cliente final (Vitrine) quanto na do administrador (Dashboard de Gestão).

---

## ✨ Funcionalidades

### 🎨 Interface & Experiência (Frontend)

* **Carrossel 3D Imersivo:** A página inicial apresenta um carrossel giratório desenvolvido com CSS puro (`perspective` e `transform-style: preserve-3d`), criando uma vitrine interativa única.
* **Design Responsivo & Moderno:** Layout fluido construído com Tailwind CSS, utilizando fontes personalizadas (*Montserrat Alternates*) e uma paleta de cores premium (Laranja/Cinza/Branco).
* **Visualização Detalhada:** Modais interativos (pop-ups) para exibir especificações técnicas dos produtos (Material, Preço, Descrição) sem necessidade de recarregar a página.
* **Upload de Imagens com Preview:** Interface de arrastar e soltar (drag-and-drop) para upload de fotos, com pré-visualização imediata no navegador.

### ⚙️ Sistema & Gestão (Backend)

* **CRUD Completo de Produtos:** Capacidade de Criar, Ler, Atualizar e Deletar registros de relógios.
* **Gestão Dinâmica de Marcas:**
    * Cadastro de novas coleções/marcas via modal, sem sair da tela de cadastro de produtos.
    * Dropdowns inteligentes que carregam as marcas disponíveis do banco de dados.
* **Upload de Arquivos:** Sistema seguro de upload de imagens locais, renomeação automática para evitar conflitos e armazenamento em diretório estático.
* **API RESTful:** Endpoints JSON bem estruturados (`/produtos`, `/marcas`) servindo o frontend.

---

## 🚀 Tecnologias Utilizadas

### Frontend
- **HTML5 Semântico**
- **Tailwind CSS (via CDN):** Para estilização utilitária rápida e responsiva.
- **JavaScript (Vanilla):** Para manipulação do DOM, lógica de modais e requisições `fetch` assíncronas.

### Backend
- **Python 3:** Linguagem base.
- **Flask:** Microframework web para rotas e lógica de servidor.
- **Flask-CORS:** Para gerenciamento de permissões de acesso entre origens (Cross-Origin Resource Sharing).
- **Werkzeug:** Para segurança no tratamento de nomes de arquivos de upload.

### Banco de Dados
- **MySQL:** Banco de dados relacional.
- **MySQL Connector:** Driver de conexão Python.

---

## 🗄️ Estrutura de Dados

O projeto utiliza um esquema relacional para garantir a integridade entre os produtos e suas respectivas coleções (marcas).

### Tabela: Marcas
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INT (PK) | Identificador único da marca |
| `nome` | VARCHAR(100) | Nome da coleção (ex: Marine Star) |
| `imagem_url` | VARCHAR(255) | Caminho da imagem do logo/coleção |

### Tabela: Produtos
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | INT (PK) | Identificador único do relógio |
| `nome` | VARCHAR(255) | Nome do modelo |
| `preco` | DECIMAL(10, 2) | Valor monetário |
| `imagem_url` | VARCHAR(255) | Caminho da foto do relógio |
| `descricao` | TEXT | Detalhes técnicos e descrição |
| `material` | VARCHAR(100) | Composição (ex: Aço Inoxidável) |
| `marca_id` | INT (FK) | Chave estrangeira ligada à tabela Marcas |

---

## 📸 Galeria

| **Home (Carrossel 3D)** | **Detalhes do Produto** |
|:---:|:---:|
| *[Insira screenshot aqui]* | *[Insira screenshot aqui]* |

| **Painel de Gestão** | **Cadastro & Upload** |
|:---:|:---:|
| *[Insira screenshot aqui]* | *[Insira screenshot aqui]* |

---

<p align="center">
  Feito com 🧡 por Isabella
</p>
