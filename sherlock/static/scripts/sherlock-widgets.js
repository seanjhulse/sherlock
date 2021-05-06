console.log("Widgets Loaded")

// Legend ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

//log unique protocol values

function uniqueProtocol(protocolCode, uniqueArray,colorArray) {
    if (uniqueArray.indexOf(protocolCode)==-1){
        uniqueArray.push(protocolCode);
        console.log(uniqueArray);
        updateLegend(protocolCode,uniqueArray,colorArray)
    }
}

function updateLegend(protocolCode, protocolArray, colorArray) {
    var node = document.createElement('p');
    node.appendChild(document.createTextNode(protocolCode));
    node.style.cssText = "color:" + colorArray[protocolArray.indexOf(protocolCode)];
    var element = document.getElementById('legend');
    element.appendChild(node);

}

// Inspection ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


function createInspectionDiv(label, source, target, protocol, port){
    var container = document.createElement("div");
    var menuid = label + "inspectionmenu";
    container.className = "draggable widget";
    container.id = menuid;
	  container.style.top = '500px';
	  container.style.left = '1000px';

    var header = document.createElement("div");
    header.id = label + "inspectionmenuheader";
    header.className = "headerbar";
    header.innerHTML = protocol + " on " + port;

    var closeButton = document.createElement("button");
    closeButton.className = 'closeButton';
    closeButton.innerHTML = "X";
    closeButton.addEventListener("click", function() {
        this.parentElement.remove()
    });

    container.appendChild(header);
    container.appendChild(closeButton);

    pSourceIP = document.createElement('p');
    pSourceIP.innerHTML = "Source IP: " + source;
    pSourceIP.style.textAlign = "left";
    container.appendChild(pSourceIP);

    pTargetIP = document.createElement('p');
    pTargetIP.innerHTML = "Destination IP: " + target;
    pTargetIP.style.textAlign = "left";
    container.appendChild(pTargetIP);


    document.body.appendChild(container);


    for (i = 0; i<draggableElements.length; i++){
        dragElement(draggableElements[i]);
    }

}
function closeDiv(ele){
    console.log("closing " + ele);
    getElementById(ele).remove();
}