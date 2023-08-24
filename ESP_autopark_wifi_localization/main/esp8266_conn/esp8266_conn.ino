#include <ESP8266WiFi.h>
#include <MySQL_Connection.h>
#include <MySQL_Cursor.h>

// WiFi ağ bilgilerini burada belirtin
const char* ssid = "your_ssid";
const char* password = "your_password";

// AWS MySQL veritabanı bilgilerini burada belirtin
const char* hostname = "MySQL_host_name" ;
int server_port = 3306;
const char* user = "admin";
const char* password_db = "admin";
const char* database = "rssi";

// WiFi istemcisini ve MySQL bağlantı nesnelerini oluşturun
WiFiClient client;
MySQL_Connection conn((Client *)&client);
MySQL_Cursor *cursor;

void setup() {
  // Seri bağlantıyı başlat
  Serial.begin(115200);

  // WiFi ağına bağlan
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("WiFi baglaniyor...");
  }

  Serial.println("WiFi baglandi!");

   // DNS çözümlemesi yap
  IPAddress serverIP;
  WiFi.hostByName(hostname, serverIP);

  // MySQL sunucusuna bağlan
  Serial.println("MySQL sunucusuna baglaniliyor...");
  if (conn.connect(serverIP, server_port, const_cast<char*>(user), const_cast<char*>(password_db))) {
    Serial.println("MySQL sunucusuna baglanildi!");
  } else {
    Serial.println("MySQL sunucusuna baglanilamadi." );
    while (1);  // Bağlantı hatası durumunda döngüyü dondur
  }
  // MySQL işaretçi nesnesini başlat
  cursor = new MySQL_Cursor(&conn);
}


void loop() {
  // SELECT sorgusunu gönder
  char SELECT_SQL[] = "SELECT rssi_value FROM rssi4";
  cursor->execute(SELECT_SQL);

  char USE_SQL[] = "USE rssi4";
  cursor->execute(USE_SQL);

  // INSERT sorgusunu gönder
  // RSSI değerini oku
  int rssi = WiFi.RSSI();
  char INSERT_SQL[64];
  sprintf(INSERT_SQL, "INSERT INTO rssi4 (rssi_value) VALUES (%d)", rssi);
  cursor->execute(INSERT_SQL);

  Serial.println("Yeni veri eklendi!");
  Serial.println("RSSI: " + String(rssi));

  delay(500);  // Wait 5 seconds
}
