# Angular routing

### ng-view

The default view method.
`ngRoute` is no longer a part of the base `angular.js` file, so you'll need to include the `angular-route.js` file after your the base angular javascript file.
ng-view will allow us to set up config function and access the $routeProvider. In the config function, the services are not yet available to us so we have to access the router through $routeProvider and not $route.

```html
<body ng-app="myApp">
  <ng-view></ng-view>
</body>
```

We can configure a route by using the `when` function of the `$routeProvider`. We need to first specify the route, then in a second parameter provide an object with a `templateUrl` property and a controller property.  Since we're using the `controllerAs` syntax, we'll set the `controllerAs` parameter to “app”.

```javascript
angular.module('myApp', ['ngRoute'])

.config(function($routeProvider){
  $routeProvider.when("/",
    {
      templateUrl: "app.html",
      controller: "AppCtrl",
      controllerAs: "app"
    }
  );
})

.controller('AppCtrl', function() {
  var self = this;
  self.message = "The app routing is working!";
});
```

### $routeProvider

$routeProvider has a simple API, accepting either the when() method, which matches a pattern, or otherwise(). It also allows for method chaining:

```javascript
.config(function($routeProvider){
  $routeProvider.when("/",
    {
      templateUrl: "app.html",
      controller: "AppCtrl",
      controllerAs: "app"
    }
  )
  .when('/cookies',
    {
      template: "NOM NOM NOM NOM"
    }
  )
  .otherwise({
    template: "This route isn't set!"
  });
})
```


### $routeParams

`$routeParams` provides access to contents of the URL

```javascript
angular.module('myApp', ['ngRoute'])

.config(function($routeProvider){
  $routeProvider.when("/:firstName/:middleName/:lastName",
    {
      templateUrl: "app.html",
      controller: "AppCtrl",
      controllerAs: "app"
    }
  );
})

.controller('AppCtrl', function($routeParams) {
  var self = this;
  self.message = $routeParams.firstName + " " + $routeParams.middleName + " " + $routeParams.lastName;
});
```

When the URL `/Bobby/Taylor/Smith` is entered the` self.message is = "Bobby Taylor Smith"`.  Dont forget to inject `$routeParams` in the controller.


### redirectTo

`redirectTo` as well as an easy way to redirct on the `otherwise`.  The `redirectTo` has access to `routeParams, path, search` which makes it possible to do redirects based on the URL.

 ```javascript
 .when('/cookies/:cookieType',
   {
     redirectTo: function (routeParams, path, search) {
       console.log(routeParams);
       console.log(path);
       console.log(search);
       return "/" + routeParams.cookieType;
     }
   }
 )
 .when('/sugar',
   {
     template: 'Sugar cookie'
   }
 )
 ```


 ### Resolve

 The Resolve method lets you do something (like request data) before the controller and template is loaded.
The resolve property is a list of promises - things that need to happen before the controller instantiates and the view loads.

 ```javascript
 app.config(function ($routeProvider) {
  $routeProvider
    .when('/',
    {
      templateUrl: "app.html",
      controller: "AppCtrl"
      resolve: {
        app: function ($q) {
          var defer = $q.defer();
            defer.resolve(); // The page would not render unless the defer was resolved
          return defer.promise;
        }
      }
    }
  )
});
```


OK, not 100% sure about this but i think the idea is that instead of `$timeout` below you would make http request for data.  
That returned or resolved data can be accessed from $route, but it is recommend to pass to a service.

So i guess you would do this when you had to have some data to rendor the page and could not use a loading spinner.  
So CMS, or all data for template etc

```javascript
app.config(function ($routeProvider) {
  $routeProvider
    .when('/',
    {
      templateUrl: "app.html",
      controller: "AppCtrl"
      resolve: {
        loadData: appCtrl.loadData,
        prepData: appCtrl.prepData
      }
    }
  )
});

var appCtrl = app.controller("AppCtrl", function ($scope, $route) {
  $console.log($route); // returned data available via $route
  $scope.model = {
    message: "I'm a great app!"
  }
});

appCtrl.loadData = function ($q, $timeout) {
  var defer = $q.defer;
  $timeout(function () {
    defer.resolve("loadData");
  }, 2000);
  return defer.promise;
};

appCtrl.prepData = function ($q, $timeout) {
  var defer = $q.defer;
  $timeout(function () {
    defer.resolve("prepData");
  }, 2000);
  return defer.promise;
};
```
By passing strings to the resolve method and inspecting the route in the console, $route.current.locals will have the loadData and prepData attributes, with their respective string values that were returned from the promise.
