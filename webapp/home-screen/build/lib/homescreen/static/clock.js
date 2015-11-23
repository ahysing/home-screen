/*property
    addEventListener, coords, element, geolocation, getCurrentPosition,
    getElementsByClassName, innerText, latitude, length, location, log,
    longitude, onreadystatechange, open, readyState, replace, responseText,
    send, status
*/

var clock_object = {
    'element': undefined
};

function createCurrentTime() {
    'use strict';
    var currentTime = new Date();
    var currentHours = currentTime.getHours();
    var currentMinutes = currentTime.getMinutes();
    var currentSeconds = currentTime.getSeconds();
    // Pad the minutes and seconds with leading zeros, if required
    currentMinutes = ( currentMinutes < 10 ? "0" : "" ) + currentMinutes;
    currentSeconds = ( currentSeconds < 10 ? "0" : "" ) + currentSeconds;
    // Choose either "AM" or "PM" as appropriate
    var timeOfDay = ( currentHours < 12 ) ? "AM" : "PM";
    // Convert the hours component to 12-hour format if needed
    currentHours = ( currentHours > 12 ) ? currentHours - 12 : currentHours;
    // Convert an hours component of "0" to "12"
    currentHours = ( currentHours == 0 ) ? 12 : currentHours;
    // Compose the string for display
    return currentHours + ":" + currentMinutes + ":" + currentSeconds + " " + timeOfDay;
}

function updateClock() {
    'use strict';
    var currentTimeString = createCurrentTime();
    clock_object.element.innerText = currentTimeString;
}

function attachClock(elem) {
    'use strict';
    clock_object.element = elem;
    setInterval(updateClock, 1000);
}

function setupClock() {
    'use strict';
    var clock = document.getElementsByClassName('clock');
    if (clock.length > 0) {
        var c = clock[0];
        clock_object.element = c;
        attachClock(c);
    }
}

function main() {
    'use strict';
    if (window.addEventListener) {
        window.addEventListener('load', setupClock, false);
    } else {
        var re =  new RegExp('(\/\?|\?).*', 'g');
        var location = window.location;
        location.replace(re, '');
        window.location = location + '/static';
    }
}

main();
