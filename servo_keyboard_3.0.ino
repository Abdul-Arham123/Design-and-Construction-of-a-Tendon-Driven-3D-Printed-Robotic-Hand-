#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

unsigned long previousMillis = 0;
const long interval = 20; // Time between servo movements in milliseconds
bool servoMoving[10] = {false, false, false, false, false, false, false, false, false, false}; // Array to track the movement state of each servo
int angle[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int direction[10] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1};

void setup() {
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate
  pwm.begin();
  pwm.setPWMFreq(60);
  Serial.println("Ready for keyboard input (1-10):");
}

void loop() {
  if (Serial.available() > 0) { // Check if there is any data in the serial buffer
    char action = Serial.read(); // Read a single character from the serial buffer

    if (action == 'P' || action == 'R' || action == 'B') { // Check if the character is 'P' (pressed) or 'R' (released) or 'B' (reverse pressed)
      while (Serial.available() == 0); // Wait for the next character (servo number) to arrive
      char input = Serial.read(); // Read the servo number

      if (input >= '1' && input <= '9') {
        int servoNumber = input - '1';            // Convert the character to an integer representing the servo number (0-8)
        if (action == 'P') {
          servoMoving[servoNumber] = true;        // Start moving the servo
          direction[servoNumber] = 1;
        } else if (action == 'R') {
          servoMoving[servoNumber] = false;        // Stop moving the servo
        } else if (action == 'B') { 
          servoMoving[servoNumber] = true;       // Start moving the servo in reverse direction
          direction[servoNumber] = -1;
        }
      } else if (input == ':') {
        int servoNumber = 9;
        if (action == 'P') {
          servoMoving[servoNumber] = true; // Start moving the servo
          direction[servoNumber] = 1;
        } else if (action == 'R') {
          servoMoving[servoNumber] = false; // Stop moving the servo
        } else if (action == 'B') {
          servoMoving[servoNumber] = true; // Start moving the servo in reverse direction
          direction[servoNumber] = -1;
        }
      } else {
        Serial.println("Invalid input. Please enter a number between 1 and 10.");
      }
    }
  }

  moveServos();
}

void moveServos() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    // Save the last time servo movement was executed
    previousMillis = currentMillis;

    for (int servoNumber = 0; servoNumber < 10; servoNumber++) {
      if (servoMoving[servoNumber]) {
        angle[servoNumber] += direction[servoNumber];

        if (angle[servoNumber] >= 180) {
          angle[servoNumber] = 180;
        } else if (angle[servoNumber] <= 0) {
          angle[servoNumber] = 0;
        }

        pwm.setPWM(servoNumber, 0, map(angle[servoNumber], 0, 180, 150, 600));
      }
    }
  }
}
