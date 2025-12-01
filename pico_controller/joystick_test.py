from machine import ADC, Pin
import utime

# Joystick conectado a los ADC de la Raspberry Pi Pico
adc_x = ADC(27)   # VRx en GP27 (ADC1)
adc_y = ADC(26)   # VRy en GP26 (ADC0)

btn   = Pin(16, Pin.IN, Pin.PULL_UP)        # Boton joystick
boton_guardado = Pin(14, Pin.IN, Pin.PULL_UP)  # Boton de guardado

led   = Pin(15, Pin.OUT)              # LED en GP15 (joystick)
led_guardado = Pin(13, Pin.OUT)       # LED en GP17 (guardado)

# Valores aproximados cuando el joystick esta en el centro
CENTER = 32768
DEADZONE = 5000

ultima_direccion = None

# Tiempo hasta el que el LED de guardado debe permanecer encendido (en ms)
guardado_activo_hasta = 0          
TIEMPO_GUARDADO_MS = 3000          # 1 segundo

while True:
    # Leer valores crudos de los potenciometros
    raw_x = adc_x.read_u16()
    raw_y = adc_y.read_u16()

    # Desplazamiento respecto al centro
    dx = raw_x - CENTER
    dy = raw_y - CENTER

    # Determinar direccion
    if abs(dx) < DEADZONE and abs(dy) < DEADZONE:
        direccion = "CENTRO"
    else:
        if abs(dx) > abs(dy):
            if dx > 0:
                direccion = "ARRIBA"
            else:
                direccion = "ABAJO"
        else:
            if dy > 0:
                direccion = "DERECHA"
            else:
                direccion = "IZQUIERDA"

    # --- Lectura de botones ---
    boton_joystick = btn.value()           # 1 = suelto | 0 = presionado
    estado_guardado = boton_guardado.value()

    # --- Control del LED del joystick ---
    if boton_joystick == 0:
        led.value(0)   # encender 
    else:
        led.value(1)   # apagar

    # --- TIEMPO PARA EL LED DE GUARDADO ---
    ahora = utime.ticks_ms()

    if estado_guardado == 0 and utime.ticks_diff(guardado_activo_hasta, ahora) <= 0:
        print("boton de guardado presionado")
        # Mantener encendido durante TIEMPO_GUARDADO_MS ms desde ahora
        guardado_activo_hasta = utime.ticks_add(ahora, TIEMPO_GUARDADO_MS)

    # Encender/apagar el LED segun si el tiempo de guardado sigue vigente
    if utime.ticks_diff(guardado_activo_hasta, ahora) > 0:
        led_guardado.value(0)   # encendido
    else:
        led_guardado.value(1)   # apagado

    # imprimir la direccion solo cuando se cambia
    if direccion != ultima_direccion:
        print("X:", raw_x, "Y:", raw_y, "->", direccion)
        ultima_direccion = direccion

    utime.sleep_ms(50)

