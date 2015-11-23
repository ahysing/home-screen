/*property
    addEventListener, coords, element, geolocation, getCurrentPosition,
    getElementsByClassName, innerText, latitude, length, location, log,
    longitude, onreadystatechange, open, readyState, replace, responseText,
    send, status
*/

if (typeof(MAIL_USERNAME_KEY) == 'undefined') {
    var MAIL_USERNAME_KEY = 'mail_u';
}

if (typeof(MAIL_PASSWORD_KEY) == 'undefined') {
    var MAIL_PASSWORD_KEY = 'mail_k';
}

if (typeof(MAIL_SUBMIT_KEY) == 'undefined') {
    var MAIL_SUBMIT_KEY = 'mail_s';
}

var mail_object = {
    'element': undefined,
    'root_domain': undefined
};

function clearCredentials() {
    'use strict';
    window.localStorage.removeItem(MAIL_USERNAME_KEY);
    window.localStorage.removeItem(MAIL_PASSWORD_KEY);
    window.localStorage.removeItem(MAIL_SUBMIT_KEY);
}

function login(username, password) {
    'use strict';
    var root_domain = mail_object.root_domain;
    var xhr = new XMLHttpRequest();
    function updateCalendar(e) {
        'use strict';
        var elem = undefined;
        var raw = undefined;
        var event_response = undefined;
        var events = undefined;
        var evnt_elem = undefined;
        var title_elem = undefined;
        var body_elem = undefined;
        var datetime_s_elem = undefined;

        if (xhr.readyState === 4) {
            switch (xhr.status) {
                case 200:
                    elem = document.getElementsByClassName('mail')[0];
                    raw = xhr.responseText;
                    event_response = JSON.parse(raw);
                    events = event_response['events'];
                    elem.innerText = '';
                    if (events) {
                        events.forEach(function(x) {
                            evnt_elem = document.createElement('article');
                            title_elem = document.createElement('title');
                            body_elem = document.createElement('div');
                            datetime_s_elem = document.createElement('div');
                            datetime_s_elem.innerText = x.from + " til " + x.to;
                            datetime_s_elem.setAttribute('class', 'horizontal-line');
                            title_elem.innerText = x.title;
                            body_elem.innerText = x.body;

                            evnt_elem.appendChild(title_elem);
                            evnt_elem.appendChild(body_elem);
                            evnt_elem.appendChild(datetime_s_elem);

                            elem.appendChild(evnt_elem);
                        });
                    }
                    break;
                case 423:
                case 419:
                case 401:
                    clearCredentials();
                    break;
                default:
                    console.log('Error response when fetching calendar ' + xhr.status);
                    break;
            }
        }
    }

    var credentials_from = new FormData();
    credentials_from.append('username', username);
    credentials_from.append('password', password);
    xhr.open('POST', root_domain);
    xhr.onreadystatechange = updateCalendar;
    xhr.send(credentials_from);
}

function setupMail() {
    'use strict';
    var elem = document.getElementsByClassName('mail');
    if (elem.length > 0) {
        var e = elem[0];
        mail_object.root_domain = e.getData('mail.url');
        mail_object.element = e;

        var username = window.localStorage.getItem(MAIL_USERNAME_KEY);
        var password = window.localStorage.getItem(MAIL_PASSWORD_KEY);
        var submit = window.localStorage.getItem(MAIL_SUBMIT_KEY);
        if (username && password && submit) {
            var u_obj = JSON.parse(username);
            var p_obj = JSON.parse(password);
            var s_obj = JSON.parse(submit);
            if (u_obj.id === p_obj.id && p_obj.id === s_obj.id) {
                login(u_obj.username, p_obj.password);
            }
        }
    }
}

function main() {
    if (document.addEventListener) {
        document.addEventListener('load', setupMail);
    }
}

main();