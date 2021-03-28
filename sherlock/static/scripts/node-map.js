
const defaultLineColor = "#444";
const trafficLineColor = "red";

document.addEventListener('DOMContentLoaded', function () {

  const nodeMap = window.cy = cytoscape({
    container: document.getElementById('node-map'),
    autounselectify: true,
    maxZoom: 10,
    boxSelectionEnabled: false,
    layout: { name: 'cola' },
    style: [
      {
        selector: 'node',
        style: {
          'label': 'data(id)',
          'color': '#fff',
        }
      },
      {
        selector: 'edge',
        style: {
          'label': 'data(label)',
          'color': '#fff',
        }
      }
    ],
    elements: {
      nodes: [],
      edges: []
    }
  });


  nodeMap.ready((event) => {
    console.log("Node map running...")
    var isGraphCentered = false;

    // Connect to the websocket
    const socket = new WebSocket(
      'ws://'
      + window.location.host
      + '/ws/network-stream'
    );

    // Everytime a websocket sends a message...
    socket.onmessage = function (e) {
      const message = JSON.parse(e.data);
      const data = JSON.parse(message.message);

      // Contains our nodes AND our edges 
      graph = [];
      edgeId = null;

      for (index = 0; index < data.length; index++) {
        packet = data[0];

        // console.log(packet);

        const closeConnectionFlag = packet.fields.fin;
        const sourceIP = packet.fields.source_ip_address;
        const destinationIP = packet.fields.destination_ip_address;
        
        // If the FIN flag has been set, we should remove the node (the connection is closed)
        if (closeConnectionFlag) {
          if (destinationIP != "10.0.2.15" && destinationIP != "127.0.0.1") {
            const node = nodeMap.$(`[id="${destinationIP}"]`);
            const nodeEdgeId = createEdgeId(packet);
            const nodeEdge = nodeMap.$(`[id="${nodeEdgeId}"]`);
            console.log("Removing node:", destinationIP)
            nodeMap.remove(node);
            nodeMap.remove(nodeEdge);
            nodeCache.push(destinationIP);
          } 
          if (closeConnectionFlag && sourceIP != "10.0.2.15" && sourceIP != "127.0.0.1") {
            const node = nodeMap.$(`[id="${sourceIP}"]`);
            const nodeEdgeId = createEdgeId(packet);
            const nodeEdge = nodeMap.$(`[id="${nodeEdgeId}"]`);
            console.log("Removing node:", sourceIP)
            nodeMap.remove(node);
            nodeMap.remove(nodeEdge);
            nodeCache.push(sourceIP);
          }
        } else {
          edgeId = createEdgeId(packet);
          edges = createEdges(packet);

          const sourceNode = nodeMap.$(`[id="${sourceIP}"]`);
          const destinationNode = nodeMap.$(`[id="${destinationIP}"]`);
          if (sourceNode.length <= 0) {
            graph.push(createNode(sourceIP));
          }
          if (destinationNode.length <= 0) {
            graph.push(createNode(destinationIP));
          }
          
          graph.push(edges);

          nodeCache.push(sourceIP);
          nodeCache.push(destinationIP);
        }
      }

      // If we have more than 0 elements to add
      if (graph.length > 0){
        nodeMap.add(graph);
      }

      if (!isGraphCentered) {
        nodeMap.fit();
        isGraphCentered = true;
      }
      
      if (edgeId != null)
      {
        var edge = nodeMap.getElementById(edgeId);
        edge.animate({
          style: {
            lineColor: trafficLineColor
          },
          duration: 600,
          easing: 'ease-in-sine'
        }).animate({
          style: {
            lineColor: defaultLineColor
          },
          duration: 600,
          easing: 'ease-out-sine'
      });
      }

    };

    socket.onclose = function (e) {
      console.error('Socket closed unexpectedly');
    };
  })

});

// Setup global variables for our concentric circles
var radius = 500;
var theta = 0;
const nodeCache = []

function createEdges(packet) {
  return {
    group: 'edges',
    data: {
      id: createEdgeId(packet),
      source: packet.fields.source_ip_address,
      target: packet.fields.destination_ip_address,
      label: packet.fields.source_port,
    }
  }
}


function createNode(id) {

  if (!nodeCache.includes(id)) {
    // Increment theta
    theta = theta + 20;
    if (theta > 360) {
      theta = 0;
      radius = radius * 1.25;
    }
  }

  return {
    group: 'nodes',
    data: {
      id: id,
    },
    position: {
      x: radius * Math.cos(theta),
      y: radius * Math.sin(theta)
    }
  }
}

function createEdgeId(packet)
{
  return packet.fields.source_ip_address + "->" + packet.fields.destination_ip_address;
}