from src.auth import password_recovery

def probar_recovery():
    print("=== PRUEBA DE RESTABLECIMIENTO DE CONTRASEÑA ===")
    username = input("Ingrese el username del usuario: ")
    password_recovery.restablecer_password_por_username(username)

if __name__ == "__main__":
    probar_recovery()
