/*property
    addEventListener, coords, element, geolocation, getCurrentPosition,
    getElementsByClassName, innerText, latitude, length, location, log,
    longitude, onreadystatechange, open, readyState, replace, responseText,
    send, status
*/
var TRANSPORT_LIMIT =  '10';
var pt_object = {
    'element': undefined
};
function begForLocation(callback) {
    'use strict';
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(callback);
    }
}
function iso8601_to_timehm(time_pp) {
    'use strict';
    var time_start = time_pp.indexOf('T');
    var time_end = Math.max(time_pp.indexOf('Z'),time_pp.indexOf('+'));
    return time_pp.slice(time_start+1, time_end);
}
function updateTransportDisplay(elem, text) {
    'use strict';
    if (elem !== undefined) {
        var obj = JSON.parse(text);
        if (obj) {
            var container = document.createElement('div');

            while (elem.hasChildNodes()) {
                elem.removeChild(elem.lastChild);
            }

            var transports = obj['transport'];
            var d = undefined;
            if (transports) {
                d = transports['departures'];
            }

            if (Array.isArray(d)) {
                d.forEach(function(x) {
                    var route = document.createElement('article');
                    var icon = document.createElement('img');
                    var display_txt = document.createElement('div');
                    var time_txt = document.createElement('time');
                    var h_line = document.createElement('div');

                    var mode = x['vehicle_mode'];
                    var icon_link = '';
                    switch(mode) {
                        case 'bus':
                            icon_link = '/static/icon/bus.png';
                            break;
                        case 'train':
                            icon_link = '/static/icon/train.png';
                            break;
                        case 'ferry':
                            icon_link = '/static/icon/ferry.png';
                            break;
                        default:
                            icon_link = '/static/icon/unknown.png';
                            break;
                    }
                    icon.setAttribute('href', icon_link);
                    icon.setAttribute('alt', 'Mode of transport for departure');

                    var destination_name = x['destination_name'];
                    display_txt.innerText = x ['line_ref'] + ' ' + destination_name;

                    var dt = x['destination_aimed_arrival_time'];
                    var time_pp = iso8601_to_timehm(dt);
                    time_txt.setAttribute('datetime', dt);
                    time_txt.innerText = time_pp

                    h_line.setAttribute('class', 'horizontal-line');
                    route.appendChild(icon);
                    route.appendChild(display_txt);
                    route.appendChild(time_txt);
                    route.appendChild(h_line);
                    container.appendChild(route);
                });
            } else {
                console.error('No transport inforamtion is available.');
            }

            elem.appendChild(container);
        }
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

    var url_template = '/transport/next?latitude=%lat&longitude=%lon&limit=%lim';
    var url = url_template.replace('%lat', String(e.coords.latitude)).replace('%lon', String(e.coords.longitude))
    .replace('%lim', TRANSPORT_LIMIT);
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
