'use strict'

angular.module 'jury', ['ngRoute', 'ngResource', 'jury.controllers', 'jury.filters', 'jury.services',
                        'jury.directives']

.config ['$routeProvider', '$resourceProvider', ($routeProvider, $resourceProvider) ->
    resolvePhotos = ["Photo", (Photo) -> Photo.query().$promise]
    resolvePhoto = ["$route", "Photo", ($route, Photo) ->
        Photo.get({id: $route.current.params.photoId}).$promise]
    resolveRatings = ["Rating", (Rating) -> Rating.query().$promise]
    resolveRating = ["$route", "Rating", ($route, Rating) ->
        Rating.query({photo: $route.current.params.photoId}).$promise]

    $routeProvider
    .when '/',
        templateUrl: '../static/jury/partials/main.html'
        controller: 'MainController'
        resolve: _photos: resolvePhotos, _ratings: resolveRatings
    .when '/:photoId',
        templateUrl: '../static/jury/partials/photo.html'
        controller: 'PhotoController'
        resolve: _photo: resolvePhoto, _photos: resolvePhotos, _rating: resolveRating
    .otherwise redirectTo: '/'

    # TODO: Uncomment in AngularJS 1.3
    # $resourceProvider.defaults.stripTrailingSlashes = false
]
.config ['$httpProvider', ($httpProvider) ->
    $httpProvider.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')
]
