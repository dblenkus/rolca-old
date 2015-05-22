'use strict'

angular.module 'fiap', ['ngRoute', 'ngAnimate', 'ui.bootstrap', 'fiap.controllers',
                        'fiap.filters', 'fiap.services', 'fiap.directives']

.constant('uploadServiceUrl', '/upload/')

.config ['$routeProvider', '$resourceProvider', ($routeProvider, $resourceProvider) ->
    resolveSalon = ["$route", "Salon", ($route, Salon) ->
        Salon.get({id: $route.current.params.salonId}).$promise]
    resolveFile = ["File", (File) -> File.get().$promise]

    $routeProvider
    .when '/',
        redirectTo: '/salon'
        # templateUrl: '../static/frontend/partials/index.html'
        # controller: 'IndexController'
    .when '/salon',
        templateUrl: '../static/frontend/partials/salons.html'
        controller: 'SalonController'
        resolve: _salons: resolveSalon
    .when '/salon/:salonId',
        templateUrl: '../static/frontend/partials/upload.html'
        controller: 'UploadController'
        resolve: _salon: resolveSalon, _files: resolveFile
    .otherwise redirectTo: '/'

    # TODO: Uncomment in AngularJS 1.3
    # $resourceProvider.defaults.stripTrailingSlashes = false
]
