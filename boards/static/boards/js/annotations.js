// Подключение к WebSocket
const socket = new WebSocket(
    `ws://${window.location.host}/ws/board/${boardId}/`
);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    drawAnnotation(data);
};

// При создании аннотации отправляем через WebSocket
function sendAnnotation(data) {
    socket.send(JSON.stringify(data));
}