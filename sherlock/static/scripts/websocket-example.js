window.onload = () => {

    const socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/network-stream'
    );
    
    console.log("Hello world");
    
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        document.querySelector('#data').innerHTML += (data.message + '\n');
    };
    
    socket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
}
