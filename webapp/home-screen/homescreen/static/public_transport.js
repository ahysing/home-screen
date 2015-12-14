/*property
    addEventListener, coords, element, geolocation, getCurrentPosition,
    getElementsByClassName, innerText, latitude, length, location, log,
    longitude, onreadystatechange, open, readyState, replace, responseText,
    send, status
*/
var ALT_ICN = 'Transportmiddel for avreise';
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
function iso8601_to_time_hm(time_pp) {
    'use strict';
    var time_start = time_pp.indexOf('T');
    return time_pp.slice(time_start+1, time_start+6);
}
function updateTransportDisplay(elem, text) {
    'use strict';
    if (elem !== undefined) {
        var obj = JSON.parse(text);
        if (obj) {
            var container = document.createElement('div');
            var transports = obj['transport'];
            var d = undefined;
            if (transports) {
                d = transports['departures'];
            }

            if (Array.isArray(d)) {
                d.forEach(function(x) {
                    var route = document.createElement('article');
                    var icon = document.createElement('img');
                    var display_txt = document.createElement('span');
                    var time_txt = document.createElement('time');
                    var h_line = document.createElement('div');

                    var mode = x['vehicle_mode'];
                    var icon_link = '';
                    var port_pre = '//' + window.document.location.host;
                    switch(mode) {
                        case 0:
                        case 'bus':
                            icon_link = port_pre + '/static/icon/bus.png';
                            break;
                        case 'rail':
                            icon_link = port_pre + '/static/icon/train.png';
                            break;
                        case 1:
                        case 'ferry':
                            icon_link = port_pre + '/static/icon/ferry.png';
                            break;
                        default:
                            icon_link = port_pre + '/static/icon/unknown.png';
                            break;
                    }

                    icon.setAttribute('src', icon_link);
                    icon.setAttribute('alt', ALT_ICN);

                    var destination_name = x['destination_name'];
                    display_txt.innerText = x ['line_ref'] + ' ' + destination_name;
                    display_txt.setAttribute('class', 'transport-name');
                    var dt = x['destination_aimed_arrival_time'];
                    var time_pp = iso8601_to_time_hm(dt);
                    time_txt.setAttribute('class', 'transport-time');
                    time_txt.setAttribute('datetime', dt);
                    time_txt.innerText = time_pp;

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

            elem.replaceChild(container, elem.lastChild);
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
