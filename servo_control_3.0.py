import serial
from pynput import keyboard

ser = serial.Serial('COM3', 9600)

keys_to_servos = {
    'q': (1, 'P'), 'w': (2, 'P'), 'e': (3, 'P'), 'r': (4, 'P'), 't': (5, 'P'),
    'y': (6, 'P'), 'u': (7, 'P'), 'i': (8, 'P'), 'o': (9, 'P'), 'p': (10, 'P'),
    'a': (1, 'B'), 's': (2, 'B'), 'd': (3, 'B'), 'f': (4, 'B'), 'g': (5, 'B'),
    'h': (6, 'B'), 'j': (7, 'B'), 'k': (8, 'B'), 'l': (9, 'B'), ';': (10, 'B')
}

def on_press(key):
    if key.char in keys_to_servos:
        servo_number, action = keys_to_servos[key.char]
        ser.write(action.encode('utf-8'))
        if servo_number != 10:
            ser.write(str(servo_number).encode('utf-8'))
        else:
            ser.write(':'.encode('utf-8'))

def on_release(key):
    if key.char in keys_to_servos:
        servo_number, action = keys_to_servos[key.char]
        if action == 'P':
            ser.write('R'.encode('utf-8'))
            if servo_number != 10:
                ser.write(str(servo_number).encode('utf-8'))
            else:
                ser.write(':'.encode('utf-8'))
        elif action == 'B':
            ser.write('R'.encode('utf-8'))
            if servo_number != 10:
                ser.write(str(servo_number).encode('utf-8'))
            else:
                ser.write(':'.encode('utf-8'))

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
