document.addEventListener('DOMContentLoaded', function(){

    var cy = window.cy = cytoscape({
        container: document.getElementById('cy'),

        autounselectify: true,
        
        boxSelectionEnabled: false,

        layout: { name: 'cola' },

        style: [ { selector: 'node', css: { 'background-color': '#f92411' } }, { selector: 'edge', css: { 'line-color': '#f92411' } } ],

        elements: {
          nodes: [ { data: { id: "1", label: "You" } }, { data: { id: "2", label: "Google" } }, { data: { id: "4", label: "Amazon" } } ],
          edges: [ { data: { source: "2", target: "1" } }, { data: { source: "4", target: "1" } } ]
        }
    });

});