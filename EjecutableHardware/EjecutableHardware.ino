#include <Wire.h>
#include <LiquidCrystal_PCF8574.h>
#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>

// Pines RFID
#define SS_PIN D2      // SDA del RC522
#define RST_PIN D1     // RST del RC522

// Pin del relé que activa la cerradura
#define RELAY_PIN D0   // GPIO16

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Crear objeto para RFID
LiquidCrystal_PCF8574 lcd(0x27);   // Dirección I2C del LCD

const char* ssid = "Alejandro";               // Tu SSID
const char* password = "roldan1982";          // Tu contraseña WiFi
const char* serverName = "http://172.20.10.2:5000/historial";  // URL del servidor Flask

void setup() {
  Serial.begin(115200);
  Wire.begin(D4, D3);        // SDA = D4, SCL = D3
  lcd.begin(16, 2);
  lcd.setBacklight(255);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Acercar tarjeta");

  SPI.begin();               // Iniciar SPI para RFID
  mfrc522.PCD_Init();        // Inicializar RFID

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);  // Cerradura abierta (perno afuera) al inicio

  // Conectar a WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Conectando a WiFi...");
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    attempts++;
    if (attempts > 15) {
      Serial.println("\nNo se pudo conectar a WiFi.");
      return;
    }
  }
  Serial.println("\nConectado a WiFi.");
  Serial.print("IP Local: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) return;

  // Leer UID y convertir a string hexadecimal en minúscula
  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) uid += "0";
    uid += String(mfrc522.uid.uidByte[i], HEX);
  }
  uid.toLowerCase();

  Serial.print("Identificación: ");
  Serial.println(uid);

  // Enviar UID al servidor
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    http.begin(client, serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{\"uid\":\"" + uid + "\"}";
    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Código HTTP: " + String(httpResponseCode));
      Serial.println("Respuesta del servidor: " + response);

      // Verifica si el servidor otorga permiso
      if (response.indexOf("Acceso autorizado") != -1) {
        // Acceso permitido
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Acceso permitido");
        lcd.setCursor(0, 1);
        lcd.print("hola, Bienvenido");
        lcd.print(uid);

        // Activar la cerradura (cerrar perno)
        digitalWrite(RELAY_PIN, LOW);  // Cerrar cerradura
        delay(5000);                   // Mantener cerradura cerrada 5 segundos
        digitalWrite(RELAY_PIN, HIGH);  // Abrir cerradura (perno afuera)

        // Volver a mensaje de espera
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Acercar Tarjeta");
      } else {
        // Acceso denegado
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Acceso denegado");
        lcd.setCursor(0, 1);
        lcd.print("Intente de nuevo");
        lcd.print(uid);
        delay(3000);  // Mostrar mensaje 3 segundos

        // Volver a mensaje de espera sin activar relé
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Acercar Tarjeta");
      }
    } else {
      Serial.println("Error en la solicitud HTTP: " + String(httpResponseCode));
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Error de red");
      delay(3000);
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Acercar Tarjeta");
    }

    http.end();
  } else {
    Serial.println("No conectado a WiFi.");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Sin conexion");
    delay(3000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Acercar Tarjeta");
  }

  // Detener comunicación con la tarjeta
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();

  delay(1000); // Pequeña pausa para evitar lecturas rápidas
}
