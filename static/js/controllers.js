function ProcessListCtrl($scope, $http, socket) {
    /*
    $http.get('/api/process_list').success(function(data) {
        $scope.processes = data['results'];
    });
    */

    socket.onmessage = function(event) {
        $scope.$apply(function() {
            $scope.processes = JSON.parse(event.data)['results'];
        });
    };
}