# Maestro dos Filtros: Osciloscópio Humano 🎹⚡

## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos

O **Maestro dos Filtros** é uma experiência interativa de áudio e visão computacional. O objetivo é permitir que o usuário controle a síntese de uma onda senoidal pura em tempo real usando apenas o movimento das mãos, simulando o funcionamento de um gerador de funções e um osciloscópio.

---

## 🎮 Orientações de Uso

O jogo funciona detectando a posição das suas mãos através da webcam:

1.  **Mão Direita (Sintonia):** Mova sua mão horizontalmente (eixo X). 
    - Levar a mão para a **direita** aumenta a frequência (o som fica mais agudo).
    - Levar a mão para a **esquerda** diminui a frequência (o som fica mais grave).
2.  **Mão Esquerda (Potenciômetro):** Mova sua mão verticalmente (eixo Y).
    - Subir a mão aumenta a **amplitude** (o som fica mais alto).
    - Descer a mão diminui a **amplitude** (o som fica mais baixo).
3.  **Visualização:** Observe a linha preta no centro da tela. Ela representa a onda senoidal que você está criando!

---

## 🧠 Explicação Técnica (Lógica do Código)

### 1. Síntese de Áudio (NumPy + Pygame Mixer)
Diferente de jogos que tocam arquivos MP3, este projeto gera o som **matematicamente** frame a frame.
* **Função `gerar_onda_senoidal`**: Utiliza a biblioteca `numpy` para criar um sinal baseado na fórmula:  
    `Sinal = Amplitude * sen(2 * pi * frequencia * tempo)`
* O array resultante é convertido para 16-bits e enviado ao buffer de áudio do Pygame.

### 2. Visão Computacional (MediaPipe Hands)
O código diferencia as mãos através do rótulo (`label`) "Left" ou "Right" fornecido pelo MediaPipe.
* Rastreamos o **Landmark 8** (ponta do dedo indicador) para obter coordenadas precisas.
* As coordenadas são normalizadas para os limites da tela (800x600) e mapeadas para valores de frequência (Hz) e amplitude (0 a 1).

### 3. Plotagem do Osciloscópio Virtual
Para criar o gráfico da senóide em tempo real:
* Utilizamos `pygame.draw.lines` ligando uma série de pontos calculados pela mesma função seno do áudio.
* **Escalonamento Visual:** Para que a onda não fique "embolada" em frequências altas, aplicamos um fator de escala para que o usuário sempre consiga ver as cristas e vales da onda de forma didática.

---

## 🛠️ Requisitos de Instalação

```bash
pip install opencv-python mediapipe pygame numpy
