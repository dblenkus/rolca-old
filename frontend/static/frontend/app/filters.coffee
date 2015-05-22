'use strict'

angular.module 'fiap.filters', []

.filter 'date', ->
    (input) -> input.split('-').reverse().join('. ')
