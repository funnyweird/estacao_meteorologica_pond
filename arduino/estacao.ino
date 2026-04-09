void setup() {
  // Inicia a comunicação serial a 9600 bits por segundo
  Serial.begin(9600);
}

void loop() {
  // Gerando valores aleatórios realistas para simular os sensores
  // Temperatura entre 20.0 e 35.0 ºC
  float temp = random(200, 350) / 10.0; 
  // Umidade entre 40.0 e 80.0 %
  float umid = random(400, 800) / 10.0; 

  // Imprimindo os dados no formato JSON exigido pelo projeto
  Serial.print("{");
  Serial.print("\"temperatura\":"); Serial.print(temp);
  Serial.print(",\"umidade\":"); Serial.print(umid);
  Serial.println("}");

  // Aguarda 5 segundos (5000 milissegundos) para a próxima leitura
  delay(5000);
}
