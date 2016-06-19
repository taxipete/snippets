/*
// do the same thing
// setting q by var
function getData($timeout, $q) {
  return function() {
    var defer = $q.defer()

    // simulated async function
    $timeout(function() {
      if(Math.round(Math.random())) {
        defer.resolve('data received!')
      } else {
        defer.reject('oh no an error! try again')
      }
    }, 2000)
    return defer.promise
  }
}

// using $q constructor

function getData($timeout, $q) {
  return function() {
    // simulated async function
    return $q(function(resolve, reject) {
      $timeout(function() {
        if(Math.round(Math.random())) {
          resolve('data received!')
        } else {
          reject('oh no an error! try again')
        }
      }, 2000)
    })
  }
}
*/

// Chaning promise

function getData($timeout, $q) {
  return function() {
    // simulated async function
    return $q(function(resolve, reject) {
      $timeout(function() {
        resolve(Math.floor(Math.random() * 10))
      }, 2000)
    })
  }
}


angular.module('app', [])
.factory('getData', getData)
.run(function(getData) {
  var promise = getData()
    .then(function(num) {
      console.log(num)
      return num * 2
    })
     .then(function(num) {
      console.log(num) // = random number * 2
    })
})


/*  
// All optoins of the promise
angular.module('app', [])
.factory('getData', getData)
.run(function(getData) {
  var promise = getData()
    .then(function(string) {
      console.log(string)
    }, function(error) {
      console.error(error)
    })
    .finally(function() {
      console.log('Finished at:', new Date())
    })
})

*/