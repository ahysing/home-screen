/*property
    addEventListener, coords, element, geolocation, getCurrentPosition,
    getElementsByClassName, innerText, latitude, length, location, log,
    longitude, onreadystatechange, open, readyState, replace, responseText,
    send, status
*/

var pt_object = {
    'element': undefined
};
function begForLocation(callback) {
    'use strict';
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(callback);
    }
}

function updateTransportDisplay(elem, text) {
    'use strict';
    if (elem !== undefined) {
        var transports = JSON.parse(text);
        var container = document.createElement('div');
        container.setAttribute('class', 'transport');

        while (elem.hasChildNodes()) {
            elem.removeChild(elem.lastChild);
        }

        var trips = transports['departures'];
        trips.forEach(function(x) {
            var route = document.createElement('div');
            route.setAttribute('class', 'transport');
            route.innerText = x['line_name'] + '    ' + x['destination_aimed_arrival_time'];
            container.appendChild(route);
        });

        elem.appendChild(container);
    }
}

function requestTransportForLocation(e) {
    'use strict';
    var xhr = new XMLHttpRequest();
    function handleTransport() {
        'use strict';
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                updateTransportDisplay(pt_object.element, xhr.responseText);
            } else {
                console.log('transport response status ' + xhr.status);
            }
        }
    }

    var url_template = '/transport/next?latitude=%lat&longitude=%lon';
    var url = url_template.replace('%lat', String(e.coords.latitude)).replace('%lon', String(e.coords.longitude));
    xhr.open('GET', url);
    xhr.setRequestHeader('Accepts', 'application/json');
    xhr.onreadystatechange = handleTransport;
    xhr.send();
}


function setupTransport() {
    'use strict';
    var transport = document.getElementsByClassName('transport');
    if (transport.length > 0) {
        var t = transport[0];
        pt_object.element = t;
    }

    begForLocation(requestTransportForLocation);
}

function main() {
    'use strict';
    if (window.addEventListener) {
        window.addEventListener('load', setupTransport, false);
    }
}

main();
