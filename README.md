#  Clash of Clans - Gerador de Relatórios em PDF

Este projeto consiste em uma série de scripts Python desenvolvidos para interagir com a API oficial do Clash of Clans. A ferramenta principal coleta dados detalhados sobre os membros de um clã e compila todas as informações em um relatório profissional e bem formatado em PDF.

## 🚀 Funcionalidades

* **Conexão com a API Oficial:** Utiliza a API da Supercell para buscar dados em tempo real.
* **Análise Detalhada de Jogadores:** Coleta informações individuais de cada membro, incluindo:
    * Nível do Centro de Vila (CV)
    * Níveis de todos os Heróis
    * Total de Estrelas de Guerra
    * Recorde de Troféus
* **Geração de Relatório em PDF:** Cria um documento PDF com um resumo do clã, imagens dos Centros de Vila e uma lista de todos os jogadores, ordenada por força.
* **Scripts Auxiliares:** Inclui ferramentas para automatizar o download e a conversão de imagens necessárias para o relatório.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Requests:** Para fazer as chamadas à API.
* **ReportLab:** Para a criação e formatação do documento PDF.
* **Pillow (PIL):** Para o processamento e conversão de imagens.

## 📋 Como Usar

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    ```
2.  **Instale as dependências:**
    ```bash
    pip install requests reportlab Pillow
    ```
3.  **Obtenha sua chave de API:** Crie uma chave no [Portal de Desenvolvedores do Clash of Clans](https://developer.clashofclans.com/) e configure seu IP.
4.  **Configure o Script:** Insira sua chave de API (`TOKEN`) e a tag do seu clã (`CLAN_TAG`) no arquivo `index.py`.
5.  **Execute o script:**
    ```bash
    python index.py
    ```