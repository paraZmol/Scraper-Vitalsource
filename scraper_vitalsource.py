import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json # <-- ¡NUEVO! Importamos la biblioteca JSON nativa

# --- CONFIGURACIÓN ---
URL_HOME = "https://full-bookshelf.vitalsource.com/home/explore"
ARCHIVO_SALIDA_CSV = "libros_vitalsource_COMPLETO.csv"
ARCHIVO_SALIDA_JSON = "libros_vitalsource_RESPALDO.json"

# --- FUNCIÓN DE LOGIN (Sin cambios) ---
def esperar_login(driver):
    print("=================================================================")
    print("¡ACCIÓN REQUERIDA!")
    print("Por favor, INICIA SESIÓN manualmente en la ventana de Edge.")
    print("Una vez que estés en la página 'Home' (Explore) después de iniciar sesión,")
    print("vuelve a esta terminal y presiona Enter para continuar.")
    print("=================================================================")
    input("Presiona Enter aquí después de iniciar sesión...")
    
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View All')]")) 
        )
        print("¡Login confirmado!")
        return True
    except Exception as e:
        print(f"Error: No se encontró el botón 'View All'. {e}")
        return False

# --- FUNCIÓN PARA EXTRAER DATOS DEL PANEL (Sin cambios, v6) ---
def extraer_datos_del_panel(driver):
    try:
        panel = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "._panelOuter_1hhj1_1"))
        )
        
        titulo_panel = None
        autor = None
        editorial = "PEARSON" # Valor por defecto
        portada_url = None

        # --- Lógica de Título (Prueba los 3 tipos) ---
        try:
            titulo_panel = panel.find_element(By.CSS_SELECTOR, "a._title_o1x7c_18 h2").text.strip()
        except:
            try:
                titulo_panel = panel.find_element(By.CSS_SELECTOR, "button._title_o1x7c_18 h2").text.strip()
            except:
                try:
                    titulo_panel = panel.find_element(By.CSS_SELECTOR, "div._title_o1x7c_18 h2").text.strip()
                except:
                    print("  > ADVERTENCIA: No se pudo encontrar el TÍTULO.")

        # --- Extracción Independiente ---
        try:
            autor = panel.find_element(By.XPATH, "//dt[text()='Author(s)']/following-sibling::dd[1]").text.strip()
        except:
            print("  > ADVERTENCIA: No se pudo encontrar el AUTOR.")
        
        try:
            editorial = panel.find_element(By.XPATH, "//dt[text()='Publisher']/following-sibling::dd[1]").text.strip()
        except:
            print("  > ADVERTENCIA: No se pudo encontrar la EDITORIAL. Usando 'PEARSON'.")
            
        try:
            portada_url = panel.find_element(By.CSS_SELECTOR, "._container_o1x7c_2 img.vst-book-card-component-image").get_attribute('src')
        except:
            print("  > ADVERTENCIA: No se pudo encontrar la URL de la IMAGEN.")

        # --- Cierre del Panel ---
        panel.find_element(By.CSS_SELECTOR, "button._closeButton_1hhj1_25").click()
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "._panelOuter_1hhj1_1"))
        )
        
        return titulo_panel, autor, portada_url, editorial
    
    except Exception as e:
        print(f"  > Error CRÍTICO procesando el panel: {e}")
        return None, None, None, None

# --- INICIO DEL SCRIPT (Sin cambios) ---

print("Iniciando el navegador Microsoft Edge...")
try:
    service = webdriver.EdgeService() 
    driver = webdriver.Edge(service=service)
except Exception as e:
    print(f"Error al iniciar msedgedriver: {e}"); input("Presiona Enter para salir."); exit()

driver.get(URL_HOME)
driver.maximize_window()

if not esperar_login(driver):
    print("Saliendo del script."); driver.quit(); exit()

libros_data = []
titulos_procesados = set()

print("Navegando a la página 'View All'...")
try:
    view_all_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View All')]"))
    )
    view_all_button.click()
    
    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h2"), "Trending")
    )
    
    contenedores_libros = driver.find_elements(By.CSS_SELECTOR, "div.vst-book-card-auto")
    total_libros = len(contenedores_libros)
    if total_libros == 0: raise Exception("No se encontraron libros")
    print(f"¡Éxito! Se encontraron {total_libros} libros en la página 'Trending'. Empezando el bucle.")

except Exception as e:
    print(f"Error fatal al intentar cargar la página 'View All': {e}")
    driver.quit()
    exit()

# --- BUCLE PRINCIPAL (Sin cambios, v6) ---
i = 0
while i < total_libros:
    print("---------------------------------------------------------")
    print(f"Procesando libro {i+1} de {total_libros}...")
    
    titulo_tarjeta = f"Libro Desconocido #{i+1}" 
    
    try:
        libro_actual = driver.find_elements(By.CSS_SELECTOR, "div.vst-book-card-auto")[i]
        
        titulo_tarjeta_elem = libro_actual.find_element(By.CSS_SELECTOR, "._title_1i967_1")
        titulo_tarjeta = titulo_tarjeta_elem.text.strip()
        
        if titulo_tarjeta in titulos_procesados:
            print(f"  > '{titulo_tarjeta}' ya fue procesado. Saltando.")
            i += 1
            continue
            
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", libro_actual)
        time.sleep(1) 

        three_dot_button = libro_actual.find_element(By.CSS_SELECTOR, 'button.vst-icon-button-circle[aria-label*="More Options"]')
        driver.execute_script("arguments[0].click();", three_dot_button)
        time.sleep(0.5) 

        book_details_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Book Details')]"))
        )
        book_details_button.click()
        
        titulo, autor, portada, editorial = extraer_datos_del_panel(driver)
        
        if titulo or autor or portada:
            titulo_final = titulo if titulo else titulo_tarjeta 
            print(f"  > OK: {titulo_final} - {autor}")
            libros_data.append({
                "N": i + 1, "Libro": titulo_final, "Autor": autor,
                "URL img": portada, "Plataforma": "VITAL SOURCE", "Editorial": editorial
            })
            titulos_procesados.add(titulo_final)
        else:
            print(f"  > ERROR: No se pudieron extraer datos del panel para '{titulo_tarjeta}'.")
            print("  > Se guardará un marcador de error y se saltará al siguiente. NO SE RECARGARÁ.")
            libros_data.append({
                "N": i + 1, "Libro": f"ERROR AL PROCESAR: {titulo_tarjeta}", "Autor": "FALLO",
                "URL img": None, "Plataforma": "VITAL SOURCE", "Editorial": "PEARSON"
            })
            titulos_procesados.add(titulo_tarjeta)

        i += 1 
        time.sleep(1) 

    except Exception as e:
        print(f"  > Error CRÍTICO en el libro {i+1} (ej. no se pudo hacer clic): {e}")
        print(f"  > La página se rompió. Volviendo al 'Home' para reiniciar sesión...")
        
        driver.get(URL_HOME)
        
        if not esperar_login(driver):
            print("El login falló durante la recuperación. Saliendo.")
            break 
            
        try:
            print("  > Volviendo a la página 'View All'...")
            view_all_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View All')]"))
            )
            view_all_button.click()
            WebDriverWait(driver, 20).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "h2"), "Trending")
            )
            
            contenedores_libros = driver.find_elements(By.CSS_SELECTOR, "div.vst-book-card-auto")
            total_libros = len(contenedores_libros)
            print("  > Página recargada. Reintentando el libro que falló...")
        except Exception as e_recarga:
            print(f"  > Fallo catastrófico al recargar. Saliendo. {e_recarga}")
            break

# --- ¡¡FINALIZACIÓN CORREGIDA (CSV y JSON con formato)!! ---
print("=========================================================")
print("Proceso completado. Cerrando el navegador.")
driver.quit()

if libros_data:
    print(f"Guardando {len(libros_data)} libros en los archivos...")
    df = pd.DataFrame(libros_data)
    
    columnas_ordenadas = ["N", "Libro", "Autor", "URL img", "Plataforma", "Editorial"]
    df = df.reindex(columns=columnas_ordenadas) 
    
    # 1. Guardar en CSV (para Excel)
    df.to_csv(ARCHIVO_SALIDA_CSV, index=False, sep=';', encoding='utf-8-sig')
    print(f"¡Éxito! Archivo '{ARCHIVO_SALIDA_CSV}' (Excel) creado.")
    
    # 2. Guardar en JSON (con el formato de espacio correcto)
    try:
        # Convertir el DataFrame a una lista de diccionarios (formato Python)
        data_list = df.to_dict(orient='records')
        
        # Usar la biblioteca 'json' para escribir el archivo
        with open(ARCHIVO_SALIDA_JSON, 'w', encoding='utf-8') as f:
            # indent=4 : Pone los saltos de línea y la sangría
            # ensure_ascii=False : Guarda los acentos (ej. "Enfermería")
            # separators=(',', ': ') : ¡ESTA ES LA CLAVE! Pone el espacio después de los dos puntos.
            json.dump(data_list, f, indent=4, ensure_ascii=False, separators=(',', ': '))
            
        print(f"¡Éxito! Archivo '{ARCHIVO_SALIDA_JSON}' (JSON) creado con el formato correcto.")
        print("\nAhora puedes abrir el archivo .json, copiar su contenido y pegarlo en Word.")
        
    except Exception as e:
        print(f"  > Error al crear el archivo JSON: {e}")

else:
    print("No se pudo extraer ningún libro.")
