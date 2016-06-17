# Learning Angular Directives

The purpose of this document is to help me understand angualar Directives.

### Basic Syntax
Remember that camel case in the Javascript and Dashes in the mark up.  In the Javascript `LikeThis` and in the markup `Like-This`.

```html
<body ng-app="greetings">
    <welcome></welcome>
</body>
```

```javascript
angular.module('greetings', [])
.directive("welcome", function() {
  return {
    restrict: "E",
    template: "<div>Howdy there! You look splendid.</div>"
  }
})
```

### Restrict
`restrict` has 4 options the default is A:
* 'A' - only matches attribute name
* 'E' - only matches element name
* 'C' - only matches class name
* 'M' - only matches comment





### Basics
#### 1-Functionalities

This binds the mousenter event to the element the `entering` attribute is added to.

```javascript
angular.module('functionalities', [])
.directive("entering", function(){
 return function(scope, element) {
        element.bind("mouseenter", function(){
        console.log("Mouse has entered the div");
      })
    }
})
```
Note : That this is shorthand, the link function is used, but it is the same as:

```javascript
angular.module('functionalities', [])
.directive("entering", function(){
return {
   link: function(scope, element){
       element.bind("mouseenter", function(){
       console.log("Mouse has entered the div");
       })   
   }
}})
```

### 2-Attrs



This is part of the link `link` function and provides access to data added declaratively.

```html
<div entering="activeClass" leaving>Hover over me for fun times</div>
```

```javascript
angular.module('functionalities', [])
.directive("entering", function(){
 return function(scope, element, attrs) {
      element.bind("mouseenter", function(){
        element.addClass(attrs.entering);
      })
    }
})
```


 NOTE : During the linking phase, interpolation has not been evaluated yet, so if the value of a directive contains {{ }}, it is necessary to call attrs.$observe() in order to properly evaluate the value, otherwise it will return as undefined.



### 3-Talking to Controllers
See 3-Talking_Controllers

This is a simple way to pass methods from a controller to a directive.  It decouples the name of the method in the controller.  By enteringg the method as an attr, the directive is reusable.

```html
<body ng-app="coolApp" ng-controller="FunCtrl as fun">
  <div entering="fun.start()">Hover over me for fun times</div>
</body>
```

```javascript
function FunCtrl() {
  var self = this;

  self.start = function() {
    console.log("Fun times have been started!");
  }

}

angular.module('coolApp', [])
.controller('FunCtrl', FunCtrl)
.directive("entering", function(){
 return function(scope, element, attrs) {
      element.bind("mouseenter", function(){
        scope.$apply(attrs.entering);
      })
    }
});
```
`scope.$apply()` parses the passed string and finds the method within scope.


### 4. Directive to Directive
See 4-Directive_to_Directive

Here we look at sharing a controller in one directive, in other directives.

```html
<body ng-app="greetings">
  <welcome hello howdy hi>Say something!</welcome>
  <br>
   <welcome hi>Only Hi!</welcome>
</body>
```

The welcome directive that contains the controller. All this directive does is console.log the contents of the words array.

NOTE: `scope = {}` this create a local scope in the directive so it will not be shared if multiple instances are used.

```javascript
angular.module('greetings', [])
.directive("welcome", function() {
  return {
    restrict: "E",
    scope: {},  // So multiple instances don't share scope
    controller: function($scope) {      
      $scope.words = [];

      this.sayHello = function() {
        $scope.words.push("hello");
      };

      this.sayHowdy = function() {
        $scope.words.push("howdy");
      };

      this.sayHi = function() {
        $scope.words.push("hi");
      };
    },

    link: function(scope, element){
      element.bind("mouseenter", function() {
        console.log(scope.words);
      });
    }
  }
})
```

These directives make use of the controller in welcome.
They require welcome, so they have access to the welcome directive.
The welcomeCtrl is added to the link function.

```javascript
.directive("hello", function() {
  return {
    require: "welcome", // using another directive
    link: function (scope, element, attrs, welcomeCtrl) {   //welcomeCtrl is defined here.  The controller is passed from welcome directive
      welcomeCtrl.sayHowdy();
    }
  };
 }).directive("howdy", function() {
  return {
    require: "welcome",
    link: function (scope, element, attrs, welcomeCtrl) {
      welcomeCtrl.sayHowdy();
    }
  };
 })

.directive("hi", function() {
  return {
    require: "welcome",
    link: function (scope, element, attrs, welcomeCtrl) {
      welcomeCtrl.sayHi();
    }
  };
 });
 ```


### 5-Transclusion
See 5-Transclusion

The default for directives is to destructively replace the contents of the element.  Sometimes the content needs to persost, this is when transclusion should be enabled

```html
<body ng-app="greetings">
  <welcome>
    <button>Click this button</button>
  </welcome>
 ```

NOTE: `transclude: true` enables the transclusion and `<ng-transclude></ng-transclude>` in the template shows where the content will appear.

As a rule of thumb, transclusion should only be used on element directives, which should always specify a template and define an isolated scope.


```javascript
angular.module('greetings', [])
.directive("welcome", function() {
  return {
    restrict: "E",
    scope: {},
    transclude: true,  // Include the content in the view
    template: "<div>This is the welcome component</div><ng-transclude></ng-transclude>"   // Add ng-transclude (transclude is not in the directive scope)
  }
});
```
