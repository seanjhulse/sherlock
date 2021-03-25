
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
      nodeId = null;

      for (index = 0; index < data.length; index++) {
        packet = data[0]
        nodeId = createEdgeId(packet);
        nodes = createNodes(packet);
        edges = createEdges(packet);
        nodeCache.push(packet.fields.source_ip_address);
        nodeCache.push(packet.fields.destination_ip_address);
        graph.push(...nodes);
        graph.push(edges);
      }

      console.log(graph);
      nodeMap.add(graph);

      if (!isGraphCentered) {
        nodeMap.fit();
        isGraphCentered = true;
      }
      
      if (nodeId != null)
      {
        var node = nodeMap.getElementById(nodeId);
        node.animate({
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

function createNodes(packet) {
  return [
    createNode(packet.fields.source_ip_address),
    createNode(packet.fields.destination_ip_address)
  ]
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

  console.log(theta);

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