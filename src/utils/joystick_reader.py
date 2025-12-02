import serial
"""
    Lee las lineas que envía la Raspberry Pi Pico por el puerto serie.
    Formato esperado de cada linea:
        DIR:UP BTN:0
        DIR:CENTER BTN:1
    """

class JoystickReader:
    def __init__(self, port, baudrate=115200, timeout=0):
        """
        port: nombre del puerto serie, por ejemplo 'COM3' (Windows) o '/dev/ttyACM0' (Linux).
        """
        try:
            self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            self.last_direction = "CENTER"
            self.last_button = 1  # 1 = suelto, 0 = presionado 
            print(f"[JoystickReader] Conectado a {port}")
        except serial.SerialException as e:
            print(f"[JoystickReader] NO se pudo abrir el puerto {port}: {e}")
            self.ser = None
            self.last_direction = "CENTER"
            self.last_button = 1

    def read_state(self):
        """
        Lee una linea del puerto serie y devuelve (direction, button)
        - direction: 'UP', 'DOWN', 'LEFT', 'RIGHT', 'CENTER'
        - button: 0 (presionado) o 1 (suelto)

        Si no hay datos nuevos o no hay puerto, devuelve (last_direction, last_button).
        """

        if self.ser is None:
            return self.last_direction, self.last_button

        try:

            line = self.ser.readline().decode('utf-8').strip()
 
            if not line:
                return self.last_direction, self.last_button

            partes = line.split()
            data = {}

            for p in partes:
                if ":" in p:
                    k, v = p.split(":", 1)
                    data[k] = v

            # Tomar la direccion y boton si estan presentes
            direction = data.get("DIR", self.last_direction)
            btn_str = data.get("BTN", str(self.last_button))

            # Convertir BTN a entero 
            try:
                button = int(btn_str)
            except ValueError:
                button = self.last_button

            # Guardamos como ultimo estado
            self.last_direction = direction
            self.last_button = button

            return direction, button

        except Exception as e:
            # Si algo sale mal
            # devuelve el ultimo
            return self.last_direction, self.last_button
