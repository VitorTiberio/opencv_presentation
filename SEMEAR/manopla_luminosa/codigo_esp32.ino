// Autor: Vitor Augusto Tibério - Estudante de Engenharia Elétrica - USP São Carlos // 

// Manopla Luminosa // 

// Definição dos pinos dos LEDs
const int pinosLeds[] = {13, 12, 14, 27, 26};
const int numLeds = 5;

void setup() {
  // Inicia a comunicação Serial
  Serial.begin(115200);

  // Configura todos os pinos como SAÍDA
  for (int i = 0; i < numLeds; i++) {
    pinMode(pinosLeds[i], OUTPUT);
    digitalWrite(pinosLeds[i], LOW); // Começa tudo apagado
  }
}

void loop() {
  // Verifica se o computador enviou alguma informação
  if (Serial.available() > 0) {
    
    // Lê o texto até a quebra de linha
    String recebido = Serial.readStringUntil('\n');
    
    // Remove espaços em branco extras
    recebido.trim();

    // Tenta converter o texto para número inteiro
    int dedos = recebido.toInt();

    // Atualiza os LEDs
    atualizarLeds(dedos);
  }
}

void atualizarLeds(int quantidade) {
  // Garante que a quantidade está entre 0 e 5
  if (quantidade < 0) quantidade = 0;
  if (quantidade > 5) quantidade = 5;
  // Loop para acender ou apagar
  for (int i = 0; i < numLeds; i++) {
    if (i < quantidade) {
      digitalWrite(pinosLeds[i], HIGH); // Acende
    } else {
      digitalWrite(pinosLeds[i], LOW);  // Apaga
    }
  }
}
