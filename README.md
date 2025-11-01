# Script de Extracción de Libros de PEARSON

Este es un script de Python diseñado para automatizar la extracción de la base de datos de libros de la plataforma **PEARSON**.

El script utiliza **Selenium** para controlar un navegador **Microsoft Edge** real, simulando los pasos que haría un humano para extraer la información de cada libro, superando la carga dinámica de la página.

## 🤖 ¿Qué hace el script?

* Abre una ventana de Edge y pausa, pidiendo al usuario que **inicie sesión manualmente una vez**.
* Una vez confirmado el login, navega a la sección "View All" (Ver Todo) de la categoría "Trending" para cargar la lista completa de libros.
* Inicia un bucle 100% automático que, para cada libro de la lista, realiza lo siguiente:
    1.  Hace *scroll* (se desplaza) hasta que el libro es visible.
    2.  Hace clic en el botón de los tres puntos (`...`).
    3.  Hace clic en el botón "Book Details".
    4.  Espera a que el panel lateral aparezca y extrae el **Título, Autor, Editorial** y la **URL de la imagen**.
    5.  Cierra el panel.
    6.  Continúa con el siguiente libro.
* **Maneja errores:** Está programado para reconocer diferentes tipos de libros ("Disponibles", "Unavailable", "Borrow") y extraer sus datos.
* **Es robusto:** Si falla al extraer un libro, lo marcará en el Excel y continuará con el siguiente. Si la sesión se cierra (un error crítico), pausará y pedirá al usuario que inicie sesión de nuevo, para luego reintentar desde el libro que falló.
* **Guarda todo** automáticamente en dos archivos: `libros_vitalsource_COMPLETO.csv` (para Excel) y `libros_vitalsource_COMPLETO.json` (como respaldo).

---

## ⚙️ Configuración (Solo una vez)

Para que este script funcione en una nueva computadora, se deben seguir estos 3 pasos:

### Paso 1: Instalar los Requisitos

1.  **Instalar Python:**
    * Ten o descarga e instala Python desde [python.org](https://www.python.org/downloads/).
    * **¡MUY IMPORTANTE!** Durante la instalación, asegúrate de marcar la casilla que dice **"Add Python to PATH"**.

3.  **Instalar Bibliotecas:**
    * Abre una terminal o símbolo del sistema (CMD).
    * Ejecuta los siguientes dos comandos (uno por uno):
        ```bash
        pip install selenium
        ```
        ```bash
        pip install pandas
        ```

4.  **Descargar el "Conector" de Edge (msedgedriver):** //** en mi caso uso Edge, pero si usas otro navegador, deberas buscar el conector(WebDriver) correspondiente a ese navegador **//
    * Abre tu navegador **Microsoft Edge** y ve a `Configuración > Ayuda y comentarios > Acerca de Microsoft Edge` para ver tu número de versión (ej: `141.0.3537.99`).
    * Ve a la página oficial de descargas de Microsoft: [developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
    * Busca y descarga el archivo `win64` que coincida **exactamente** con tu versión de Edge.
    * Descomprime el `.zip` y obtendrás un archivo llamado `msedgedriver.exe`.

### Paso 2: Preparar la Carpeta

1.  Crea una carpeta en tu computadora (ej. `C:\Scraper`).
2.  Coloca **dos archivos** dentro de esa carpeta:
    * `scraper_vitalsource.py` (este script).
    * `msedgedriver.exe` (el conector que acabas de descargar).

Tu carpeta debe verse así:
* Mi_Carpeta_Scraper
*    |- scraper_vitalsource.py
*    |- msedgedriver.exe

### Paso 3: Ejecutar el Script (pasos de como se usa el scrit y que debes de hacer)

1.  Abre una terminal (CMD o la terminal de VS Code).
2.  Navega a tu carpeta usando el comando `cd`:
    ```bash
    cd C:\Scraper
    ```
3.  Ejecuta el script escribiendo:
    ```bash
    python scraper_vitalsource.py
    ```
4.  **Inicio de Sesión (Manual, deberas iniciar sesion ocn tu correo institucional):**
    * El script abrirá una ventana de Edge. Ve a esa ventana e **inicia sesión** con tu cuenta.
    * Una vez que estés dentro(tendras que esperar a que termine de cargar la pagina y verificar que estas en la opcion de **Explore**, solo entonces podras continuar) y veas la página "Home" (Explore),         regresa a la terminal.
5.  **Confirmación:**
    * Presiona **Enter** en la terminal.
6.  **¡Dejar Correr!**
    * ¡Listo! El script tomará el control y empezará a procesar todos los libros uno por uno. Este proceso es lento (puede tardar 30-40 segundos por libro), así que déjalo trabajando solo.
    * Si la sesión se cierra, la terminal te pedirá que inicies sesión de nuevo (Paso 4). /* es aca donde falta cubrir algunos errores en el script, asi que de preferencia evita los errores o mejora el          codigo y/o script */
7.  **Finalización:**
    * Cuando termine, la ventana de Edge se cerrará sola y encontrarás tus archivos `libros_vitalsource_COMPLETO.csv` y `libros_vitalsource_COMPLETO.json` en la misma carpeta.
