// Setup global variables
var nodeMap;
const defaultLineColor = "#444";
var graphFit = false;
var trafficLineColor = "red";
var unique = [];
var MY_SYSTEM;
var trafficColors = ['green', 'blue', 'yellow', 'orange','purple','red']
const COLOR_COUNT = trafficColors.length-1;

const layoutOptions = {
  autounselectify: true,
  avoidOverlap: true,
  animate: true,
  maxSimulationTime: 4000,
  refresh: 1,
  nodeDimensionsIncludeLabels: true,
  boxSelectionEnabled: false,
  randomize: false,
  nodeSpacing: function( node ){ return 50; },
};

var MY_IP = '10.0.2.15';

// Prepare an empty logger instance
let LOGGER;

document.addEventListener('DOMContentLoaded', function () {

    // Create a logger instance
    LOGGER = new Logs();

    // Get the data injected inside the div #data and parse it as JSON
    const dataNode = document.getElementById("data");

    // Do some hacky clean up
    dataNode.dataset.context = dataNode.dataset.context.replaceAll("'", "\"")

    const data = JSON.parse(dataNode.dataset.context);

    MY_IP = data.ip
    console.log("host ip address is: " + MY_IP);
    MY_SYSTEM = data.os;


  // Clear Graph Button
  const button = document.getElementById('delete-all-button');
  button.addEventListener('click', (e) => {
    fetch('/delete-all')
    .then(res => {
      nodeMap.elements().remove();
      createLocalHost(MY_IP);
    })
  })

  // Start Cytoscape
  nodeMap = window.cy = cytoscape({
    container: document.getElementById('node-map'),
    layout: { name: 'cola', ...layoutOptions },
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
          let ipaddr = ele.data('id');
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
        content: 'Watch network traffic',
        select: function(ele){
          let ipaddr = ele.data('id')
          const logsTitle = document.getElementById('network-logs-ip-address');
          logsTitle.innerText = ipaddr;
          LOGGER.setVisibility(true);
          LOGGER.setIp(ipaddr);
        }, 

      },
      {
        content: 'Get ports',
        select: function(ele){
          let ipaddr = ele.data('id')
          sessionStorage.setItem('ipaddr', ipaddr);
          window.open("/portpage/", '_blank').focus();
        }, 

      },
      {
        content: 'Get other hosts',
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
  //context menu for ports
  //inspect connection details (pop up closable menu with connection data)
  //block port via uncomplicated firewall
  //block connection by IP

    nodeMap.cxtmenu({
    selector: 'edge',
    adaptativeNodeSpotlightRadius: false,
    activeFillColor: 'rgba(113, 110, 212, 1)',
    commands: [
      {
        content: 'Inspect Connection',
        select: function(ele){

        edgeLabel = ele.data('id') ;
        sourceIP = ele.data('source');
        targetIP = ele.data('target');
        edgePort = ele.data('label');
        edgeProtocol = ele.data('protocol');
        console.log(edgeLabel, sourceIP, targetIP, edgePort, edgeProtocol)
        createInspectionDiv(edgeLabel, sourceIP, targetIP, edgeProtocol, edgePort);
        }
      },
      {
        content: 'Block Port',
        select: function(ele){

            sourceIP = ele.data('source');
            targetIP = ele.data('target');
            edgePort = ele.data('label');

            blockType =  (targetIP==MY_IP) ? "out" : "in";
            blockTarget = edgePort;

            scriptURL = '/block-connection/' + blockType + '/' + blockTarget + '/'

            $(function(scriptURL) {
                console.log("hit " + scriptURL)
                $('#urlLoader').load(scriptURL);
            }(scriptURL));
        }
      },
      {
        content: 'Block Host',
        select: function(ele){

            sourceIP = ele.data('source');
            targetIP = ele.data('target');
            edgePort = ele.data('label');

            blockType =  "host";
            blockTarget = (targetIP==MY_IP) ? sourceIP : targetIP;

            scriptURL = '/block-connection/' + blockType + '/' + blockTarget + '/'

            $(function(scriptURL) {
                console.log("hit " + scriptURL)
                $('#urlLoader').load(scriptURL);
            }(scriptURL));
        }
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
      handleMessage(message);

      if (graphFit)
      {
        const map = nodeMap.layout({name: 'cola', ...layoutOptions, fit: false});
        map.run();
      } else {
        const map = nodeMap.layout({name: 'cola', ...layoutOptions, fit: true});
        map.run();
        graphFit = true;
      }

    };
    // When the socket closes...
    socket.onclose = function (e) {
      console.error('Socket closed unexpectedly');
    };
  })
});

function createEdge(source, target, port, protocol) {
  return {
    group: 'edges',
    data: {
      id: source + '->' + target,
      source: source,
      target: target,
      label: port,
      protocol: protocol,
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

function createNode(id) {
  var NODE_SYSTEM = 'default';
  return {
    group: 'nodes',
    data: {
      id: id,
      label: id
    },
    position: {
      x: 0,
      y: 0,
    },
    style: {
          shape: 'roundrectangle',
          width:65,
          height: 65, 
          'background-image': '../../static/images/newdefaulticon.png',
          'background-color': '#F9F9F9'
          
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
    style: {
        shape: 'roundrectangle',
         width: 100,
         height: 100,
        'background-image': getIcon(MY_SYSTEM),
        'background-color': '#F9F9F9',
    }
  }
}

function createEdgeId(packet) {
  return packet.source_ip_address + "->" + packet.destination_ip_address;
}

// Initialize the graph based on previous data in the database
function initGraph() {
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

function addPacket(packet) {
  const closeConnectionFlag = packet.flags === "FIN";
  const sourceIP = packet.source_ip_address;
  const destinationIP = packet.destination_ip_address;
  const protocol = packet.protocol;

  const loggerIP = LOGGER.getIp();
  // Add packet to the logger
  if (sourceIP === loggerIP || destinationIP === loggerIP) {
    LOGGER.addPacket(packet);
  }

  // If the FIN flag has been set, we should remove the node (the connection is closed)
  if (closeConnectionFlag) {
    if (destinationIP != "10.0.2.15" && destinationIP != "127.0.0.1") {
      removeNode(packet, packet.destination_ip_address)
    } 
    if (closeConnectionFlag && sourceIP != "10.0.2.15" && sourceIP != "127.0.0.1") {
      removeNode(packet, packet.source_ip_address)
    }
  } else {

    // Create the source and destination nodes
    const sourceNode = nodeMap.$(`[id="${sourceIP}"]`);
    if (sourceNode.length <= 0) {
      nodeMap.add(createNode(sourceIP));
    }
    const destinationNode = nodeMap.$(`[id="${destinationIP}"]`);
    if (destinationNode.length <= 0) {
      nodeMap.add(createNode(destinationIP));
    }
    const port = packet.source_port ? packet.source_port : packet.destination_port;

    // Create the intermediary nodes (if they exist)
    const sourceHostName = domainFromUrl(packet.source_host_name);
    const destinationHostName = domainFromUrl(packet.destination_host_name);
   
    if(port == "443"){

        colorNode(sourceNode, 'green')
    }
    else if(port == "80"){
      colorNode(sourceNode, 'red')
    }
    const sourceHostNode = nodeMap.$(`[id="${sourceHostName}"]`);
    const destinationHostNode = nodeMap.$(`[id="${destinationHostName}"]`);
    if (sourceHostName !== undefined && sourceHostName !== 'undefined' && sourceHostNode.length <= 0) {
      nodeMap.add(createNode(sourceHostName));
      
      // Edge from source -> intermediary
      var edgeNode = nodeMap.$(`[id="${packet.source_ip_address + '->' + sourceHostName}"]`)
      if (edgeNode.length <= 0)
      {
        edges = createEdge(packet.source_ip_address, sourceHostName, port, protocol);
        nodeMap.add(edges);
      }

      // Edge from intermediary -> end
      edgeNode = nodeMap.$(`[id="${sourceHostName + '->' + packet.destination_ip_address}"]`)
      if (edgeNode.length <= 0)
      {
        edges = createEdge(sourceHostName, packet.destination_ip_address, port, protocol);
        nodeMap.add(edges);
      }
    } else if (destinationHostName !== undefined && destinationHostName !== 'undefined' && destinationHostNode.length <= 0) {
      nodeMap.add(createNode(destinationHostName));
      
      // Edge from source -> intermediary
      var edgeNode = nodeMap.$(`[id="${packet.source_ip_address + '->' + destinationHostName}"]`)
      if (edgeNode.length <= 0)
      {
        edges = createEdge(packet.source_ip_address, destinationHostName, port, protocol);
        nodeMap.add(edges);
      }

      // Edge from intermediary -> end
      edgeNode = nodeMap.$(`[id="${destinationHostName + '->' + packet.destination_ip_address}"]`)
      if (edgeNode.length <= 0)
      {
        edges = createEdge(destinationHostName, packet.destination_ip_address, port, protocol);
        nodeMap.add(edges);
      }
    } else {
      // Edge from source -> intermediary
      var edgeNode = nodeMap.$(`[id="${packet.source_ip_address + '->' + packet.destination_ip_address}"]`)
      if (edgeNode.length <= 0)
      {
        edges = createEdge(packet.source_ip_address, packet.destination_ip_address, port, protocol);
        nodeMap.add(edges);
      }

      // Edge from intermediary -> end
      // edgeNode = nodeMap.$(`[id="${uniqueNodeName + '->' + packet.destination_ip_address}"]`)
      // if (edgeNode.length <= 0)
      // {
      //   edges = createEdge(uniqueNodeName, packet.destination_ip_address, port);
      //   nodeMap.add(edges);
      // }
    }

    colorEdge(packet.source_ip_address + '->' + sourceHostName);
    colorEdge(sourceHostName + '->' + packet.destination_ip_address);
    colorEdge(packet.source_ip_address + '->' + destinationHostName);
    colorEdge(destinationHostName + '->' + packet.destination_ip_address);

    colorEdge(packet.source_ip_address, packet.destination_ip_address);
    // colorEdge(uniqueNodeName, packet.destination_ip_address);
    // colorEdge(packet.destination_ip_address, uniqueNodeName);
    // colorEdge(uniqueNodeName, packet.source_ip_address);
  }
}

function colorNode(selectedNode, color)
{
  console.log(selectedNode)
  selectedNode.style('shape', 'ellipse')
  selectedNode.style('width', 90);
  selectedNode.style('height', 90);
  selectedNode.style('border-width', 4)
  selectedNode.style('border-color', color)

}


function colorEdge(source, target) {
  var edge = nodeMap.getElementById(source + '->' + target);
  if (edge.length > 0) {
    trafficLineColor = resolveProtocol(packet.protocol, unique, trafficColors);
    
    uniqueProtocol(packet.protocol,unique,trafficColors); //needs to be before edge creation /animation to update color list
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

function removeNode(packet, id) {
  const source_nodes = nodeMap.$(`[id*="${id}"]`);
  console.log("Removing nodes:", source_nodes)
  nodeMap.remove(source_nodes);

  var alt_nodes = nodeMap.$(`[id*="${packet.sourceHostName}"]`);
  console.log("Removing nodes:", alt_nodes)
  nodeMap.remove(alt_nodes);

  alt_nodes = nodeMap.$(`[id*="${packet.destinationHostName}"]`);
  console.log("Removing nodes:", alt_nodes)
  nodeMap.remove(alt_nodes);
}

function resolveProtocol(protocolCode, protocolArray, colorArray){
  var output;
  let colorIndex = protocolArray.indexOf(protocolCode);
  if (colorIndex>COLOR_COUNT){
      colorIndex = COLOR_COUNT;
  }

  output = colorArray[colorIndex];

  return output;
}


// https://stackoverflow.com/a/34818545
function domainFromUrl(url) {
  if (url === undefined || url === "undefined" || url === null) {
    return undefined;
  }
  var result
  var match
  if (match = url.match(/^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n\?\=]+)/im)) {
      result = match[1]
      while (match = result.match(/^[^\.]+\.(.+\..+)$/)) {
        result = match[1]
        
      }
  }
  if (result.includes('.')) {
    return result;
  }

  return undefined;
}
function getIcon(os) {
    _osIcon = "../../static/images/newdefaulticon.png";

    switch (os) {

        case "Windows":
            _osIcon = "../../static/images/newwindowsicon.png";
            break;
        case "Darwin":
            _osIcon = "../../static/images/newmacicon.png";
            break;
        case "Linux":
            _osIcon = "../../static/images/newlinuxicon.png";
            break;
        case "Android":
            _osIcon = "../../static/images/newandroidicon.png";
            break;
        case "Chrome OS":
            _osIcon = "../../static/images/newchromeicon.png";
            break;
        default:
            _osIcon = "../../static/images/newdefaulticon.png";
    }

    return _osIcon
}