# ⚡ SEL-Ninja: Semana de Recepção dos Bixos - 2026 ⚡

## Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos

O **SEL-Ninja** é um jogo inspirado no clássico *Fruit Ninja*, desenvolvido com **Python**, **OpenCV** e **Pygame**. O projeto utiliza visão computacional para rastrear a mão do usuário através da webcam, permitindo que ele interaja com componentes eletrônicos na tela.

---

## 🚀 Como Funciona
- **Objetivo:** Coletar o máximo de componentes elétricos (resistores, capacitores, etc.) em **60 segundos**.
- **Controle:** O jogo rastreia a ponta do seu **dedo indicador**. Use-o como se fosse uma chave de fenda para atingir os itens.
- **Obstáculo:** Evite atingir o ícone da **SASEL**. Se atingi-lo, você perde uma vida e a tela pisca em vermelho.
- **Condições de Fim de Jogo:** O jogo termina se as suas 3 vidas acabarem ou se o tempo de 60 segundos esgotar.

## 🛠️ Tecnologias Utilizadas
* **Python 3.11.9**
* **OpenCV**: Para captura e processamento de imagem da webcam.
* **MediaPipe**: Para o rastreamento (tracking) das mãos em tempo real.
* **Pygame**: Para a lógica do jogo, interface gráfica e colisões.

## 📋 Pré-requisitos
Para rodar este projeto, você precisará instalar as dependências abaixo. É recomendado o uso do NumPy na versão 1.x para garantir compatibilidade:

```bash
pip install "numpy<2"
pip install opencv-python mediapipe pygame
```

## 🧠 Lógica e Estrutura do Código

O projeto foi estruturado de forma modular para facilitar a manutenção e garantir que o processamento da visão computacional não trave a interface gráfica do jogo.

### 1. Funções Principais
* **`carregar_imagem(nome, tamanho)`**: Gerencia a importação de ativos. Possui um sistema de *fallback* que desenha um bloco colorido caso o arquivo de imagem não seja encontrado, evitando que o programa feche por erro de diretório.
* **`tratar_camera(camera, hands, LARGURA, ALTURA)`**: É a ponte entre o OpenCV e o Pygame. 
    * Captura o frame da webcam.
    * Inverte a imagem (espelhamento) para tornar a interação intuitiva.
    * Converte o padrão de cor de BGR para RGB (exigido pelo MediaPipe).
    * Retorna a coordenada exata da ponta do dedo indicador (Landmark 8).
* **`desenhar_botao(...)`**: Uma função customizada para criar botões interativos que detectam a posição do mouse e cliques, mudando de cor quando o usuário passa o cursor sobre eles.

### 2. Classes
* **`Item`**: Define o comportamento de cada componente elétrico que surge na tela.
    * **Atributos**: Define se o item é um "ponto" (componente) ou um "dano" (logo SASEL), além de sua velocidade aleatória.
    * **Física**: Utiliza uma lógica simples de gravidade, onde a velocidade vertical (`vel_y`) recebe um incremento constante a cada frame, criando o efeito de parábola (sobe e depois cai).

### 3. Lógica de Interação (Colisão)
Diferente de jogos que usam o mouse, a colisão aqui é calculada através do método `rect.collidepoint(pos_dedo)`. O Pygame verifica se a coordenada `(x, y)` enviada pelo MediaPipe está dentro da área ocupada pelo retângulo da imagem do componente.

### 4. Gerenciamento de Estados
O jogo utiliza uma **Máquina de Estados** simples para controlar o que aparece na tela:
1.  **MENU**: Exibe a tela inicial e aguarda o clique no botão "JOGAR".
2.  **JOGANDO**: Ativa a câmera, o rastreamento de mãos e o surgimento de itens.
3.  **PERDEU/FIM DE JOGO**: Para o processamento dos itens e exibe a pontuação final, oferecendo a opção de resetar as variáveis (vidas, pontos e cronômetro).

### 5. Feedback Visual e Auditivo
* **Flash de Dano**: Ao atingir um item incorreto, o fundo da tela muda para vermelho por um curto período (5 frames). Isso é controlado por um contador decrescente que sobrepõe a cor branca padrão.
* **Cronômetro**: Baseado no `clock.tick(60)`, o jogo conta 60 frames para subtrair 1 segundo do tempo total, garantindo precisão independente da velocidade do processador.
