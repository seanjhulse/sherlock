document.addEventListener('DOMContentLoaded', function () {

    /* first, create home node with appropriate labels using spread notation
        then, loop through open ports and do the same for them
        
        add style element with spread notation, also looping through ports
        
        finally, create nodes with .add() and organize concentric. possibly just add nodes too.
    */
    _hostAddress = "192.168.1.5";
    _hostOS = "Windows 10";
    _ports = [80, 443, 632, 663, 500, 3600];

    _nodeColor = '#F9F9F9';


    //initialize object for cytoscape
    var hostJSON = { container: document.getElementById('host-node'), }

    //create and append nodes under list 'element'

    var _elements = [{ data: { id: "host" } },];

    for (var i = 0; i < _ports.length; i++) {
        _elements.push({ data: { id: 'port' + _ports[i] } });
    }

    hostJSON = {
        ...hostJSON,
        elements: _elements
    }

    //create and append style objects under list 'style'

    var _osIcon;
    var _portIcon = "../../static/images/port-icon.png";

    switch (_hostOS) {

        case "Windows 10":
            _osIcon = "../../static/images/windows-10-icon.png";
            break;
        case "iOs":
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
            _osIcon = "../../static/images/default-logo.png";
    }


    var _style = [{
        selector: '#host', //#tag name to select node
        style: {
            shape: 'roundrectangle',
            width: 128,
            height: 128,
            'background-image': _osIcon,
            'background-color': _nodeColor,
            label: _hostAddress,
            'color': _nodeColor,
        },
    }];


    for (var i = 0; i < _ports.length; i++) {
        _style.push({
            selector: '#port' + _ports[i],
            style: {
                shape: 'roundrectangle',
                width: 85,
                height: 85,
                'background-image': _portIcon,
                'background-color': _nodeColor,
                label: "port " + _ports[i],
                'color': _nodeColor,
            }
        });
    }

    hostJSON = {
        ...hostJSON,
        style: _style,
    }

    //RUN CYTOSCAPE
    var cy = cytoscape(hostJSON);


    //Connect nodes to host using .add(). may move node creation up to the initial
    //object creation later, but for now will just use this
    //need to figure out how to make nodes longer

    for (var i = 0; i < _ports.length; i++) {

        var source = 'port' + _ports[i];
        cy.add({
            data: {
                id: 'edge' + i,
                source: source,
                target: 'host',
            },
        });
    }


    //run .layout() to organize nodes.        

    cy.layout({
        name: 'concentric',
        minDist: 40
    }).run();
});