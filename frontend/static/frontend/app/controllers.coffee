'use strict'

angular.module 'fiap.controllers', []

.controller 'RootController', ['$scope', ($scope) ->
    console.log 1
]

.controller 'IndexController', ['$scope', ($scope) ->
    console.log 2
]

.controller 'SalonController', ['_salons', '$scope',
(_salons, $scope) ->
    $scope.salons = _salons.objects
]

.controller 'UploadController', [ '$scope', '_salon', '_files', 'alert',
($scope, _salon, _files, alert) ->
    $scope.files = _files.objects
    $scope.salon = _salon

    $scope.addPhotos = (e, data) ->
        $scope.files = data.result.concat $scope.files
        $scope.$apply() if !$scope.$$phase
]
