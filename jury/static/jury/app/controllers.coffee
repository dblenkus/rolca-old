'use strict'

angular.module 'jury.controllers', []

.controller 'RootController', ['Photo', '$scope', (Photo, $scope) ->
  console.log 'root controler'
  $scope.$root._ = _;
]

.controller 'MainController', ['_photos', '_ratings', '$scope', '$timeout', '$location', (_photos, _ratings, $scope, $timeout, $location) ->
  $scope.photos = _photos
  $scope.ratings = _ratings

  console.log _ratings

  $scope.selectPhoto = (id) ->
    $location.path '/'+id

  $timeout ->
    $scope.pivotW = $('.photoThumb').width()
  $(window).resize ->
    $scope.pivotW = $('.photoThumb').width()
    $scope.$apply()
]

.controller 'PhotoController', ['_photo', '_photos', '_rating', '$scope', '$timeout', '$location', 'Rating', (_photo, _photos, _rating, $scope, $timeout, $location, Rating) ->
  $scope.photo = _photo

  if _rating.length > 0
    $scope.rating = _rating[0]
  else
    $scope.rating = new Rating({photo: _photo.id, rating: 0})

  switchPhoto = (switchTo) ->
    if switchTo != 0
      currIx = _.findIndex(_photos, {id: _photo.id})
      return if currIx < 0
      return if currIx+switchTo < 0
      return if currIx+switchTo >= _photos.length

      $location.path '/' + _photos[currIx+switchTo].id
      if !$scope.$$phase
        $scope.$apply()

  w = false
  h = false
  $('.singlePhoto img').on 'load', ->
    w = $(this).width()
    h = $(this).height()
    refreshH()
    $scope.$apply()
    $that = $(this)
    $timeout -> $('body').scrollTop($that.offset().top - 10)

  window.Rating = Rating
  rate = (stars) ->
    $scope.rating.rating = stars
    console.log $scope.rating.id
    if $scope.rating.id
      $scope.rating.$update()
    else
      $scope.rating.$save()
    switchPhoto(1)
  $scope.rate = rate

  $('body').off 'keypress'
  $('body').on 'keypress', (e) ->
    rate(10) if e.keyCode == 48
    rate(e.keyCode-48) if 49 <= e.keyCode and e.keyCode <= 57
  .on 'keyup', (e) ->
    switchTo = 0
    switchTo = -1 if e.keyCode == 37
    switchTo = +1 if e.keyCode == 39
    switchPhoto(switchTo)

  $('input').on 'keypress', (e) ->
    e.stopPropagation()

  refreshH = ->
    return if !w
    remainingW = $('.singlePhoto').width()
    remainingH = $(window).height() - 50

    $scope.photoStyle = if (remainingW / w < remainingH / h) then {width: remainingW} else {height: remainingH}

  $timeout refreshH
  $(window).resize ->
    refreshH()
    $scope.$apply()
]
