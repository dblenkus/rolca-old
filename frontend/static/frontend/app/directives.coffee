'use strict'

angular.module 'fiap.directives', []

.directive 'loadingWheel', ->
    restrict: 'A'
    scope:
        enabled: '='
    replace: true
    templateUrl: '/static/frontend/partials/directives/loadingwheel.html'
    link: (scope, element, attrs) ->
        scope.$watch 'enabled', (val=true) -> scope.show = val

.directive 'imageUpload', ['uploadServiceUrl', 'alert', (uploadServiceUrl, alert) ->
    restrict: 'A'
    scope:
        done: "="
    replace: true
    templateUrl: '/static/frontend/partials/directives/imageupload.html'
    link: (scope, element, attrs) ->
        uploadOptions =
            url: uploadServiceUrl
            dataType: 'json'
            autoUpload: true
            done: scope.done
            fail: -> alert.error 'errorA'
        element.fileupload uploadOptions
]

.directive 'imageView', ['Photo', 'alert', (Photo, alert) ->
    restrict: 'A'
    scope:
        file: '='
        salon: '=salonObj'
    replace: true
    templateUrl: '/static/frontend/partials/directives/imageview.html'
    link: (scope, element, attrs) ->
        Photo.get file: scope.file.id, ->
            scope.loading = false

        photo = new Photo()

        scope.themes = scope.salon.themes

        scope.changeTheme = (theme) ->
            scope.selectedTheme = theme

        update = ->
            return if !scope.title?
            photo.title = scope.title
            photo.$save().finally -> scope.loading = false
                .catch -> alert.error 'error'

        throttleUpdate = _.debounce update, 500

        scope.$watch 'title', (val) ->
            scope.loading = true
            throttleUpdate()

        # scope.$watch 'theme', (val) ->
        #     update() if val
        #     # _.throttle update, 5 if val
]

.directive 'salon', ->
    restrict: 'A'
    scope:
        salon: '=salonObj'
    replace: true
    templateUrl: '/static/frontend/partials/directives/salon.html'
    controller: ['$scope', '$location', ($scope, $location) ->
        $scope.go = -> $location.path "/salon/#{$scope.salon.id}"
    ]



