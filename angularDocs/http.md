# $http

The $http service is how AngularJS makes rest API calls. It's capable of making the common 'GET', 'POST', 'PUT', and 'DELETE' API calls as well as the less common 'PATCH' and 'HEAD' calls. It can also make jsonp calls for cross-origin requests.

### Getting

Simple Get Example
`$http` methods return Angular $q promises, which allows for clean code flow via promise chaining. We can use this concept to mutate the returned data.


```html
<html>
    <head>
        <title>$http fun</title>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.0-beta.5/angular.min.js"></script>
        <script src="app.js"></script>
    </head>
    <body ng-app="app" ng-controller="TestCtrl as test">
        {{test.message}}
        <button ng-click="test.getMessage()">Get Message</button>
    </body>
</html>
```

```javascript
angular.module('app', [])
.service('testService', testService)
.controller('TestCtrl', TestCtrl)


function testService($http) {
    this.get = function() {
      return $http.get('http://test-routes.herokuapp.com/test/hello')
        .then(function(res) {
          // return the enveloped data
          return res.data.message;
        })
    }
}

function TestCtrl(testService) {
  var self = this;
  self.getMessage = function() {

    testService.get()
      .then(function(message) {
        self.message = message;
      })
  }
}

```

### POST
POST-ing data is similar to GET-ing it except we can pass a JavaScript object to be sent along with the request. In our service, we'll create a method that'll allow us to POST a message to an API endpoint and receive an upper-cased version in return:

```html        
<input ng-model="test.sendMessage" placeholder="Enter a message">
        <button ng-click="test.postData(test.sendMessage)">uppercase</button>
        {{test.sendMessage}}
```

```javascript
//service
this.upperCase = function(data) {
  return $http.post('http://test-routes.herokuapp.com/test/uppercase', data)
}

// controller
self.postData = function(message) {
  testService.upperCase({message: message})
    .success(function(body) {
        console.log(body.message);
      self.sendMessage = body.message;
    })
}
```

#### success() and error() Methods
The promises returned by `$http` have two additional non-standard methods attached to them: `success()` and `error()`. These methods behave just like the `then()` and `catch()` methods on standard promises accept rather than passing a standard response object to the callback function, they instead pass the response properties as function parameters starting with data. They are provided merely as convenience functions.


### $http Interceptors

Interceptors make changes to http request before and after they are sent

```javascript
function testInterceptor() {
  return {
    request: function(config) {
      return config;
    },

    requestError: function(config) {
      return config;
    },

    response: function(res) {
      return res;
    },

    responseError: function(res) {
      return res;
    }
  }
}

angular.module('app', [])
.factory('testInterceptor', testInterceptor)
.config(function($httpProvider) {
  $httpProvider.interceptors.push('testInterceptor');
})
.run(function($http) {
  $http.get('http://test-routes.herokuapp.com/test/hello')
    .then(function(res) {
      console.log(res.data.message)
    })
})
```

```html
<html>
    <head>
        <title>$http interceptors</title>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.0-beta.5/angular.min.js"></script>
        <script src="app.js"></script>
    </head>
    <body ng-app="app">
    </body>
</html>
```

An interceptor is simply a factory() service that returns an object with 4 properties that map to functions:

* request: called before a request is sent, capable of mutating the request object
* requestError:
* response: called with an $http request succeeds, is passed the results object,
* responseError: called if an $http method fails

This object is then registered as an interceptor with the $httpProvider in a config() block. It's perfectly fine to include all or only a subset of the properties that are needed.



### Reminders for later

angular has a  $resource service for  CRUD operations.
[Creating a CRUD App in Minutes with Angular’s $resource](https://www.sitepoint.com/creating-crud-app-minutes-angulars-resource/)
