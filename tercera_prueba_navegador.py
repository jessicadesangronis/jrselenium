from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

# --- Inicialización del Driver ---
def initialize_driver():
    # driver = webdriver.Chrome() -> re reemplazo por la siguiente línea de código
    # Inicializa y descarga/usa automáticamente el driver de Chrome más reciente
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # Fue reemplazada porque me dava el error AttributeError: 'str' object has no attribute 'capabilities'
    
    # 1. Obtener la ruta del driver usando webdriver-manager
    driver_path = ChromeDriverManager().install()
    # 2. Crear un objeto Service con esa ruta
    service = Service(executable_path=driver_path)
    # 3. Pasar el objeto Service a webdriver.Chrome()
    driver = webdriver.Chrome(service=service)
    
    return driver

# --- Lógica de Login/Logout ---
# Define el usuario a usar (la contraseña se obtiene del sitio web de demo)
user_name = "standard_user" 
def login(driver):
    # Realiza el proceso de inicio de sesión en saucedemo.com.
    input_username = driver.find_element(By.ID, "user-name")
    input_username.send_keys(user_name)

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
    print("Iniciando prueba de Login/Logout en Chrome...")
    driver = initialize_driver() 
    driver.get("https://www.saucedemo.com/")
    driver = login(driver)
    # Verifica si el inicio de sesión fue exitoso
    if driver.current_url == "https://www.saucedemo.com/inventory.html":
        # Cierra sesión
        print("Login exitoso. Procediendo a Logout...")
        menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
        menu_button.click()
        
        # time.sleep(1)  Es posible usar un sleep simple, pero es mejor usar una espera explícita, hasta que el elemento “esté presente” 
        WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.ID, "logout_sidebar_link")) ) 
        
        logout_button = driver.find_element(By.ID, "logout_sidebar_link")
        logout_button.click()
        print('LogOut success')
        
        driver.quit() # Cierra el navegador
    else:
        print("Login failed")
        driver.quit() # Cierra el navegador


if __name__ == '__main__':
    main()
