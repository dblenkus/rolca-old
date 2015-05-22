'use strict'

angular.module 'jury.services', []

.factory "Photo", ["$resource", ($resource) ->
    $resource "/api/v1/photo/:id/:func", id: "@id",
        query: {method: "GET", isArray: true, cache: true}
        get: {method: "GET", cache: true}
]

.factory "Rating", ["$resource", ($resource) ->
    $resource "/api/v1/rating/:id/:func", id: "@id",
        query: {method: "GET", isArray: true}
        update: {method: "PUT"}
]
