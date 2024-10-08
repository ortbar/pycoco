document.addEventListener("DOMContentLoaded", function() {
    // Seleccionamos el formulario de respuesta
    const respuestaForm = document.querySelector('#respuesta-form');
    const nextButton = document.querySelector('#nextButton');  // Botón "Siguiente"
    
    if (respuestaForm) {
        respuestaForm.addEventListener('submit', function(event) {
            event.preventDefault();  // Evitar el envío normal del formulario

            // Obtener la respuesta del input
            const respuesta = document.querySelector('#respuesta').value;

            // Realizar la llamada AJAX para verificar la respuesta
            fetch(`/check_answer/${ match_id }/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf_token,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ 'respuesta': respuesta })
            })
            .then(response => response.json())
            .then(data => {
                // Obtener el div de mensaje donde se mostrará el resultado
                const mensaje = document.querySelector('#mensaje');

                if (data.status === 'correct') {
                    mensaje.textContent = data.message; // Mostrar mensaje de éxito

                    // Actualizar los puntos
                    document.querySelector('#puntos-container').textContent = `Puntos: ${data.points}`;

                    // Reproducir la canción si está disponible
                    if (data.song_url) {
                        const audio = new Audio(data.song_url);
                        audio.play();
                    }

                    // Deshabilitar el campo de respuesta
                    document.querySelector('#respuesta').disabled = true;

                    // Mostrar el botón de siguiente
                    document.querySelector('#nextButton').style.display = 'inline-block';
                } else if (data.status === 'incorrect') {
                    mensaje.textContent = data.message; // Mostrar mensaje de error
                }
            })
            .catch(error => console.error('Error:', error));  // Manejo de errores
        });
    }

    // Manejar el evento click para pasar al siguiente acertijo
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            //al poner el archivo js linkeado de forma externa, ahi que seguir la sintaxis de js y no la sintax de jinja que es como estaba cuando el codigo js estaba incrustado en el game.html.
            fetch(`/next_riddle/${ match_id }/`, { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'next_riddle') {
                    // Actualizar el acertijo con el nuevo acertijo
                    document.querySelector('h2').textContent = data.question;
                    

                    const row = document.querySelector('#row');
                    row.innerHTML = ''; // Vaciar las imágenes anteriores

                    // Verificar si las nuevas imágenes están disponibles y agregarlas
                    if (data.photo) {
                        const imgElement = document.createElement('img');
                        imgElement.src = data.photo;
                        imgElement.alt = 'Imagen 1 del acertijo';
                        imgElement.className = 'img-fluid col-4';
                        row.appendChild(imgElement);
                    }
                    if (data.photo_1) {
                        const imgElement1 = document.createElement('img');
                        imgElement1.src = data.photo_1;
                        imgElement1.alt = 'Imagen 2 del acertijo';
                        imgElement1.className = 'img-fluid col-4';
                        row.appendChild(imgElement1);
                    }
                    if (data.photo_2) {
                        const imgElement2 = document.createElement('img');
                        imgElement2.src = data.photo_2;
                        imgElement2.alt = 'Imagen 3 del acertijo';
                        imgElement2.className = 'img-fluid col-4';
                        row.appendChild(imgElement2);
                    }


                    // Limpiar el mensaje y el campo de respuesta, habilitar el campo de nuevo
                    document.querySelector('#mensaje').textContent = '';
                    document.querySelector('#respuesta').value = '';
                    document.querySelector('#respuesta').disabled = false;

                    // Ocultar el botón "Siguiente"
                    nextButton.style.display = 'none';

                } else if (data.status === 'finished') {
                    document.querySelector('#mensaje').textContent = data.message;
                    nextButton.style.display = 'none';  // Ocultar el botón siguiente si no hay más acertijos
                }
            })
            .catch(error => console.log('Error:', error));
        });
    }
});