from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# 1. Configurar el navegador (Chrome en este caso)
# Selenium 4 suele descargar el driver automáticamente, no necesitas configurarlo manual.
driver = webdriver.Chrome()

# 2. Decirle a dónde ir
driver.get("https://www.google.com")

# 3. Imprimir el título de la página en la consola
print("El título de la página es: " + driver.title)

# 4. Esperar 5 segundos para que puedas verlo (si no, se cierra muy rápido)
time.sleep(5)

# 5. Cerrar el navegador (buena práctica)
driver.quit()