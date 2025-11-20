import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def run_automation():
    # 1. Configuración del Driver (Navegador)
    # ChromeDriverManager descarga e instala automáticamente la versión correcta del driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Descomenta esto si no quieres ver el navegador abrirse
    
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10) # Tiempo de espera explícito de hasta 10 segundos

    try:
        print("--- Paso 1: Abriendo Google ---")
        driver.get("https://www.google.com")

        # Nota: Si estás en Europa o cierta región, aquí podría aparecer un popup de cookies.
        # Este script asume que vas directo a la búsqueda.

        print("--- Paso 2: Buscando 'bandcamp' ---")
        # Buscamos la barra de búsqueda por su atributo name="q"
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys("bandcamp")
        search_box.send_keys(Keys.RETURN) # Simula presionar Enter

        print("--- Paso 3: Haciendo clic en el primer resultado ---")
        # Esperamos a que los resultados (etiquetas h3) sean clickeables
        # Google suele poner los títulos de los resultados en etiquetas <h3>
        first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h3")))
        first_result.click()

        print("--- Esperando carga de la página ---")
        # Esperamos un poco para asegurar que la página cargue visualmente antes de la foto
        time.sleep(3) 

        print("--- Paso 4: Tomando captura de pantalla ---")
        filename = "bandcamp_captura.png"
        driver.save_screenshot(filename)
        print(f"¡Éxito! Captura guardada como '{filename}'")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        # Cerramos el navegador al finalizar (importante para no dejar procesos abiertos)
        print("--- Cerrando navegador ---")
        driver.quit()

if __name__ == "__main__":
    run_automation()