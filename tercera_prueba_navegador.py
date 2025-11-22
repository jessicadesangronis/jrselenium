from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# --- Inicialización del Driver ---
def initialize_driver():
 # Configurar opciones para deshabilitar las ventanas emergentes del navegador
    chrome_options = Options()
    
    # 1. Deshabilitar el pop-up de 'Guardar Contraseña'
    chrome_options.add_argument("--disable-save-password-bubble")
    # 2. Deshabilitar el pop-up de 'Notificaciones' (útil en general)
    chrome_options.add_argument("--disable-notifications")
    # 3. Deshabilitar la extensión de administrador de contraseñas
    # Esto ayuda a evitar el pop-up de 'Cambia la contraseña' que viste
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)

# Configurar el servicio 
    # Inicializa y descarga/usa automáticamente el driver de Chrome más reciente
    # Usamos la clase Service para pasar la ruta del driver a webdriver.Chrome
    driver_path = ChromeDriverManager().install()
    service = Service(executable_path=driver_path)
    # Crear el driver, pasando tanto el servicio como las opciones
    driver = webdriver.Chrome(service=service, options=chrome_options) 
    
    return driver

# --- Lógica de Login/Logout ---
# Define el usuario a usar (la contraseña se obtiene del sitio web de demo)
def login(driver, user_name_to_use): # Acepta un argumento
    # Realiza el proceso de inicio de sesión en saucedemo.com.
    input_username = driver.find_element(By.ID, "user-name")
    input_username.send_keys(user_name_to_use) # Usa el argumento

    # Bloque para obtener la contraseña de la página (como lo hace el código original)
    # *Nota: La etiqueta “standard_user” que es el nombre de usuario de la página demo, no tiene un ID, CCS_SELECTOR, ni un CLASS_NAME, además no es un elemento independiente, sino que forma parte de un DIV PADRE, por esta razón usaremos código para extraer con XPATH el contenedor div padre completo, y luego extraer la segunda línea “standard_user”, luego se repite con la contraseña.
    try:
        container_password = driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[2]/div[2]")
        split_container_password = container_password.text.split("\n")
        # Se asume que el segundo elemento de la lista dividida es la contraseña
        password = split_container_password[1] 
    except:
        password = "secret_sauce" 
        print("Advertencia: No se pudo obtener la contraseña por XPath. Usando 'secret_sauce'.")

    input_password = driver.find_element(By.ID, "password") 
    input_password.send_keys(password) 

    #Luego de escribir en los cuadros de texto “Username” y “password” el usuario y la contraseña, hacemos click en el botón LOGIN
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    return driver

def main():
    # Función principal que ejecuta la secuencia de prueba.

    user_name = "standard_user" 
    
    print("Iniciando prueba de Login/Logout en Chrome...")
    driver = initialize_driver() 
    driver.get("https://www.saucedemo.com/")
    
    driver = login(driver, user_name) # Pasa el argumento

    # Verifica si el inicio de sesión fue exitoso
    if driver.current_url == "https://www.saucedemo.com/inventory.html":
        # Cierra sesión
        print("Login exitoso. Procediendo a Logout...")
        menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
        menu_button.click()
        
        # INSERTO UNA NUEVA ESPERA AQUÍ para que el menú lateral se abra ===
        # El ID del contenedor del menú lateral es 'menu-sidebar' (o similar)
        # Usaremos el ID de la barra lateral de Sauce Demo: "menu-sidebar"
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "bm-menu-wrap"))
        )
        
        # La Espera por el botón de Logout ahora funcionará correctamente
        logout_button = WebDriverWait(driver, 10).until( 
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link")) 
        )
        logout_button.click()
        print('LogOut success')
        
        driver.quit() # Cierra el navegador
    else:
        print("Login failed")
        driver.quit() # Cierra el navegador

if __name__ == '__main__':
    main()
