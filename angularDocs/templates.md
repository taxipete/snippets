# Templates

There are multiple ways to use templates in Angular.  The basics are.


### Basic String

Passing a string directly into $route for our template that we want to use with our TestCtrl. You usually wouldn't do this in your application though, as it'd be hard to maintain all of your templates in your config block. Angular allows us to specify remote templates by using the templateUrl property instead of template.

```html
<!DOCTYPE html>
<html>
<head>
  <title>$templateCache</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.0-beta.5/angular.min.js"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.0-beta.5/angular-route.min.js"></script>
  <script src="app.js"></script>
</head>
<body ng-app="app">
  <div ng-view></div>
</body>
</html>
```

```javascript
(function(){

  function TestCtrl() {
    this.user = {name: 'Blake'};
  }

  angular.module('app', ['ngRoute'])
  .config(function($routeProvider){
    $routeProvider.when('/', {
      controller: 'TestCtrl as test',
      template: 'Hello {{ test.user.name }}!'
    })
    .otherwise('/');
  })
  .controller('TestCtrl', TestCtrl);

})()
```


### Remote Templates

When a template is loaded using `templateUrl`, the template is load in to memory in the `$templateCache`.
If the template is called again, the file is not reloaded it is pulled from the `$templateCache`, meaning that any template is only loaded once.

```javascript
function TestCtrl() {
  this.user = {name: 'Blake'};
}

angular.module('app', ['ngRoute'])
.config(function($routeProvider){
  $routeProvider.when('/', {
    controller: 'TestCtrl as test',
    templateUrl: 'test.html'
  })
  .otherwise('/');
})
.controller('TestCtrl', TestCtrl);
```

You can view the the templateCache by injecting it in to a controller

```javascript
function TestCtrl($templateCache) {
  this.user = {name: 'Blake'};

  console.log($templateCache.get('test.html'));
}
```

### Inline Templates
Not recommended

Angular ships with a script directive, which when passed text/ng-template as the text attribute, Angular will recognize that it is a template meant to be used with our application and put any content between the script tags into $templateCache, keyed by the id attribute.

```html
<!DOCTYPE html>
<html>
<head>
  <title>$templateCache</title>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.0-beta.5/angular.min.js"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.0-beta.5/angular-route.min.js"></script>
  <script src="app.js"></script>
</head>
<body ng-app="app">
  <div ng-view></div>
  <script type="text/ng-template" id="test.html">
      Hello {{test.user.name}}

  </script>
</body>
</html>
```

## Populating $templateCache directly

`$templateCache` is simply a key-value store where you can get and put templates. Angular will automatically check `$templateCache `whenever you use `templateUrl` in your application or when you specify a template src with ng-include before attempting to retrieve your template from a remote location.

```javascript
angular.module('app').run(function ($templateCache){
  $templateCache.put('test.html', 'Hello {{ test.user.name }}!');
});
```

Automate this with Gulp [gulp-angular-templatecache]([https://github.com/miickel/gulp-angular-templatecache)
