document.addEventListener("DOMContentLoaded", function() {
    const respuestaForm = document.querySelector('#respuesta-form');
    const nextButton = document.querySelector('#nextButton');  
    
    if (respuestaForm) {
        respuestaForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const respuesta = document.querySelector('#respuesta').value;

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
                    console.log("Puntos recibidos (correct):", data.points);  // <-- Verificamos los puntos
                    document.querySelector('#puntos-container').textContent = `Puntos: ${data.points}`;

                    if (data.song_url) {
                        const audio = new Audio(data.song_url);
                        audio.play();
                    }

                    document.querySelector('#respuesta').disabled = true;
                    document.querySelector('#nextButton').style.display = 'inline-block';
                } else if (data.status === 'incorrect') {
                    mensaje.textContent = data.message;

                    // Asegurarse de que el contenedor de puntos se actualice correctamente
                    console.log("Puntos recibidos (incorrect):", data.points);  // <-- Verificamos los puntos
                    document.querySelector('#puntos-container').textContent = `Puntos: ${data.points}`;

                    // Mostrar el botón de siguiente
                    document.querySelector('#nextButton').style.display = 'inline-block';
                }
            })
            .catch(error => console.error('Error:', error));  // Manejo de errores
        });
    }

    // Evento para el botón "Siguiente"
    if (nextButton) {
        nextButton.addEventListener('click', function() {
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
                    // Si no hay más acertijos, mostrar mensaje de finalización
                    document.querySelector('#mensaje').textContent = data.message;
                    nextButton.style.display = 'none';  // Ocultar el botón siguiente si se ha terminado
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});
