app.factory('socket', function ($rootScope) {
    var socket = new WebSocket('ws://' + document.location.host + '/wsapi/process_list');
    return socket;
});