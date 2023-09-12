#include <M5StickCPlus.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLE2902.h>

float accX, accY, accZ; // values for the accelerometer 

const int button = 37; // G37 on M5StickC

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define ACCELEROMETER_UUID "5e8be540-13b8-49bf-af35-63b725c5c066"
#define BUTTON_UUID "e672f43d-ee01-4e48-bf96-4e772413c930"


BLEServer* pServer = NULL; 
BLECharacteristic* pAccelerometer = NULL;
BLECharacteristic* pButton = NULL;
bool deviceConnected = false;
bool advertising = false;

int num = 0;

class MyServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer, esp_ble_gatts_cb_param_t *param) {
    Serial.println("Device connected");
    deviceConnected = true;
    advertising = false;
  };
  
  void onDisconnect(BLEServer* pServer) {
    Serial.println("Device disconnected");
    deviceConnected = false;
  }
};

void setup() {

  M5.begin(); 

  // Service Config
  BLEDevice::init("M5StickCPlus-Maddie");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Accelerometer Characterisitc Config
  pAccelerometer = pService->createCharacteristic(
                      ACCELEROMETER_UUID,
                      BLECharacteristic::PROPERTY_READ    |
                      BLECharacteristic::PROPERTY_NOTIFY 
                    );
  pAccelerometer->addDescriptor(new BLE2902());

  // Button Characterisitc Config
  pButton = pService->createCharacteristic(
                      BUTTON_UUID,
                      BLECharacteristic::PROPERTY_READ    |
                      BLECharacteristic::PROPERTY_NOTIFY 
                    );
  pButton->addDescriptor(new BLE2902());

  pService->start();
  BLEDevice::startAdvertising();

  M5.IMU.Init(); //initializing accelerometer

  pinMode(button, INPUT_PULLUP); // Set up button
}

int waitingForRelease = 0; 
void loop(){

if (deviceConnected){
  
//Accelerometer Section
M5.IMU.getAccelData(&accX, &accY, &accZ);
      
// creating a buffer to hold the accelerometer data
uint8_t buffer1[12];
      
// converting the accelerometer data to a byte array
memcpy(buffer1, &accX, sizeof(float));
memcpy(buffer1+sizeof(float), &accY, sizeof(float));
memcpy(buffer1+2*sizeof(float), &accZ, sizeof(float));
      
// Send the accelerometer data over BLE
pAccelerometer->setValue(buffer1, 12);
pAccelerometer->notify();

M5.Lcd.printf("X:%5.2f\nY:%5.2f\nZ:%5.2f ", accX, accY, accZ);

//Button Section
// creating a buffer to hold the accelerometer data
uint8_t buttonStatus = 0;
uint8_t buffer2[sizeof(buttonStatus)];

if(digitalRead(button)==LOW && !waitingForRelease)
{
    buttonStatus = 1;
    waitingForRelease = 1;   

}  

if(digitalRead(button)==HIGH)
{
    waitingForRelease = 0;
}

memcpy(buffer2, &buttonStatus, sizeof(int));

// Send the button data over BLE
pButton->setValue(buffer2, sizeof(buttonStatus));
pButton->notify();

delay(100);
  
}
if (!deviceConnected && !advertising){

BLEDevice::startAdvertising();
Serial.println("start advertising");
advertising = true;

}


}
