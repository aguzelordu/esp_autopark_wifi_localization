#include <WiFi.h>
#include "Arduino.h"
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <VL53L0X.h>

const char* ssid           = "your_ssid";                  // SSID Name
const char* password       = "your_password";                // SSID Password - Set to NULL to have an open AP

AsyncWebServer server(80);

long duration;
float distanceCm;

int t_s = 0;
int b_s = 0;
int r_s = 0;
int l_s = 0;
int x = 0;
int lock = 0;
int tofDistance;


#define SOUND_SPEED 0.034
#define trigPin  18
#define echoPin  19

#define SDA_PIN 21
#define SCL_PIN 22

#define MOTOR_R_PIN_1   12  //pin number
#define MOTOR_R_PIN_2   14    //pin number

#define ENA 13 // YELLOW
#define ENB 25 // WHITE

#define MOTOR_L_PIN_1 27    //pin number
#define MOTOR_L_PIN_2 26    //pin number

VL53L0X tof200c;


WiFiUDP Udp; 
unsigned int Port = 4210;
char incomingPacket[200];

unsigned long previousMillis = 0;
const long interval = 600;

const int ledPin = 2; // The pin (GPIO 2) on the ESP32 that the internal blue LED is connected to


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  // WiFi connection
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("WiFi connecting...");
  }

  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Start web server
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/html", R"HTMLHOMEPAGE(
      <!DOCTYPE html>
      <html>
      <head>
        <title>Car Control</title>
        <style>
          button {
            width: 100px;
            height: 100px;
            font-size: 20px;
          }
        </style>
      </head>
      <body>
        <h1>Car Control</h1>
        <button onclick="sendRequest('/backward')">BACKWARD</button>
        <br><br>
        <button onclick="sendRequest('/left')">LEFT</button>
        <button onclick="sendRequest('/stop')">STOP</button>
        <button onclick="sendRequest('/right')">RIGHT</button>
        <br><br>
        <button onclick="sendRequest('/forward')">FORWARD</button>

        <script>
          function sendRequest(path) {
            fetch(path)
              .then(response => {
                console.log(response);
              })
              .catch(error => {
                console.error(error);
              });
          }
        </script>
      </body>
      </html>
    )HTMLHOMEPAGE");
  });

  server.on("/forward", HTTP_GET, [](AsyncWebServerRequest *request){
    goForward();
    request->send(200, "text/plain", "go forward");
  });

  server.on("/backward", HTTP_GET, [](AsyncWebServerRequest *request){
    goBackward();
    request->send(200, "text/plain", "go backward");
  });

  server.on("/right", HTTP_GET, [](AsyncWebServerRequest *request){
    turnRight();
    request->send(200, "text/plain", "turn right");
  });

  server.on("/left", HTTP_GET, [](AsyncWebServerRequest *request){
    turnLeft();
    request->send(200, "text/plain", "turn left");
  });

  server.on("/stop", HTTP_GET, [](AsyncWebServerRequest *request){
    stopMoving();
    request->send(200, "text/plain", "stop");
  });

  // Start server
  server.begin();
  
  Wire.begin(SDA_PIN, SCL_PIN);
  tof200c.init();
//  tof200c.configureDefault();
  tof200c.setTimeout(500);

  //Distance Sensor
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  //Sağ motor
  pinMode(MOTOR_R_PIN_1,OUTPUT);
  pinMode(MOTOR_R_PIN_2,OUTPUT);
  //Sol Motor
  pinMode(MOTOR_L_PIN_1,OUTPUT);
  pinMode(MOTOR_L_PIN_2,OUTPUT);
  // PWM hızını ayarla (0-255)
  analogWrite(ENA, 0); // Motor A speed
  analogWrite(ENB, 0); // Motor B speed

  pinMode(ledPin, OUTPUT); // LED pin as a output
}


void loop() {
unsigned long currentMillis = millis();
  /*
  if (currentMillis - previousMillis >= interval) {
    
    int packetSize = Udp.parsePacket();
    if (packetSize)
    {
      // receive incoming UDP packets
      Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
      int len = Udp.read(incomingPacket, 255);
      if (len > 0)
      {
        incomingPacket[len] = 0;
      }
      Serial.printf("UDP packet contents: %s\n", incomingPacket);
    }

    String data = incomingPacket;
    previousMillis = currentMillis;
  }
  */
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance
  distanceCm = duration * 0.034 /2;
  
  // Prints the distance in the Serial Monitor
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);

  tofDistance = tof200c.readRangeSingleMillimeters();

  if (tof200c.timeoutOccurred()) {
    Serial.println("Time out!");
    digitalWrite(ledPin, LOW); // Close LED
  } else {
    Serial.print("tofDistance (mm): ");
    Serial.println(tofDistance);
    digitalWrite(ledPin, HIGH); // open LED
  }
  
  if(tofDistance > 100)
  {
    digitalWrite(ledPin, LOW); // close LED
  }else{
    digitalWrite(ledPin, HIGH); // open LED
  }

  delay(200);
}

// Turn right function
void turnRight() {
  digitalWrite(MOTOR_R_PIN_1, HIGH);
  digitalWrite(MOTOR_R_PIN_2, LOW);
  digitalWrite(MOTOR_L_PIN_1, LOW);
  digitalWrite(MOTOR_L_PIN_2, HIGH);

  analogWrite(ENA, 50);
  analogWrite(ENB, 100);
}

// Turn left function
void turnLeft() {
  digitalWrite(MOTOR_R_PIN_1, LOW);
  digitalWrite(MOTOR_R_PIN_2, HIGH);
  digitalWrite(MOTOR_L_PIN_1, HIGH);
  digitalWrite(MOTOR_L_PIN_2, LOW);
  
  analogWrite(ENA, 100);
  analogWrite(ENB, 50);
}

// Go forward function
void goForward() {
  digitalWrite(MOTOR_R_PIN_1, HIGH);
  digitalWrite(MOTOR_R_PIN_2, LOW);
  digitalWrite(MOTOR_L_PIN_1, HIGH);
  digitalWrite(MOTOR_L_PIN_2, LOW);

  analogWrite(ENA, 100);
  analogWrite(ENB, 100);
}

// Go backward function
void goBackward() {
  digitalWrite(MOTOR_R_PIN_1, LOW);
  digitalWrite(MOTOR_R_PIN_2, HIGH);
  digitalWrite(MOTOR_L_PIN_1, LOW);
  digitalWrite(MOTOR_L_PIN_2, HIGH);

  analogWrite(ENA, 100);
  analogWrite(ENB, 100);
}


void stopMoving()
{
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}
