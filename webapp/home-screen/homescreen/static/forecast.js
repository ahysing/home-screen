/*property
    addEventListener, coords, element, geolocation, getCurrentPosition,
    getElementsByClassName, textContent, latitude, length, location, log,
    longitude, onreadystatechange, open, readyState, replace, responseText,
    send, status,
    element, credits, num_forecasts, beg_id
*/
var dt_separator = 'til';
var forecast_object = {
    'beg_id': -1,
    'credits': undefined,
    'element': undefined,
    'num_forecasts': 5
};

function fallbackLocationIgnorantBrowserForecast() {
    'use strict';
    var CLS = '.forecast';
    var noscript = document.querySelector(CLS + ' > noscript');
    if (noscript) {
        var statics = document.createElement('div');
        statics.innerHTML = noscript.innerText;
        var f = document.querySelector(CLS);
        f.replaceChild(statics, noscript);
    }
}

function updateForecastDisplay(root, credit_root, responseText) {
    var result = JSON.parse(responseText);
    var forecast_result = result.forecast;
    if (root !== undefined && Array.isArray(forecast_result)) {
        var slice_size = forecast_object.num_forecasts;
        var container = document.createElement('div');
        forecast_result.forEach(function(area) {
            var forecast_text = document.createElement('h1');
            forecast_text.textContent = area.place.name;
            container.appendChild(forecast_text);
            var forecasts = area.time_forecasts;
            forecasts.slice(0, slice_size).forEach(function(x, i) {
                var forecast = document.createElement('article');
                var time_elem = document.createElement('div');
                var time_from = document.createElement('time');
                var time_separator = document.createElement('span');
                var time_to = document.createElement('time');
                var element = document.createElement('i');
                var temperature_elem = document.createElement('div');
                var temperature = x.temperature;
                var tool_tip = x.symbol_name;

                var start_s = x.start;
                time_from.setAttribute('datetime', start_s);
                time_from.textContent = start_s.substr(11,5);
                time_separator.textContent = " "+ dt_separator +" ";
                var time_e = x.to;
                time_to.setAttribute('datetime', time_e);
                time_to.textContent = time_e.substr(11,5);

                var symbol = parseInt(x.symbol_number_ex);
                var s = '';
                // http://om.yr.no/forklaring/symbol/
                switch (symbol) {
                    case 1:
                        s = 'wi-day-sunny';
                        break;
                    case 2:
                        s = 'wi-day-sunny-overcast';
                        break;
                    case 3:
                        s = 'wi-day-cloudy';
                        break;
                    case 4:
                        s = 'wi-cloud';
                        break;
                    case 5:
                        s = 'wi-hail';
                        break;
                    case 6:
                        s = 'wi-day-sleet-storm';
                        break;
                    case 7:
                        s = 'wi-day-rain';
                        break;
                    case 8:
                        s = 'wi-snow';
                        break;
                    case 9:
                    case 10:
                        s = 'wi-day-rain';
                        break;
                    case 11:
                        s = 'wi-lightning';
                        break;
                    case 12:
                        s = 'wi-sleet';
                        break;
                    case 13:
                        s = 'wi-sleet';
                        break;
                    case 14:
                        s = 'wi-day-alt-snow-thunderstorm';
                        break;
                    case 15:
                        s = 'wi-fog';
                        break;
                    case 20:
                        s = 'wi-day-alt-snow-thunderstorm';
                        break;
                    case 21:
                        s = 'wi-day-alt-snow-thunderstorm';
                        break;
                    case 22:
                        s = 'wi-day-alt-snow-thunderstorm';
                        break;
                    case 23:
                        s = 'wi-day-alt-snow-thunderstorm';
                        break;
                    case 24:
                        s = 'wi-day-sleet-storm';
                        break;
                    case 25:
                        s = 'wi-storm-showers';
                        break;
                    case 26:
                        s = 'wi-day-alt-snow-thunderstorm';
                        break;
                    case 27:
                        s = 'wi-day-alt-snow-thunderstorm';
                        break;
                    case 28:
                        s = 'wi-snow';
                        break;
                    case 29:
                        s = 'wi-day-alt-snow-thunderstorm';
                        break;
                    case 30:
                        s = 'wi-day-sleet-storm';
                        break;
                    case 31:
                        s = 'wi-day-sleet-storm';
                        break;
                    case 32:
                        s = 'wi-day-thunderstorm';
                        break;
                    case 33:
                        s = 'wi-day-alt-snow-thunderstorm';
                        break;
                    case 34:
                        s = 'wi-day-snow-thunderstorm';
                        break;
                    case 40:
                        s = 'wi-day-showers';
                        break;
                    case 41:
                        s = 'wi-day-rain';
                        break;
                    case 42:
                        s = 'wi-day-sleet';
                        break;
                    case 43:
                        s = 'wi-day-sleet';
                        break;
                    case 44:
                        s = 'wi-snow';
                        break;
                    case 45:
                        s = 'wi-snowflake-cold';
                        break;
                    case 46:
                        s = 'wi-raindrop';
                        break;
                    case 47:
                        s = 'wi-day-sprinkle';
                        break;
                    case 48:
                        s = 'wi-rain-mix';
                        break;
                    case 49:
                        s = 'wi-day-snow';
                        break;
                    case 50:
                        s = 'wi-snowflake-cold';
                        break;
                    case 16:
                    case 17:
                    case 18:
                    case 19:
                    case 35:
                    case 36:
                    case 37:
                    case 38:
                    case 39:
                        s = 'wi-na';
                        break;
                    default:
                        s = 'wi-na';
                        break;
                }

                temperature_elem.setAttribute('class', 'temperature');
                temperature_elem.textContent = temperature + '??';
                forecast.appendChild(temperature_elem);

                var icon_style = 'weather-icon wi ' + s;
                element.setAttribute('class', icon_style);
                element.setAttribute('title', tool_tip);
                forecast.appendChild(element);

                time_elem.appendChild(time_from);
                time_elem.appendChild(time_separator);
                time_elem.appendChild(time_to);
                time_elem.setAttribute('class', 'weather-time');
                forecast.appendChild(time_elem);

                var separator = document.createElement('div');
                separator.setAttribute('class', 'horizontal-line');
                forecast.appendChild(separator);

                container.appendChild(forecast);
            });

            if (credit_root !== undefined && area !== null && area.hasOwnProperty('credit')) {
                var a = document.createElement('a');
                var cred = area.credit;
                if (cred !== null && cred.hasOwnProperty('url') && cred.hasOwnProperty('text')) {
                    var link = cred.url;
                    var text = cred.text;
                    a.setAttribute('href', link);
                    a.textContent = text;
                    credit_root.textContent = '';
                    credit_root.appendChild(a);
                }
            } else {
                console.error('No place to attach credits for wether forecasts.');
            }
        });
    } else {
        console.error('No forecasts are available.');
    }

    root.replaceChild(container, root.firstChild);
}
function deniedLocation(position_error) {
    'use strict';
    console.error('location denied for forecasts!');
}

function requestForecastForLocation(position) {
    'use strict';
    var xhr = new XMLHttpRequest();
    function handleForecast() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                updateForecastDisplay(forecast_object.element, forecast_object.credits, xhr.responseText);
            } else {
                console.log(xhr.status);
            }
        }
    }
    var coords = position.coords;
    var url_template = '/forecast?latitude=%lat&longitude=%lon';
    var url = url_template.replace('%lat', String(coords.latitude)).replace('%lon', String(coords.longitude));
    xhr.open('GET', url);
    xhr.setRequestHeader('Accepts', 'application/json');
    xhr.onreadystatechange = handleForecast;
    xhr.send();
}
function userRequestForecast() {
    'use strict';
    return [requestForecastForLocation, deniedLocation];
}
function setupForecast() {
    'use strict';
    var credits = document.getElementsByClassName('forecast-credits');
    if (credits.length > 0) {
        forecast_object.credits = credits[0];
    }

    var forecast = document.getElementsByClassName('forecast');
    if (forecast.length > 0) {
        forecast_object.element = forecast[0];
    }
}

function main() {
    'use strict';
    if (window.addEventListener) {
        window.addEventListener('load', setupForecast, false);
    }
}

main();
