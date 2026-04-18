¿Qué ventajas le proporciona a un proyecto el uso de un pipeline de CI? Menciona al menos tres ventajas específicas y explica por qué son importantes.

1. Versionamiento automático de artefactos: Al versionar nuestros artefactos (e.g., imágenes de Docker), logramos tener un control granular sobre lo que tenemos en producción. Haciendo que deploys y, si es necesario, rollbacks sean fáciles y seguros.  

2. Automatización de pruebas: El CI también nos permite automatizar pruebas a nuestro código, asegurando que todo funcione de manera correcta fuera de nuestra máquina y además podamos asegurar que nuevas features que desarrollemos no dañen cosas que previamente estaban implementadas.

3.  Aumentar la seguridad, mantenibilidad y calidad de nuestro código: Aparte de las pruebas, también podemos implementar escáneres de seguridad como SonarQube para el código y Trivy para la imagen Docker, así como analizadores estáticos de código como ESLint y Flake8. Herramientas que nos ayudarán a mantener nuestro código limpio y seguro. Lo cual a largo plazo es una gran victoria.

¿Cuál es la diferencia principal entre una prueba unitaria y una prueba de aceptación? Da un ejemplo de algo que probarías con una prueba unitaria y algo que verificarías con una prueba de aceptación (en el contexto de cualquier aplicación que conozcas, descríbela primero).

- La diferencia es que las pruebas unitarias se encargan de probar funciones o pedazos aislados de lógica de negocio que componen todo el flujo en general de la aplicación. Mientras que las pruebas de aceptación son de cara al usuario, enfocándose en ver que la lógica de negocio esté entregando el valor esperado. Por ejemplo, en nuestra calculadora, una prueba unitaria se encarga de probar la función individual de la multiplicación y una prueba de aceptación prueba toda la lógica de negocio enfocada en la acción de multiplicar, levantando un browser (headless), haciendo peticiones y asegurándose de que la respuesta de nuestro servicio sea la esperada.

Describe brevemente qué hace cada uno de los steps principales de tu workflow de GitHub Actions (desde el checkout hasta el push de Docker). Explica el propósito de cada uno (qué hace y para qué se hace).

- Checkout: Se encarga de hacer checkout al código de nuestro repositorio, cargándolo en memoria y dejándolo listo para compilar.

- Set up Python: Instalar Python para poder correr nuestro proyecto en nuestra máquina virtual.

- Install dependencies: Se encarga de instalar todas las dependencias de nuestro proyecto; la ejecución de nuestro proyecto depende de estas, así que es mandatorio.

- Black: Correr la dependencia de code formatting Black, formateando nuestro código con reglas estándar de Python para mantener código limpio.

- Pylint: Correr la dependencia de linter Pylint, detectando errores de sintaxis y ejecución. También, para asegurar la calidad del código.

- Flake8: Correr la dependencia de linter Flake8, haciendo algo parecido a Pylint, revisando la calidad del código contra los estándares PEP8.

- Run Unit tests: Corre la dependencia de Pytest con coverage, encargándose de correr de manera automática todas nuestras pruebas, además de revisar el coverage sobre nuestro código. Este step es un blocker; si no pasa, nuestro artefacto no será desplegado.

- Run acceptance tests: Corre nuestro servicio y la dependencia de Selenium para hacer pruebas de aceptación nativamente en la máquina del CI. Encargándose de asegurar que el flujo completo de cara al cliente esté funcionando de manera correcta. También son un bloqueador para nuestro CI.

- Upload Test Reports Artifacts: Sube los reportes HTML y de cobertura como artefactos del workflow, para poder revisarlos sin tener que volver a correr el pipeline.

- SonarCloud Scan: Envía el código y los reportes a SonarQube para medir calidad, code smells, duplicación y cobertura. Es un control adicional más allá de los linters locales.

- QEMU y Docker Buildx: Preparan el runner para construir imágenes Docker multiarquitectura. Solo corren en push a main.

- Login to Docker Hub: Autentica el runner contra Docker Hub usando nuestro token guardado como secreto. Sin esto no podría hacer push al registro.

- Build and push Docker image: Construye la imagen usando el Dockerfile y la sube a Docker Hub con dos tags: el SHA del commit y latest.

Qué problemas o dificultades encontraste al implementar este taller? ¿Cómo los solucionaste? Si no encontraste ningún problema, describe algo nuevo que hayas aprendido.

- En realidad, no tuvimos ningún problema por fuera de los que pasaban en el taller. Pero, haber aprendido de SonarQube nos pareció demasiado interesante, ya que es una herramienta que agrega demasiado valor a la forma en la que desarrollamos código, pudiendo reducir la cantidad de bugs que desplegamos y ayudándonos a no repetirlos nuevamente.

¿Qué ventajas ofrece empaquetar la aplicación en una imagen Docker al final del pipeline en lugar de simplemente validar el código?

- Poder entregar un artefacto validado y probado, el cual puede ser desplegado en la etapa de CD. Asegurando robustez y seguridad.
- Poder versionar y asegurar trazabilidad del artefacto de manera automática. Lo cual nos facilita mucho acciones posteriores en el CD.
