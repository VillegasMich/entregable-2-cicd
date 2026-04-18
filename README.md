# entregable-2-cicd

Aplicación Flask (calculadora web simple) con un pipeline de CI/CD en GitHub Actions que corre linters, pruebas unitarias y de aceptación, análisis de calidad en SonarQube, y finalmente construye y publica la imagen Docker.

---

## 1. Ventajas de usar un pipeline de CI

Después de varios semestres entregando proyectos "a mano" (subir un zip, compilar en la máquina del profesor, rezar), tener un pipeline de CI cambia bastante la dinámica. Las tres ventajas que más me han servido en este taller son:

1. **Detección temprana de errores.** Cada vez que hago `push` a `main` o abro un PR, el pipeline corre los linters (Black, Pylint, Flake8) y las pruebas. Esto significa que un error de formato, un import mal puesto o un test roto se detectan en minutos, no cuando el profesor intenta correr el proyecto. Es importante porque el costo de arreglar un bug crece mucho mientras más tarde se descubre.

2. **Reproducibilidad y entorno consistente.** El workflow siempre corre sobre `ubuntu-latest` con Python 3.12 fijo e instala dependencias desde `requirements.txt`. Evita el clásico "en mi máquina sí funciona": si pasa en el runner, va a pasar en el de cualquiera. Es clave cuando se trabaja en equipo o cuando alguien revisa tu código semanas después.

3. **Automatización del flujo de entrega.** Una vez que las pruebas pasan, el pipeline construye la imagen Docker y la publica en Docker Hub sin intervención manual. No hay pasos que se me olviden ni comandos que se me escapen. Esto libera tiempo para concentrarme en programar y reduce muchísimo la probabilidad de un error humano en el despliegue.

---

## 2. Diferencia entre prueba unitaria y prueba de aceptación

**La aplicación:** es una calculadora web hecha en Flask. Tiene un formulario en `/` donde el usuario escribe dos números, elige una operación (sumar, restar, multiplicar, dividir) y la app devuelve el resultado en la misma página. La lógica matemática vive en `app/calculadora.py` y la capa web en `app/app.py`.

**Diferencia principal:** una **prueba unitaria** valida una pieza aislada del código (una función, un método) sin depender de infraestructura externa. Una **prueba de aceptación** valida el sistema completo funcionando de punta a punta, tal como lo usaría un usuario real, normalmente atravesando la red, la UI o varios componentes a la vez.

- **Ejemplo unitario:** probar directamente la función `dividir(10, 2)` y verificar que retorna `5.0`, o que `dividir(5, 0)` lanza `ZeroDivisionError`. No arranca ningún servidor, solo importa la función y la ejecuta.
- **Ejemplo de aceptación:** levantar el servidor con Gunicorn, hacer una petición HTTP `POST /` con los campos `num1=10`, `num2=2`, `operacion=sumar`, y verificar que la respuesta HTML contiene `12`. Aquí se está probando que Flask, las rutas, los templates y la lógica hablan bien entre sí.

En el pipeline se reflejan esos dos tipos: primero corre `pytest` ignorando el archivo de aceptación, y después levanta Gunicorn y corre específicamente `tests/test_acceptance_app.py`.

---

## 3. Steps principales del workflow

El workflow `.github/workflows/ci.yml` hace lo siguiente:

1. **`actions/checkout@v3`** — descarga el código del repo en el runner. Sin este paso el runner no tendría nada que compilar ni probar.
2. **`Set up Python`** — instala Python 3.12 en el runner. Fija la versión para garantizar consistencia entre local y CI.
3. **`Install dependencies`** — actualiza `pip` e instala todo lo listado en `requirements.txt` (Flask, Gunicorn, pytest, linters, etc.). Prepara el entorno para los pasos siguientes.
4. **`Run Black`** — verifica el formato del código con `--check`. Si algo no cumple el estilo, falla el step. Así todos los commits mantienen el mismo estilo.
5. **`Run Pylint`** — analiza la calidad del código y exige una nota mínima de 9. Deja el reporte en `pylint-report.txt` para que SonarQube lo use después.
6. **`Run Flake8`** — linter adicional que detecta errores de estilo/bugs potenciales y genera `flake8-report.txt`.
7. **`Run Unit Tests with pytest and Coverage`** — corre las pruebas unitarias (ignorando las de aceptación) y mide cobertura. Valida la lógica interna antes de probar el sistema completo.
8. **`Run Acceptance Tests`** — arranca el servidor con Gunicorn en `0.0.0.0:8000`, espera 10 segundos a que suba, y lanza las pruebas de aceptación contra `http://localhost:8000`. Simula el uso real de la app.
9. **`Upload Test Reports Artifacts`** — sube los reportes HTML y de cobertura como artefactos del workflow, para poder revisarlos sin tener que volver a correr el pipeline.
10. **`SonarCloud Scan`** — envía el código y los reportes a SonarQube para medir calidad, code smells, duplicación y cobertura. Es un control adicional más allá de los linters locales.
11. **`Set up QEMU` y `Set up Docker Buildx`** — preparan el runner para construir imágenes Docker multi-arquitectura. Solo corren en `push` a `main`.
12. **`Login to Docker Hub`** — autentica el runner contra Docker Hub usando un token guardado como secreto. Sin esto no podría hacer `push` al registro.
13. **`Build and push Docker image`** — construye la imagen usando el `Dockerfile` y la sube a Docker Hub con dos tags: el SHA del commit (para trazabilidad exacta) y `latest` (para referencia cómoda). Aprovecha caché GHA para acelerar builds siguientes.

---

## 4. Problemas que encontré y cómo los solucioné

Estos fueron los más representativos:

- **Pruebas de aceptación que no encontraban el servidor.** Al principio Gunicorn se quedaba escuchando en `127.0.0.1` y las pruebas fallaban intermitentemente. La solución fue bindearlo a `0.0.0.0:8000` y exportar `APP_BASE_URL=http://localhost:8000` como variable de entorno, para que el test y el servidor hablaran en la misma interfaz. También tuve que añadir un `sleep 10` para darle tiempo a Gunicorn de estar listo antes de disparar las requests.

- **Errores de SonarQube por duplicación y formato.** Los primeros escaneos salían con code smells y warnings que Black y Pylint no atrapaban localmente. Tocó refactorizar (por ejemplo, el diccionario `OPERACIONES` en `app.py` reemplazó una cadena de `if/elif`) y reformatear con Black hasta que Sonar quedara verde. De ahí aprendí que los linters locales son un mínimo, no un techo.

- **Flake8 vs Black en longitud de línea.** Tuvieron choques de reglas (Black permite más caracteres que el default de Flake8). Lo resolví dejando que Flake8 no bloqueara el pipeline (`|| true`) mientras ajustaba los límites, y luego corrigiendo las líneas realmente problemáticas.

- **Secretos y variables en GitHub Actions.** La primera vez que configuré el `docker/login-action` usé `${{ secrets.DOCKERHUB_USERNAME }}` cuando en realidad tenía el usuario como *variable* (`vars.DOCKERHUB_USERNAME`) y el token sí como *secret*. Entender la diferencia entre `secrets` y `vars` fue algo nuevo que me llevé del taller.

---

## 5. Ventajas de empaquetar en una imagen Docker al final del pipeline

Validar el código está muy bien, pero una imagen Docker da un salto cualitativo:

- **Portabilidad real.** La imagen incluye Python 3.12, todas las dependencias y el código listo para correr con Gunicorn. Cualquiera con Docker instalado puede ejecutar `docker run` y tener la app funcionando, sin instalar nada más ni lidiar con versiones.
- **Entorno idéntico en dev, CI y producción.** El mismo artefacto que pasó las pruebas es el que se despliega. Se elimina la brecha entre "el código compila" y "el código corre en el servidor".
- **Versionado y trazabilidad.** Al taggear la imagen con el SHA del commit (`:${{ github.sha }}`), cada build es identificable y reversible: si una versión rompe algo, se puede volver a una imagen anterior en segundos.
- **Despliegue listo, no solo código validado.** Sin Docker, el pipeline solo garantiza que el código pasa los tests; con Docker, el pipeline entrega un producto desplegable. La CI se convierte en CD.
- **Aislamiento y seguridad.** El contenedor corre con sus propias dependencias, sin contaminar ni depender del host. Si mañana cambio la versión de Python, no afecta a otros servicios en el mismo servidor.

En resumen: validar el código responde "¿está bien escrito?"; empaquetarlo en Docker responde "¿está listo para que cualquiera lo use?".
