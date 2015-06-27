'use strict'

angular.module 'login.directives', ['ui.bootstrap']

.directive 'institution', ["School", (School) ->
    restrict: 'A'
    templateUrl: '/static/login/partials/directives/institution.html'
    scope:
        error: '@'
        name: '@'
        placeholder: '@'
        value: '@'
    link: (scope, element, attrs) ->
        scope.getSchool = (val) ->
            School.get(search: val).$promise.then (data) ->
                _.pluck data, 'name'

        scope.$watch "value", (val, old) ->
            scope.error = false if val != old
]

.directive 'inputField', ->
    restrict: 'A'
    templateUrl: '/static/login/partials/directives/inputfield.html'
    scope:
        error: '@'
        name: '@'
        placeholder: '@'
        type: '@'
        value: '@'
    link: (scope) ->
        scope.type = 'text' if not scope.type?

        scope.$watch "value", (new_val, old_val) ->
            scope.error = false if new_val != old_val
