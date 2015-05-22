"use strict"

angular.module "fiap.services", ["ngResource"]

.factory "Salon", ["$resource", ($resource) ->
    $resource "/api/v1/salon/:id/:func", id: "@id",
        get: {method: "GET", cache: true}
]

.factory "Theme", ["$resource", ($resource) ->
    $resource "/api/v1/theme/:id/:func", id: "@id",
        get: {method: "GET", cache: true}
]

.factory "File", ["$resource", ($resource) ->
    $resource "/api/v1/file/:id/:func", id: "@id",
        get: {method: "GET", cache: true}
]

.factory "Photo", ["$resource", ($resource) ->
    $resource "/api/v1/photo/:id/:func", id: "@id",
        get: {method: "GET", cache: true}
]

.factory "alert", ["$rootScope", "$timeout", ($rootScope, $timeout) ->
    $rootScope.alerts = []

    closeAlert = (alert) -> res.close $rootScope.alerts.indexOf alert
    add = (type, msg) ->
        $rootScope.alerts.push 'type': type, 'msg': msg, close: -> closeAlert @
        $timeout (-> closeAlert @), 5000

    res =
        error: (msg) -> add "danger", msg
        warning: (msg) -> add "warning", msg
        info: (msg) -> add "info", msg
        success: (msg) -> add "success", msg
        close: (index) -> $rootScope.alerts.splice index, 1
]

.run ["$rootScope", "$window", "$location", ($rootScope, $window, $location) ->
    $rootScope.$on "$locationChangeStart", (event, nextUrl, currentUrl) ->
        $window.ga 'send', 'pageview', 'page': $location.url() if $window.ga?
]
