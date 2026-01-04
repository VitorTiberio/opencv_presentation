# OpenCV & Computer Vision: Projetos para demonstração de OpenCV ⚡

### Autores: 
Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos

---

Este repositório contém uma série de aplicações interativas desenvolvidas com **Python**, **OpenCV** e **MediaPipe** para apresentações do curso de Engenharia Elétrica (SEL) da USP São Carlos. O objetivo é demonstrar de forma lúdica conceitos de visão computacional, processamento de sinais e interação humano-computador para a população, em feiras, amostras e eventos de tecnologia!

---

## 🎮 Jogos e Aplicações

### 1. SEL-Ninja (Fruit Ninja Edition)
Inspirado no clássico jogo de coletar itens, o usuário deve usar o dedo indicador para capturar componentes eletrônicos.
- **Destaque:** Detecção de colisão entre o cursor rastreado e objetos em queda parabólica.
- **Física:** Simulação de gravidade aplicada aos componentes.

### 2. Maestro dos Filtros (Osciloscópio Humano)
Uma aplicação de síntese de áudio em tempo real que transforma movimentos das mãos em ondas sonoras.
- **Controle:** A mão esquerda controla a **Amplitude** (volume) e a mão direita controla a **Frequência** (tom).
- **Visualização:** Um gráfico senoidal (osciloscópio virtual) é gerado dinamicamente na tela baseado nos parâmetros de entrada das mãos.

### 3. Teclado Visual SEL
Um teclado musical polifônico virtual que permite tocar notas e acordes no ar.
- **Polifonia:** Suporte para detecção simultânea de ambas as mãos.
- **Sinais:** Síntese de áudio via NumPy utilizando a escala temperada musical (Dó a Si).

---

## 🧠 Arquitetura Técnica

Todas as aplicações compartilham uma base tecnológica comum focada em performance e tempo real:

* **Rastreamento de Mãos**: Utilização do MediaPipe para extração de 21 coordenadas (landmarks) espaciais das mãos.
* **Ponto de Controle**: O sistema foca no **Landmark 8** (ponta do dedo indicador) para precisão em tarefas de seleção e toque.
* **Normalização de Coordenadas**: Conversão de dados normalizados da câmera (0.0 a 1.0) para a resolução da janela gráfica (Pygame).
* **Gerenciamento de Estados**: Implementação de máquinas de estados simples para alternar entre Menu, Gameplay e Telas de Fim de Jogo.

---

## 🛠️ Instalação e Requisitos

Para rodar qualquer um dos projetos, certifique-se de ter o Python instalado e execute a instalação das dependências:

```bash
pip install "numpy<2"
pip install opencv-python mediapipe pygame
