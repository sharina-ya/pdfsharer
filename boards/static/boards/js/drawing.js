document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    // Настройки по умолчанию
    let currentColor = '#000000';
    let brushSize = 3;

    // Элементы управления
    const colorPicker = document.getElementById('colorPicker');
    const brushSizeControl = document.getElementById('brushSize');

    // Инициализация холста
    function initCanvas() {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
        ctx.strokeStyle = currentColor;
        ctx.lineWidth = brushSize;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
    }

    // Обработчики рисования
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    // Инструменты
    colorPicker.addEventListener('input', function() {
        currentColor = this.value;
        ctx.strokeStyle = currentColor;
    });

    brushSizeControl.addEventListener('input', function() {
        brushSize = this.value;
        ctx.lineWidth = brushSize;
    });

    document.getElementById('clearBtn').addEventListener('click', clearCanvas);
    document.getElementById('saveBtn').addEventListener('click', saveDrawing);

    // Функции
    function startDrawing(e) {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    }

    function draw(e) {
        if (!isDrawing) return;

        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();

        [lastX, lastY] = [e.offsetX, e.offsetY];
    }

    function stopDrawing() {
        isDrawing = false;
    }

    function clearCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    async function saveDrawing() {
        const drawingData = canvas.toDataURL('image/png');
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
                alert('Рисунок успешно сохранен!');
            }
        } catch (error) {
            console.error('Ошибка сохранения:', error);
            alert('Ошибка при сохранении рисунка');
        }
    }

    // Инициализация
    initCanvas();
    window.addEventListener('resize', initCanvas);
});
