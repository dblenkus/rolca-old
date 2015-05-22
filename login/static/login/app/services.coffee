'use strict'

angular.module 'login.services', ['ngResource']

.factory "School", ["$resource", ($resource) ->
    $resource "/api/v1/school/", {},
        get: {method: "GET", isArray:true, cache: true}
]
