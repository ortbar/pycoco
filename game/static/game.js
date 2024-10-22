document.addEventListener("DOMContentLoaded", function() {
    const respuestaForm = document.querySelector('#respuesta-form');
    const nextButton = document.querySelector('#nextButton');  
    
    if (respuestaForm) {
        respuestaForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const respuesta = document.querySelector('#respuesta').value;

            // Hacer la solicitud para comprobar la respuesta
            fetch(`/check_answer/${match_id}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf_token,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({ 'respuesta': respuesta })
            })
            .then(response => response.json())
            .then(data => {
                const mensaje = document.querySelector('#mensaje');

                if (data.status === 'correct') {
                    mensaje.textContent = data.message;

                    // Actualizar puntos en pantalla
                    document.querySelector('#puntos-container').textContent = `Puntos: ${data.points}`;

                    if (data.song_url) {
                        const audio = new Audio(data.song_url);
                        audio.play();
                    }

                    // Deshabilitar el campo de respuesta hasta que se cargue el próximo acertijo
                    document.querySelector('#respuesta').disabled = true;
                    nextButton.style.display = 'inline-block'; // Mostrar el botón "Siguiente"
                } else if (data.status === 'incorrect') {
                    mensaje.textContent = data.message;

                    // Actualizar puntos en pantalla
                    document.querySelector('#puntos-container').textContent = `Puntos: ${data.points}`;

                    // Mostrar el botón "Siguiente" para intentar un nuevo acertijo
                    nextButton.style.display = 'inline-block';
                }
            })
            .catch(error => console.error('Error:', error)); // Manejo de errores
        });
    }

    // Manejo del evento del botón "Siguiente"
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            // Hacer la solicitud para obtener el siguiente acertijo
            fetch(`/next_riddle/${match_id}/`, {
                method: 'GET',
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'next_riddle') {
                    // Actualizar el acertijo y las imágenes
                    document.querySelector('h2').textContent = data.question;

                    const row = document.querySelector('#row');
                    row.innerHTML = ''; // Vaciar las imágenes anteriores

                    // Si hay imágenes nuevas, agregarlas
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

                    // Limpiar el campo de respuesta y habilitarlo nuevamente
                    document.querySelector('#mensaje').textContent = '';
                    document.querySelector('#respuesta').value = '';
                    document.querySelector('#respuesta').disabled = false;

                    // Ocultar el botón "Siguiente"
                    nextButton.style.display = 'none';
                } else if (data.status === 'finished') {
                    // Mostrar mensaje de finalización y puntaje final
                    const acertijoContainer = document.querySelector('#acertijo-container');
                    acertijoContainer.innerHTML = `
                        <div class="text-center">
                            <h3>¡Has completado todos los acertijos!</h3>
                            <p>Tu puntuación final es: ${data.points}</p>
                        </div>
                    `;
                    nextButton.style.display = 'none'; // Ocultar el botón "Siguiente"
                }
            })
            .catch(error => console.error('Error:', error)); // Manejo de errores
        });
    }
});
