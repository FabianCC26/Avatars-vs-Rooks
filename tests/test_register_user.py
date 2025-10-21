
# Prueba para crar dos usuarios en la base de datos

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.auth.register_user import registrar_usuario

# Ejemplo de usuario jugador
player_data = {
    "role": "player",
    "username": "jugador123",
    "email": "jugador@example.com",
    "password": "abc123"
}

# Ejemplo de administrador
admin_data = {
    "role": "admin",
    "username": "admin001",
    "name": "Juan",
    "lastname": "Pérez",
    "nationality": "Argentina",
    "email": "admin@example.com",
    "password": "admin123"
}

# Pruebas
print("Registrando jugador...")
print(registrar_usuario(player_data))

print("\nRegistrando administrador...")
print(registrar_usuario(admin_data))
