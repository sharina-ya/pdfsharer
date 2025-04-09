document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    function setupCanvas() {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
    }


    canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    });


    canvas.addEventListener('mousemove', (e) => {
        if (!isDrawing) return;

        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();

        [lastX, lastY] = [e.offsetX, e.offsetY];
    });


    canvas.addEventListener('mouseup', () => isDrawing = false);
    canvas.addEventListener('mouseout', () => isDrawing = false);


    document.getElementById('clearBtn').addEventListener('click', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });


    document.getElementById('saveBtn').addEventListener('click', async function() {
        const canvas = document.getElementById('drawingCanvas');
        const drawingData = canvas.toDataURL();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch('', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `drawing_data=${encodeURIComponent(drawingData)}`
            });

            if (response.ok) {
                alert('Рисунок сохранен!');
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    });

    setupCanvas();
    window.addEventListener('resize', setupCanvas);
});