# Teclado Visual: Polifonia por Visão Computacional 🎹⚡

# Autores: 
Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos  
João Pedro Alves - Estudante de Engenharia Elétrica - USP São Carlos

---

Este projeto transforma a webcam em um instrumento musical polifônico. Utilizando técnicas de visão computacional, o software identifica as mãos do usuário e mapeia a posição dos dedos para frequências sonoras específicas, permitindo tocar acordes e melodias no ar.

---

## 🎮 Como Jogar na Recepção

1.  **Posicionamento:** Fique de frente para a câmera de modo que seu tronco e mãos apareçam bem.
2.  **Interação:** Use os **dedos indicadores** de ambas as mãos para "tocar" as teclas brancas na tela.
3.  **Polifonia:** O sistema suporta até duas mãos simultâneas, permitindo tocar duas notas ao mesmo tempo (acordes).
4.  **Feedback:** As teclas mudam de cor para cinza quando detectam o toque, e um cursor colorido (Azul/Vermelho) segue seus dedos.

---

## 🧠 Arquitetura e Lógica do Sistema

### 1. Rastreamento Multi-Mão (MediaPipe)
O sistema utiliza o modelo **MediaPipe Hands** configurado para detectar até duas mãos simultaneamente. 
* **Landmark Mapping:** O código foca no **Landmark 8**, que corresponde à ponta do dedo indicador.
* **Normalização:** As coordenadas normalizadas (0.0 a 1.0) recebidas do sensor são convertidas para os pixels da janela (800x600).

### 2. Síntese de Frequências (Engenharia de Sinais)
Em vez de usar amostras gravadas, as notas são geradas via síntese matemática:
* **Frequências de Referência:** Utilizamos a escala temperada (Dó a Si), começando pelo Dó Central ($f = 261.63$ Hz).
* **Processamento Digital:** A função `gerar_nota` cria uma onda senoidal pura usando `NumPy`. Para evitar ruídos abruptos (clicks), aplicamos um **envelope de amplitude** (*fade-out*) linear no final de cada amostra.

### 3. Lógica de Disparo (Debounce de Software)
Para garantir que o som seja agradável, implementamos uma trava de estado:
* O som só é disparado no momento em que o dedo **entra** na zona da tecla.
* Enquanto o dedo permanecer na mesma tecla, o som não é repetido (evitando 60 disparos por segundo).
* O sistema diferencia os estados da "Mão 0" e "Mão 1" de forma independente.

---

## 📋 Requisitos Técnicos

Para rodar o teclado, instale as dependências:

```bash
pip install opencv-python pygame numpy
pip install mediapipe==0.10.9
