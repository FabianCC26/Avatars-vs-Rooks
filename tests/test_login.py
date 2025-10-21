
from src.auth.login_user import login_por_username

def probar_login():
    print("=== PRUEBA DE LOGIN POR USERNAME ===")
    username = input("Usuario: ")
    password = input("Contraseña: ")

    resultado = login_por_username(username, password)

    if resultado:
        print(f"\n👤 Bienvenido {resultado.get('name', 'Usuario')}")
        print(f"🔹 Rol: {resultado.get('role', 'Sin rol asignado')}")
    else:
        print("\n❌ Error en autenticación.")

if __name__ == "__main__":
    probar_login()