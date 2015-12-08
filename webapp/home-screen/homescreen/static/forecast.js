/*property
    addEventListener, coords, element, geolocation, getCurrentPosition,
    getElementsByClassName, innerText, latitude, length, location, log,
    longitude, onreadystatechange, open, readyState, replace, responseText,
    send, status
*/
var dt_separator = 'til'
var forecast_object = {
    'element': undefined,
    'credits': undefined
};

function fallback() {
    window.location = window.location + '/static';
}

function begForLocation(callback, err_callback) {
    'use strict';
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(callback, err_callback);
    } else {
        fallback();
    }
}

function updateForecastDisplay(elem, credit_elem, responseText) {
    var result = JSON.parse(responseText);
    var forecast_result = result['forecast'];
    if (elem !== undefined) {
        var forecasts = forecast_result['time_forecasts'];

        while (elem.hasChildNodes()) {
            elem.removeChild(elem.lastChild);
        }

        forecasts.slice(0,5).forEach(function(x, i) {
            var container = document.createElement('article');
            var time_elem = document.createElement('div');
            var time_from = document.createElement('time');
            var time_separator = document.createElement('span');
            var time_to = document.createElement('time');
            var element = document.createElement('i');
            var temperature_elem = document.createElement('div');
            var temperature = x['temperature'];
            var tool_tip = x['symbol_name'];

            var start_s = x['start'];
            time_from.setAttribute('datetime', start_s);
            time_from.innerText = start_s.substr(11,5);
            time_separator.innerText = " "+ dt_separator +" ";
            var time_e = x['to'];
            time_to.setAttribute('datetime', time_e);
            time_to.innerText = time_e.substr(11,5);

            var symbol = parseInt(x['symbol_number_ex']);
            var s = 'wi';
            // http://om.yr.no/forklaring/symbol/
            switch (symbol) {
                case 1:
                    s = 'wi wi-day-sunny';
                    break;
                case 2:
                    s = 'wi wi-day-sunny-overcast';
                    break;
                case 3:
                    s = 'wi wi-day-cloudy';
                    break;
                case 4:
                    s = 'wi wi-cloud';
                    break;
                case 5:
                    s = 'wi wi-hail';
                    break;
                case 6:
                    s = 'wi wi-day-sleet-storm';
                    break;
                case 7:
                    s = 'wi wi-day-rain';
                    break;
                case 8:
                    s = 'wi wi-snow';
                    break;
                case 9:
                case 10:
                    s = 'wi wi-day-rain';
                    break;
                case 11:
                    s = 'wi wi-lightning';
                    break;
                case 12:
                    s = 'wi wi-sleet';
                    break;
                case 13:
                    s = 'wi wi-sleet';
                    break;
                case 14:
                    s = 'wi wi-day-alt-snow-thunderstorm';
                    break;
                case 15:
                    s = 'wi wi-fog';
                    break;
                case 20:
                    s = 'wi wi-day-alt-snow-thunderstorm';
                    break;
                case 21:
                    s = 'wi wi-day-alt-snow-thunderstorm';
                    break;
                case 22:
                    s = 'wi wi-day-alt-snow-thunderstorm';
                    break;
                case 23:
                    s = 'wi wi-day-alt-snow-thunderstorm';
                    break;
                case 24:
                    s = 'wi wi-day-sleet-storm';
                    break;
                case 25:
                    s = 'wi wi-storm-showers';
                    break;
                case 26:
                    s = 'wi wi-day-alt-snow-thunderstorm';
                    break;
                case 27:
                    s = 'wi wi-day-alt-snow-thunderstorm';
                    break;
                case 28:
                    s = 'wi wi-snow';
                    break;
                case 29:
                    s = 'wi wi-day-alt-snow-thunderstorm';
                    break;
                case 30:
                    s = 'wi wi-day-sleet-storm';
                    break;
                case 31:
                    s = 'wi wi-day-sleet-storm';
                    break;
                case 32:
                    s = 'wi wi-day-thunderstorm';
                    break;
                case 33:
                    s = 'wi wi-day-alt-snow-thunderstorm';
                    break;
                case 34:
                    s = 'wi wi-day-snow-thunderstorm';
                    break;
                case 40:
                    s = 'wi wi-day-showers';
                    break
                case 41:
                    s = 'wi wi-day-rain';
                    break;
                case 42:
                    s = 'wi wi-day-sleet';
                    break;
                case 43:
                    s = 'wi wi-day-sleet';
                    break;
                case 44:
                    s = 'wi wi-snow';
                    break;
                case 45:
                    s = 'wi wi-snowflake-cold';
                    break;
                case 46:
                    s = 'wi wi-raindrop';
                    break;
                case 47:
                    s = 'wi wi-day-sprinkle';
                    break;
                case 48:
                    s = 'wi wi-rain-mix';
                    break;
                case 49:
                    s = 'wi wi-day-snow';
                    break;
                case 50:
                    s = 'wi wi-snowflake-cold';
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
                default:
                    s = 'wi wi-na';
                    break;
            }

            temperature_elem.setAttribute('class', 'temperature');
            temperature_elem.innerText = temperature + '°';

            container.appendChild(temperature_elem);

            element.setAttribute('class', s);
            element.setAttribute('title', tool_tip);
            container.appendChild(element);

            time_elem.appendChild(time_from);
            time_elem.appendChild(time_separator);
            time_elem.appendChild(time_to);
            time_elem.setAttribute('class', 'weather-time');
            container.appendChild(time_elem);

            var separator = document.createElement('div');
            separator.setAttribute('class', 'horizontal-line');
            container.appendChild(separator);

            container.setAttribute('class', 'weather-container');

            elem.appendChild(container);
        });
    }

    if (credit_elem !== undefined && forecast_result !== null && forecast_result.hasOwnProperty('credit')) {
        var a = document.createElement('a');
        var cred = forecast_result['credit'];
        if (cred !== null && cred.hasOwnProperty('url') && cred.hasOwnProperty('text')) {
        var link = cred['url'];
        var text = cred['text'];
        a.setAttribute('href', link);
        a.innerText = text;
        credit_elem.innerText = '';
        credit_elem.appendChild(a);
        }
    }
}

function deniedLocation() {
    console.log('location denied');
}

function requestForecastForLocation(position) {
    'use strict';
    var xhr = new XMLHttpRequest();
    function handleForecast() {
        'use strict';
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

function setupForecast() {
    'use strict';
    var credits = document.getElementsByClassName('forecast-credits');
    if (credits.length > 0) {
        forecast_object.credits = credits[0];
    }

    var forecast = document.getElementsByClassName('forecast');
    if (forecast.length > 0) {
        forecast_object.element = forecast[0];
        begForLocation(requestForecastForLocation, deniedLocation);
    }
}

function main() {
    'use strict';
    if (window.addEventListener) {
        window.addEventListener('load', setupForecast, false);
    } else {
        fallback();
    }
}

main();
