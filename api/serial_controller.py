import serial
import threading

# Variável global para armazenar o último botão pressionado
last_button_pressed = None
arduino = None

def read_from_arduino():
    global last_button_pressed
    while True:
        try:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').strip()
                if line in ['ok1', 'ok2', 'ok3']:
                    last_button_pressed = line
                    print(last_button_pressed)
        except Exception as e:
            print("Erro ao ler do Arduino:", e)

def init_arduino(port='COM6', baudrate=9600):
    global arduino
    try:
        arduino = serial.Serial(port, baudrate, timeout=1)
        threading.Thread(target=read_from_arduino, daemon=True).start()
        print("Arduino conectado e leitura iniciada.")
        return True
    except Exception as e:
        print("Erro ao conectar com Arduino:", e)
        return False
    
def is_arduino_connected():
    global arduino
    return arduino is not None and arduino.is_open

def get_last_button():
    global last_button_pressed
    btn = last_button_pressed
    last_button_pressed = None
    return btn
