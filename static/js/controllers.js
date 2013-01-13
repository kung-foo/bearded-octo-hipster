function ProcessListCtrl($scope, $http, socket) {
    $scope.orderProp = 'pid';

    $http.get('/api/process_list').success(function(data) {
        $scope.processes = data['records'];

        socket.onmessage = function(event) {
            data = JSON.parse(event.data);
            $scope.$apply(function() {
                var clone = angular.copy($scope.processes);

                for (var i in clone) {
                    proc_hash = clone[i]['proc_hash'];
                    for (var j in data['removed']) {
                        if (data['removed'][j] == proc_hash) {
                            delete clone[i];
                        }
                    }

                    for (var j in data['updated']) {
                        k = data['updated'][j];
                        if (k == proc_hash) {
                            clone[i] = data['records'][k];
                        } 
                    }
                }

                $scope.processes = Array();

                for (var i in data['added']) {
                    k = data['added'][i];
                    $scope.processes.push(data['records'][k]);
                }

                for (var i in clone) {
                    if (clone[i] !== undefined) {
                        $scope.processes.push(clone[i]);
                    }
                }
            });
        };
    });
}