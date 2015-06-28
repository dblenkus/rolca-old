'use strict'

angular.module 'rolca.filters', []

.filter 'date', ->
    (input) -> input.split('-').reverse().join('. ')
