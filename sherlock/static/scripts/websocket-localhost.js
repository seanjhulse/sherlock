
window.onload = () => {
    const socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/network-stream'
    );
    socket.onmessage = (e) => {
        const message = JSON.parse(e.data)
        const data = JSON.parse(message.message);
        packet = data[0];
        document.querySelector('#info').innerHTML =  
        `<p>${packet.fields.source_ip_address}</p>`;
    }
    socket.onclose = (e) => {
        console.error('Chat socket closed unexpectedly');
    }
}
