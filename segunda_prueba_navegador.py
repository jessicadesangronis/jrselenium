import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_automation():
    """
    Configura Selenium, aplica trucos anti-detección (Modo Sigiloso)
    y realiza una búsqueda en Google.
    """
    
    # 1. Configuración del Driver (Navegador Chrome)
    print("--- Configurando el Driver ---")
    
    # Descarga e instala automáticamente la versión correcta del driver
    service = Service(ChromeDriverManager().install())
    
    options = webdriver.ChromeOptions()
    
    # --- TRUCOS PARA EVITAR LA DETECCIÓN DE GOOGLE (MODO SIGILOSO) ---
    # 1. Quitar la barra que dice "Un software de prueba..."
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 2. Desactivar la bandera interna de "AutomationControlled" (La más importante)
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # 3. Maximizar ventana y User-Agent para simular un usuario real
    options.add_argument("--start-maximized") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    # options.add_argument("--headless") # Descomenta esto si no quieres ver el navegador

    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15) # Aumentamos el tiempo de espera por si acaso

    try:
        print("--- Paso 1: Abriendo Google ---")
        driver.get("https://www.google.com")

        # Esperamos un momento extra para que cualquier popup de cookies cargue
        time.sleep(2) 

        print("--- Paso 2: Buscando 'bandcamp' ---")
        # Buscamos la barra de búsqueda por su atributo name="q"
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys("bandcamp")
        search_box.send_keys(Keys.RETURN) # Simula presionar Enter

        print("--- Paso 3: Haciendo clic en el primer resultado ---")
        # Esperamos a que los resultados (etiquetas h3) sean clickeables
        first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))) 
        first_result.click()
        
        print("--- Esperando carga de la página (8 segundos) ---")
        time.sleep(3) 

        print("--- Paso 4: Tomando captura de pantalla ---")
        filename = "bandcamp_captura.png"
        driver.save_screenshot(filename)
        print(f"¡Éxito! Captura guardada como '{filename}'")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        # Cerramos el navegador al finalizar 
        print("--- Cerrando navegador ---")
        # Le damos un segundo para que veas el resultado antes de cerrar
        time.sleep(1) 
        driver.quit()

if __name__ == "__main__":
    run_automation()