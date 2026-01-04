# Laboratório de Filtros PDI: Processamento de Imagens em Tempo Real 📸⚡

## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos

Este projeto é uma ferramenta interativa desenvolvida para demonstrar os fundamentos do **Processamento Digital de Imagens (PDI)**. Através de uma interface intuitiva, o usuário pode aplicar diferentes transformações matemáticas e filtros espaciais diretamente no fluxo de vídeo da webcam.

---

## 🎨 Filtros Disponíveis e Conceitos Aplicados

O laboratório conta com 10 modos de visualização, cada um representando um conceito clássico de engenharia:

* **Original**: Captura direta sem processamento.
* **Cinza**: Conversão do espaço de cor BGR para tons de cinza (Y), baseada na sensibilidade do olho humano.
* **Negativo**: Inversão bit a bit de todos os pixels da imagem.
* **Canny (Bordas)**: Algoritmo de detecção de bordas que utiliza o gradiente da imagem para identificar transições bruscas de intensidade. [Image of Canny edge detection process]
* **Blur (Desfoque)**: Aplicação de um filtro passa-baixas (Gaussiano) para suavizar ruídos e detalhes de alta frequência.
* **Sepia**: Transformação linear de cores utilizando uma matriz de conversão $3 \times 3$ sobre os canais RGB. [Image of RGB color matrix transformation]
* **Binarização (Threshold)**: Segmentação da imagem em apenas dois níveis (preto ou branco) através de um limiar de intensidade.
* **Laplaciano**: Operador diferencial de segunda ordem utilizado para realçar bordas e detalhes finos (high-frequency accentuation).
* **Cores Quentes (JET)**: Mapeamento de níveis de intensidade para uma escala pseudocolorida, simulando a visualização de câmeras térmicas de inspeção elétrica.
* **Cartoon**: Combinação de filtragem bilateral (preservação de bordas) com limiarização adaptativa para simular um desenho artístico.

---

## 🧠 Arquitetura Técnica

### 1. Manipulação de Matrizes (OpenCV + NumPy)
Diferente de filtros prontos, o sistema trata a imagem como um **tensor (matriz multidimensional)**. Cada filtro é uma operação algébrica aplicada a essa matriz:
* **Convolução Espacial**: Usada em filtros como Blur e Laplaciano.
* **Mapeamento de Pontos**: Usado em Negativo e Binarização.

### 2. Integração Pygame + OpenCV
Para garantir que a interface gráfica não prejudique a taxa de quadros (FPS):
* O processamento é feito no OpenCV (formato BGR).
* A conversão para o Pygame é otimizada via `pygame.surfarray`, transpondo os eixos da matriz para exibição direta em tela.

---
