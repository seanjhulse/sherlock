document.addEventListener('DOMContentLoaded', function () {

    // Get the data injected inside the div #data and parse it as JSON
    const dataNode = document.getElementById("data");
    let nodeMapIP = sessionStorage.getItem('ipaddr');
    // Do some hacky clean up
    dataNode.dataset.context = dataNode.dataset.context.replaceAll("'", "\"")

    const data = JSON.parse(dataNode.dataset.context);

    _nodeColor = '#F9F9F9';
    _otherHosts = data.scan.scan;
    _ips = Object.keys(_otherHosts).filter(ip => ip != data.ip)

    let ports = data.ports;
    // _ips = Object.keys(_otherHosts).filter(ip => ip != data.ip)
    ports = ports.substring(1);
    ports = ports.substring(0, ports.length - 1);
    let _ports = ports.split(',')
    for(let i = 0; i < _ports.length; i++)
    {
       _ports[i] = _ports[i].trim();
       _ports[i] = parseInt(_ports[i]);
       
    }

    // // Start with the localhost
    console.log(_ports)
    // Start with the localhost
    var _elements = [{ data: { id: "host" }}];

    var _style = [{
        selector: '#host', //#tag name to select node
        style: {
            shape: 'roundrectangle',
            width: 128,
            height: 128,
            'background-image': getIcon(data.os),
            'background-color': _nodeColor,
            label: nodeMapIP,
            'color': _nodeColor,
        },
    }];


    _ips.forEach(ip => {

        const stringifiedIp = ip.replaceAll('.', '');

        // Add the node
        _elements.push({
            data: {
                id: "other-" + stringifiedIp,
            }
        });

        // Add the Edge
        _elements.push({
            data: {
                id: 'edge-' + stringifiedIp,
                source: "host",
                target: "other-" + stringifiedIp
            }
        });

        const scan = data.scan.scan[`${ip}`];
        if (scan)
        {
            const firstOSMatch = Object.values(scan['vendor'])[0];
            // Add the styling
            _style.push({
                selector: `#other-${stringifiedIp}`,
                style: {
                    shape: 'roundrectangle',
                    width: 125,
                    height: 125,
                    'background-image': getIcon(firstOSMatch),
                    'background-color': _nodeColor,
                    label: ip + " - " + firstOSMatch,
                    color: _nodeColor
                }
            });
        }

        
    });

    //RUN CYTOSCAPE
    var cy = cytoscape({
        container: document.getElementById('localhost'),
        style: _style,
        elements: _elements
    });

    //Connect nodes to host using .add(). may move node creation up to the initial
    //object creation later, but for now will just use this
    //need to figure out how to make nodes longer

    // for (var i = 0; i < _ports.length; i++){

    //     var source = 'port' + _ports[i];
    //     cy.add({
    //         data: {
    //             id: 'edge' + i,
    //             source: source,
    //             target: 'host',
    //         },
    //   });
    // }

    //run .layout() to organize nodes.        

    cy.layout({
        name: 'concentric'
    }).run();
});


function getIcon(os) {
    _osIcon = "../../static/images/default-logo.png";

    switch (os) {

        case "Windows":
            _osIcon = "../../static/images/windows-10-icon.png";
            break;
        case "Darwin":
            _osIcon = "../../static/images/ios-icon.png";
            break;
        case "Linux":
            _osIcon = "../../static/images/linux-icon.png";
            break;
        case "Android":
            _osIcon = "../../static/images/android-icon.png";
            break;
        case "Chrome OS":
            _osIcon = "../../static/images/chrome-os-icon.png";
            break;
        default:
            _osIcon = "../../static/images/default-icon.png";
    }

    return _osIcon
}