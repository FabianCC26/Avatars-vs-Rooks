from machine import UART,ADC, Pin
import utime

uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5)) 

# Joystick conectado a los ADC de la Raspberry Pi Pico
adc_x = ADC(27)   # VRx en GP27 (ADC1)
adc_y = ADC(26)   # VRy en GP26 (ADC0)

btn = Pin(16, Pin.IN, Pin.PULL_UP)   # Boton joystick
led = Pin(15, Pin.OUT)               # LED en GP15 (joystick)

boton_guardado = Pin(14, Pin.IN, Pin.PULL_UP)  # Boton de guardado
led_guardado = Pin(13, Pin.OUT)       # LED en GP17 (guardado)

CENTER = 32768
DEADZONE = 5000

ultima_direccion = None
ultimo_boton = 1  # 1 = suelto 0 = presionado

guardado_activo_hasta = 0          # tiempo (en ms) hasta el que debe estar encendido
ultimo_boton_guardado = 1          # para detectar flanco de 1 -> 0

while True:
    raw_x = adc_x.read_u16()
    raw_y = adc_y.read_u16()

    # Desplazamiento respecto al centro
    dx = raw_x - CENTER
    dy = raw_y - CENTER

    # Determinar direccion
    if abs(dx) < DEADZONE and abs(dy) < DEADZONE:
        direccion = "CENTER"
    else:
        if abs(dx) > abs(dy):
            if dx > 0:
                direccion = "UP"
            else:
                direccion = "DOWN"
        else:
            if dy > 0:
                direccion = "RIGHT"
            else:
                direccion = "LEFT"

    # Lectura del boton del joystick
    boton_joystick = btn.value()  # 1 = suelto y 0 = presionado

    # Control del LED del joystick
    if boton_joystick == 0:
        led.value(0)  # encender 
    else:
        led.value(1)  # apagar

    # --- lectura del botón de guardado ---
    estado_guardado = boton_guardado.value()  # 1 = suelto, 0 = presionado
    ahora = utime.ticks_ms()

    if estado_guardado == 0 and ultimo_boton_guardado == 1:
        guardado_activo_hasta = utime.ticks_add(ahora, 1000)  

    # Encender/apagar LED de guardado segun el temporizador
    if utime.ticks_diff(guardado_activo_hasta, ahora) > 0:
        led_guardado.value(0)   # encendido (activo en bajo)
    else:
        led_guardado.value(1)   # apagado

    # Actualizar estado anterior del botón de guardado
    ultimo_boton_guardado = estado_guardado

    if direccion != ultima_direccion or boton_joystick != ultimo_boton:
        # Formato: "DIR:UP BTN:0"
        print(f"DIR:{direccion} BTN:{1 if boton_joystick else 0}")
        uart1.write(f"DIR:{direccion} BTN:{1 if boton_joystick else 0}")
        ultima_direccion = direccion
        ultimo_boton = boton_joystick

    utime.sleep_ms(50)
