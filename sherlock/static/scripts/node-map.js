

// Setup global variables
var nodeMap;
const defaultLineColor = "#444";
const trafficLineColor = "red";
const nodeCache = []
var radius = 500;
var theta = 0;
var graphFit = false;

document.addEventListener('DOMContentLoaded', function () {

    // Get the data injected inside the div #data and parse it as JSON
    const dataNode = document.getElementById("data");

    // Do some hacky clean up
    dataNode.dataset.context = dataNode.dataset.context.replaceAll("'", "\"")

    const data = JSON.parse(dataNode.dataset.context);

    const MY_IP = data.ip
    console.log("host ip address is: " + MY_IP);


  // Clear Graph Button
  const button = document.getElementById('delete-all-button');
  button.addEventListener('click', (e) => {
    fetch('/delete-all')
    .then(res => {
      nodeMap.elements().remove();
    })
  })

  // Start Cytoscape
  nodeMap = window.cy = cytoscape({
    container: document.getElementById('node-map'),
    autounselectify: true,
    maxZoom: 1,
    boxSelectionEnabled: false,
    layout: { name: 'cola' },
    style: [
      {
        selector: 'node',
        style: {
          'label': 'data(label)',
          'color': '#fff',
        }
      },
      {
        selector: 'edge',
        style: {
          'curve-style': 'bezier',
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

  nodeMap.cxtmenu({
    selector: 'node',
    adaptativeNodeSpotlightRadius: false,
    activeFillColor: 'rgba(113, 110, 212, 1)',
    commands: [
      {
        content: 'Copy to clipboard',
        select: function(ele){
          
          let textArea = document.createElement('textarea')
          // ipaddr = nodeMap.$(`[id="${packet.source_ip_address}"]`) 
          let ipaddr = ele.data('id') 
          console.log(typeof ipaddr)
          textArea.value = ipaddr 
          textArea.style.top="0";
          textArea.style.left = "0";
          textArea.style.position = "fixed"
          document.body.appendChild(textArea)
          textArea.focus()
          textArea.select()

          try{
              let successful = document.execCommand('copy')

          }
          catch(err){
              console.error('fallback oops did not copy', err)

          }
          document.body.removeChild(textArea)


        }

      },
      {
        content: 'Get ports',
        select: function(ele){
          window.location.href = ''
        }, 

      },
      {
        content: 'Other host',
        select: function(ele){

          let ipaddr = ele.data('id')
          sessionStorage.setItem('ipaddr', ipaddr);

          let nextPage = "/localpage/".concat(ipaddr);
          $.ajax({
              type: 'GET',
              url: nextPage, 
              data: {
                ajaxip: ipaddr 
              },
              success: function(data) {
                  window.location.href = nextPage;  
              },
              headers: {
                'X-Requested-With': 'XMLHttpRequest'
              }
          }); 
        },
      }

    ]

  });
  //create host
  nodeMap.add(createLocalHost(MY_IP));


  nodeMap.ready((event) => {
    // Start the graph
    console.log("Node map running...")
    initGraph();

    // Connect to the websocket...
    const socket = new WebSocket(
      'ws://'
      + window.location.host
      + '/ws/network-stream'
    );

    // Everytime a websocket sends a message...
    socket.onmessage = function (e) {
      const message = JSON.parse(e.data);
      handleMessage(message)
    };
    // When the socket closes...
    socket.onclose = function (e) {
      console.error('Socket closed unexpectedly');
    };
  })
});


function createEdges(packet) {
  return {
    group: 'edges',
    data: {
      id: createEdgeId(packet),
      source: packet.source_ip_address,
      target: packet.destination_ip_address,
      label: packet.source_port,
    }
  }
}

function handleMessage(message)
{
  const data = JSON.parse(message.message);
  for (index = 0; index < data.length; index++) {
    packet = data[0].fields;
    addPacket(packet);
  }
}

function createNode(id, hostName) {

  if (!nodeCache.includes(id)) {
    // Increment theta
    theta = theta + 5;
    if (theta > 360) {
      theta = 0;
      radius = radius * 1.25;
    }
  }
  return {
    group: 'nodes',
    data: {
      id: id,
      label: hostName ? hostName : id
    },
    position: {
      x: radius * Math.cos(theta),
      y: radius * Math.sin(theta)
    }
  }
}
function createLocalHost(id) {
  return {
    group: 'nodes',
    data: {
      id: id,
      label: 'This Computer'
    },
    position: {
      x: 0,
      y: 0
    },
  }
}


function createEdgeId(packet)
{
  return packet.source_ip_address + "->" + packet.destination_ip_address;
}

// Initialize the graph based on previous data in the database
function initGraph()
{
  console.log("Initializing the node map...")
  // This fetches nodes within 1-minute of our current time (ie. all nodes saved 1 minute ago)
  fetch('/nodes/5', {
    'Content': 'application/json'
  })
  .then(data => data.json())
  .then(jsonData => {
    const packets = jsonData['nodes'];
    packets.forEach(packet => {
      addPacket(packet);
    });
  });
}

function addPacket(packet)
{
  const closeConnectionFlag = packet.fin;
  const sourceIP = packet.source_ip_address;
  const destinationIP = packet.destination_ip_address;
  
  // If the FIN flag has been set, we should remove the node (the connection is closed)
  if (closeConnectionFlag) {
    if (destinationIP != "10.0.2.15" && destinationIP != "127.0.0.1") {
      removeNode(packet, packet.destination_ip_address)
    } 
    if (closeConnectionFlag && sourceIP != "10.0.2.15" && sourceIP != "127.0.0.1") {
      removeNode(packet, packet.source_ip_address)
    }
  } else {

    const sourceNode = nodeMap.$(`[id="${sourceIP}"]`);
    if (sourceNode.length <= 0) {
      nodeMap.add(createNode(sourceIP, packet.source_host_name));
    }

    const destinationNode = nodeMap.$(`[id="${destinationIP}"]`);
    if (destinationNode.length <= 0) {
      nodeMap.add(createNode(destinationIP, packet.destination_host_name));
    }
    
    const edgeId = createEdgeId(packet);
    const edgeNode = nodeMap.$(`[id="${edgeId}"]`)
    if (edgeNode.length <= 0)
    {
      edges = createEdges(packet);
      nodeMap.add(edges);
    }

    nodeCache.push(sourceIP);
    nodeCache.push(destinationIP);
  }
    

  if (!graphFit)
  {
    nodeMap.fit();
    graphFit = true;
  }
  
  edgeId = createEdgeId(packet);
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
}

function removeNode(packet, id)
{
  const node = nodeMap.$(`[id="${id}"]`);
  const nodeEdgeId = createEdgeId(packet);
  const nodeEdge = nodeMap.$(`[id="${nodeEdgeId}"]`);
  
  console.log("Removing node:", id)

  nodeMap.remove(node);
  nodeMap.remove(nodeEdge);

  const index = nodeCache.indexOf(id);
  if (index > -1) {
    nodeCache.splice(index, 1);
  }
}
