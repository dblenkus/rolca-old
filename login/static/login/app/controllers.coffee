'use strict'

angular.module 'login.controllers', []

.controller 'SignupFormController', ['$scope', '$window', ($scope, $window) ->
    $scope.location = $window.location.href;
]

.controller 'LoginFormController', ['$scope', '$window', ($scope, $window) ->
    $scope.location = $window.location.href;
]

.controller 'PasswordResetFormController', ['$scope', '$window', ($scope, $window) ->
    $scope.location = $window.location.href;
]

.controller 'ChangePasswordFormController', ['$scope', '$window', ($scope, $window) ->
    $scope.location = $window.location.href;
]
