window.onload = () => {

    const socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/network-stream'
    );
    
    socket.onmessage = function(e) {
        const message = JSON.parse(e.data);
        const data = JSON.parse(message.message);
        for (index = 0; index < data.length; index++)
        {
            packet = data[0]
            document.querySelector('#table-data').innerHTML += '<tr>' + 
            `<td>${packet.fields.source_ip_address}</td>` +
            `<td>${packet.fields.destination_ip_address}</td>` +
            `<td>${packet.fields.source_port}</td>` +
            `<td>${packet.fields.destination_port}</td>` +
            `<td>${packet.fields.ttl}</td>` +
            `<td>${packet.fields.protocol}</td>` +
            `<td>${packet.fields.sequence_number}</td>` +
            `<td>${packet.fields.payload}</td>` 
            + '</tr>';
        }
    };
    
    socket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
}
