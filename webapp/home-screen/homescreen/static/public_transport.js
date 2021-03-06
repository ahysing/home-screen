/*property
    addEventListener, coords, element, geolocation, getCurrentPosition,
    getElementsByClassName, textContent, latitude, length, location, log,
    longitude, onreadystatechange, open, readyState, replace, responseText,
    send, status,
    element, beg_id
*/
var DELAY_TEXT = 'Avvik fra tabell ';
var HOURS_TEXT = 'timer';
var MINUTES_TEXT = 'minutter';
var SECONDS_TEXT = 'sekunder';
var ALT_ICN = 'Transportmiddel for avreise';
var TRANSPORT_LIMIT =  '10';
var TRANSPORT_RETRY_DELAY = 6000;

var pt_object = {
    'element': undefined
};
function fallbackLocationIgnorantBrowserTransport() {
    'use strict';
    var CLS = '.transport';
    var noscript = document.querySelector(CLS + ' > noscript');
    if (noscript) {
        var statics = document.createElement('div');
        statics.innerHTML = noscript.innerText;
        var f = document.querySelector(CLS);
        f.replaceChild(statics, noscript);
    }
}
function deniedLocation(position_error) {
    'use strict';
    console.error('location denied for public transports!');
}
function iso8601_to_time_hm(time_pp) {
    'use strict';
    var time_start = time_pp.indexOf('T');
    return time_pp.slice(time_start+1, time_start+6);
}
function bindByIdToElem(id, elem) {
    'use strict';
    var empty_txt = document.getElementById(id).cloneNode(true);
    empty_txt.removeAttribute('id');
    empty_txt.removeAttribute('hidden');
    elem.appendChild(empty_txt);
}
function updateTransportDisplay(elem, text) {
    'use strict';
    if (elem !== undefined) {
        var obj = JSON.parse(text);
        if (obj) {
            var container = document.createElement('div');
            var transports = obj.transport;
            var d;
            if (transports) {
                d = transports.departures;
            }

            if (Array.isArray(d)) {
                var stop_text = document.createElement('h1');
                stop_text.textContent = transports.stop.name;
                container.appendChild(stop_text);
                d.forEach(function(x) {
                    var route = document.createElement('article');
                    var icon = document.createElement('img');
                    var display_txt = document.createElement('span');
                    var time_txt = document.createElement('time');
                    var delay_txt = document.createElement('span');
                    var h_line = document.createElement('div');

                    var mode = x.vehicle_mode;
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

                    var destination_name = x.destination_name;
                    display_txt.textContent = x.line_ref + ' ' + destination_name;
                    display_txt.setAttribute('class', 'transport-name');
                    var cls = 'transport-time';
                    var dt = x.expected_departure_time;
                    var dt_original = x.aimed_departure_time;
                    if (dt_original !== dt) {
                        cls += ' delay';
                        var diff_ms = Date.parse(dt) - Date.parse(dt_original);
                        var diff_s = Math.floor(diff_ms / 1000);
                        var diff_s_rem = diff_s % 60;
                        var diff_m = Math.floor((diff_s - diff_s_rem) / 60);
                        var diff_m_rem = diff_m % 60;
                        var diff_h = Math.floor((diff_m - diff_m_rem) / 60);
                        var diff_h_rem = diff_h % 24;
                        var delay_tt = DELAY_TEXT + ' ';
                        if (diff_h) delay_tt += diff_h_rem + ' ' + HOURS_TEXT +' ';
                        if (diff_m) delay_tt += diff_m_rem + ' ' + MINUTES_TEXT + ' ';
                        if (diff_s) delay_tt += diff_s_rem + ' ' + SECONDS_TEXT + ' ';
                        delay_txt.textContent = delay_tt;
                        delay_txt.setAttribute('class', 'delay-text');
                        delay_txt.dataset.delayMs = diff_ms;
                    }

                    var time_pp = iso8601_to_time_hm(dt);
                    time_txt.setAttribute('class', cls);
                    time_txt.setAttribute('datetime', dt);
                    time_txt.textContent = time_pp;

                    h_line.setAttribute('class', 'horizontal-line');
                    route.appendChild(icon);
                    route.appendChild(display_txt);
                    route.appendChild(time_txt);
                    route.appendChild(delay_txt);
                    route.appendChild(h_line);
                    container.appendChild(route);
                });
                if (d.length === 0) {
                    bindByIdToElem('no-departures', container);
                }
            } else {
                console.error('No transports are available.');
            }

            elem.replaceChild(container, elem.lastChild);
        }
    }
}

function requestTransportForLocation(e) {
    'use strict';
    var xhr = new XMLHttpRequest();
    function handleTransport() {
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
function userRequestTransport() {
    'use strict';
    return [requestTransportForLocation, deniedLocation];
}
function setupTransport() {
    'use strict';
    var transport = document.getElementsByClassName('transport');
    if (transport.length > 0) {
        var t = transport[0];
        pt_object.element = t;
    }
}

function main() {
    'use strict';
    if (window.addEventListener) {
        window.addEventListener('load', setupTransport, false);
    }
}

main();
