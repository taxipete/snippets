# Advanced Angular Directives

This follows on from Basic Angular Directives.



### Advanced
#### 6-Directive Communication

If one knows there is a hierarchical relationship between nested directives, it is possible to communicate between them using controllers. With their respective directives, a parent directive can expose something like the makeAnnouncement() method, and have it passed down to a child directive. Here, we can inject the country directive controller into the linking function of the city directive. This is accomplished by matching the require naming scheme to the parent directive name. With this, the controller of the parent directive is available for use in the child directive. This ‘inheritance’ of the controller works invariant of ancestral distance.


```html
<div ng-app="app">
    <country>
        <state>
            <city>
            </city>
        </state>
    </country>
</div>
```


```javascript
var app = angular.module("app",[]);

app.directive("country", function () {
    return {
        restrict: "E",
        controller: function () {
            this.makeAnnouncement = function (message) {
                console.log("Country says: " + message);
            };
        }
    };
});
```
First directive, sets up country and creates the controller.

```javascript
app.directive("state", function () {
    return {
        restrict: "E",
        controller: function () {
            this.makeLaw = function (law) {
                console.log("Law: " + law);
            };
        }
    };
});
```
2nd directive creates state and create a 2nd controller.

```javascript
app.directive("city", function () {
    return {
        restrict: "E",
        require: ["^country","^state"],
        link: function (scope, element, attrs, ctrls) {
            ctrls[0].makeAnnouncement("This city rocks");
            ctrls[1].makeLaw("Jump higher");
        }
    };
});
```
The final directive at the bottom of the nest.  Requires the 1st and 2nd directives and passes them in to the link function.
Passed in as `ctrls` and then accessed as an array.

### Isolated Scope and passing Methods
See : 7-IsolatedScopeAndMethods

This is an example of how to pass a controller method in to a directive with an isolate scope (needed if the directive is used more than once).  

Why do you need Isolated Scope:

```javascript
var app = angular.module('choreApp', []);

app.directive("kid", function() {
  return {
    restrict: "E",
    template: '<input type="text" ng-model="chore"> {{chore}}'
  };
});
```



```html
<div ng-app="choreApp">
  <kid></kid>
  <kid></kid>
  <kid></kid>
</div>
```
Here when the `kid` directive is repeated the `{{chore}}` binding is shared across all directives.  Typing in the input of one, updates all.

What we need to do is isolate them so they don’t share the bindings. We can do this by setting the scope property on the object being returned in the “kid” directive.

```javascript
app.directive("kid", function() {
  return {
    restrict: "E",
    scope: {},
    template: '<input type="text" ng-model="chore"> {{chore}}'
  };
});
```

Now we can go back and tell each `kid` directive a different chore,  and we see that the binding still works, but it’s limited to each individual directive we created.
This breaks any interaction with the controllers if the bindings we use are scoped in the controller.

Let’s create a controller “ChoreCtrl” and set up some thing we’ll want to interact with. We’ll create a logChore function which takes a chore, and alerts ‘chore + “ is done!”’

```javascript
app.controller("ChoreCtrl", function($scope){
  $scope.logChore = function(chore){
    alert(chore + " is done!");
  };
});
```
We need to wire up `logChore` and `done`. We can do this by setting the `done` property on the scope object within the directive to an ampersand (`&`) for an expression and then change the template to include a div with a class of "button" and an ng-click attribute set to "done({chore:chore})" and say "I'm done!" inside the div.

The {chore:chore} syntax maps the chore from the model we made in the `<input>` to be passed to the logChore function when we said `done="logChore(chore)"` (in the kid directive)

```javascript
app.directive("kid", function() {
  return {
    restrict: "E",
    scope: {
        done: "&"
      },
    template: '<input type="text" ng-model="chore">' +
      '{{chore}}' +
      '<div class="button" ng-click="done({chore: chore})">I\'m done</div>'
  };
});
```


## Scope operators

* Isolate Scope "@" - evaluated as string
* Isolate Scope "=" - two way binding to object
* Isolate Scope "&" - Access to methods of parent controller  

### Isolate Scope "@"

the scope "@" will pass bindings as strings in the same way as using the attrs.

On isolate scope The attributes are evaluated to a string before they are handed off to the directive’s scope.

```html
<div ng-app="drinkApp">
  <div ng-controller="AppCtrl">
    <div drink flavor="strawberry"></div>
  </div>
</div>
```
This setup serves to take the flavor attribute passed from the view, assign it to the flavor value in the scope, and insert it into a div, which is dropped into the drink element directive.

```javascript
var app = angular.module('drinkApp', []);

app.controller("AppCtrl", function ($scope) {
})

app.directive("drink", function () {
  return {
    scope: {},
    template: '<div>{{ flavor }}</div>',
    link: function (scope, element, attrs) {
      scope.flavor = attrs.flavor;
    }
  };
});
```

With the @ operator, we are able to substitute the entire link function into a single attribute within the scope object. This operator serves to do exactly the same thing as what the link function does above: extract an attribute by name, and assign it to the scope.

```javascript
app.directive("drink", function () {
  return {
    scope: {
      flavor: "@"
    },
    template: '<div>{{ flavor }}</div>',
  };
});
```
This works even when passing from a controller

```javascript
app.controller("AppCtrl", function ($scope) {
  $scope.ctrlFlavor = "blackberry";
})
```

```html
<div ng-app="drinkApp">
  <div ng-controller="AppCtrl">
    <div drink flavor="{{ctrlFlavor}}"></div>
  </div>
</div>
```

Or when passing from mg-model

```html
<div ng-app="drinkApp">
  <div ng-controller="AppCtrl">
    <input type="text" ng-model="ctrlFlavor">
    <div drink flavor="{{ ctrlFlavor }}"></div>
  </div>
</div>
```


### Isolate Scope "="

Unlike the `@` operator, which expects a string attribute, the `=` operator expects an object which it can bind to.
A binding is set up both ways, so that an template with an `<input>` will bind to the controller object, allowing modification.
In the example above if we change `<div drink flavor="{{ ctrlFlavor }}"></div>` to `<div drink flavor="ctrlFlavor"></div>` and use the `=` operator.



```html
<div ng-app="drinkApp">
  <div ng-controller="AppCtrl">
    <div drink flavor="ctrlFlavor"></div>
  </div>
</div>
```

```javascript
var app = angular.module('drinkApp', []);

app.controller("AppCtrl", function ($scope) {
  $scope.ctrlFlavor = "blackberry";
})

app.directive("drink", function () {
  return {
    scope: {
      flavor: "="
    },
    template: '<div>{{ flavor }}</div>',
  };
});
```


### Isolate Scope &

The `&` allows the passing of methods from a controller in to a directive.
The `&` operator allows you to invoke or evaluate an expression on the parent scope of whatever the directive is inside of.
Basic Example

```html
<div ng-app="phoneApp">
    <div ng-controller="AppCtrl">
        <div phone dial="callHome()"></div>
    </div>
</div>
```

```javascript
var app = angular.module('phoneApp', []);

app.controller("AppCtrl", function($scope) {

    $scope.callHome = function() {
        alert("called Home");
    }
})

app.directive("phone", function() {
    return {
        scope: {
            dial: "&"
        },
        template: '<div class="button" ng-click="dial()">Call Home!</div>',

    };
});
```

The `phone` directive passes the `callHome` method from the controller, in the scope it is assigned to `dial`.  
Which is then called by the ng-click directive in the template.

**Passing data**

When passing data via the method the Syntax is a little different.

```html
<div ng-app="phoneApp">
    <div ng-controller="AppCtrl">

        <div phone dial="callHome(message)"></div>

    </div>
</div>
```

```javascript
var app = angular.module('phoneApp', []);

app.controller("AppCtrl", function ($scope) {

	$scope.callHome = function (message) {
      alert(message);
    };
})


app.directive("phone", function () {
  return {
    scope: {
      dial: "&"
    },
    template: '<input type="text" ng-model="value">' +
      '<div class="button" ng-click="dial({message:value})">' +
      'Call home!</div>',
  };
});
```

The value of the input is added as an attribute on a message object.  The value is retreived in the controller via the message key.
