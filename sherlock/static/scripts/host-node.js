document.addEventListener('DOMContentLoaded', function () {
    /* first, create home node with appropriate labels using spread notation
        then, loop through open ports and do the same for them
        add style element with spread notation, also looping through ports
        finally, create nodes with .add() and organize concentric. possibly just add nodes too.
    */

    let _hostAddress = sessionStorage.ipaddr;

    fetch('/scan-ports/' + _hostAddress)
        .then(res => res.json())
        .then(res => {
            let ports = res.port_data.ports;

            _nodeColor = '#F9F9F9';

            //initialize object for cytoscape
            var hostJSON = { container: document.getElementById('host-node'), }

            //create and append nodes under list 'element'
            var _elements = [{ data: { id: "host" } },];
            for (var i = 0; i < ports.length; i++) {
                _elements.push({ data: { id: 'port' + ports[i].portid + '-' + ports[i].protocol } });
            }

            hostJSON = {
                ...hostJSON,
                elements: _elements
            }

            //create and append style objects under list 'style'

            // var _osIcon;
            var _portIcon = "../../static/images/newporticon.png";

            var _style = [{
                selector: '#host', //#tag name to select node
                style: {
                    shape: 'roundrectangle',
                    width: 128,
                    height: 128,
                    'background-image': getIcon(data.os),
                    'background-color': _nodeColor,
                    label: _hostAddress,
                    'color': _nodeColor,
                },
            }];


            for (var i = 0; i < ports.length; i++) {
                _style.push({
                    selector: '#port' + ports[i].portid + '-' + ports[i].protocol,
                    style: {
                        shape: 'roundrectangle',
                        width: 85,
                        height: 85,
                        'background-image': _portIcon,
                        'background-color': _nodeColor,
                        label: 'Port ' + ports[i].portid + ' ' + (ports[i].protocol).toUpperCase(),
                        'color': _nodeColor,
                    }
                });
            }

            hostJSON = {
                ...hostJSON,
                style: _style,
            }

            document.getElementById('loading-icon').remove();

            //RUN CYTOSCAPE
            var cy = cytoscape(hostJSON);


            //Connect nodes to host using .add(). may move node creation up to the initial
            //object creation later, but for now will just use this
            //need to figure out how to make nodes longer

            for (var i = 0; i < ports.length; i++) {

                var source = 'port' + ports[i].portid + '-' + ports[i].protocol;
                cy.add({
                    data: {
                        id: 'edge' + i,
                        source: source,
                        target: 'host',
                    },
                });
            }

            cy.layout({
                name: 'concentric',
                minDist: 40
            }).run();
        });
    
});


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