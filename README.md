# Juego de Acertijos

Este proyecto es una aplicación web para un juego de acertijos, en el que los usuarios pueden resolver preguntas y adivinanzas para ganar puntos. La aplicación está desarrollada utilizando tecnologías como Django, JavaScript y Bootstrap para ofrecer una experiencia interactiva y dinámica.

## Funcionalidades

- **Registro e inicio de sesión:** Los usuarios pueden registrarse y autenticarse para participar en el juego.
- **Sistema de partidas:** Cada jugador puede participar en partidas de un juego específico, con la posibilidad de retomar partidas no terminadas.
- **Adivinanzas con imágenes:** Los acertijos pueden incluir texto y hasta tres imágenes para hacer el juego más interesante.
- **Puntuación:** Los jugadores ganan puntos por respuestas correctas y pierden puntos por respuestas incorrectas.
- **Audio de recompensa:** Cuando se responde correctamente, puede sonar una canción asociada con el acertijo.
- **Gestión de estados del juego:** La aplicación mantiene el estado de la partida y los acertijos, incluyendo los puntos acumulados y si el acertijo ha sido resuelto o no.

## Tecnologías Utilizadas

- **Django:** Framework web de Python que se utiliza para manejar el backend, la lógica de negocio y la comunicación con la base de datos.
- **JavaScript (AJAX):** Utilizado en el frontend para manejar las interacciones de la página sin recargarla, como la comprobación de respuestas y la carga de los siguientes acertijos.
- **Bootstrap:** Framework de CSS que ayuda a crear una interfaz de usuario responsiva y atractiva.
- **HTML y CSS:** Para la estructura y el diseño de las vistas del juego.
- **SQLite:** Base de datos utilizada para el almacenamiento de datos en el entorno de desarrollo. Puede ser reemplazada por otra base de datos relacional como PostgreSQL o MySQL en producción.

## Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/juego-de-acertijos.git
   cd juego-de-acertijos
