# $index $event $log

Reminder of $index, $event and $log

### $index
Displays an index in `ng-repeat`

```html
<div ng-app="app">
  <div ng-repeat="item in 'somewords'.split('')">
    {{$index + 1}}. {{item}}
  </div>
</div>
```



### Events

Passes current object to ev.

```html
<div ng-app="app">
  <div
    class="button"
    ng-repeat="item in 'somewords'.split('')"
    ng-click="ev = $event"
    >
    {{$index + 1}}. {{item}}
    {{ev.pageX}}
  </div>
</div>
```

### log

Use the Angular log instead of console.log.
Accesing the rootScope make is available everywhere.

```javascript
var app = angular.module("app", []);

app.run(function($rootScope, $log){
  $rootScope.$log = $log;
});
```

```html

$index is a way to show which iteration of a loop you’re in. If we set up an ng-repeat to repeat over the letters in ‘somewords’, like so:

<div ng-app="app">
  <div ng-repeat="item in 'somewords'.split('')">
    {{$index + 1}}. {{item}}
  </div>
</div>
We can see that we get a listing of all the characters in ‘somewords’ with the index next to it.

Now, let’s add an ng-click attribute to the div as “ev = $event” and a binding to ev.pageX. Let’s also set this div’s class to “button” since we’re going to be clicking on it

<div ng-app="app">
  <div
    class="button"
    ng-repeat="item in 'somewords'.split('')"
    ng-click="ev = $event"
    >
    {{$index + 1}}. {{item}}
    {{ev.pageX}}
  </div>
</div>
Now we can click on all of these buttons and whenever we click we get the extra number next to our index and character. This is the x value of where we’re clicking, and this shows that we can access the event that’s happening through $event.

If we want to log this event, we can do so by using $log. In order to use $log without setting up a controller, we can put it on the root scope of our application. We need to set up the run phase of our application and inject $rootScope and $log in order to expose $log to $rootScope

var app = angular.module("app", []);

app.run(function($rootScope, $log){
  $rootScope.$log = $log;
});
Now we’re able to access the $log function anywhere within our app. (Note that you rarely want to put anything on the $rootScope as anything on the $rootScope will be available throughout the app.) Let’s change the ng-click attribute to “$log.debug($event)”

<div ng-app="app">
  <div
    class="button"
    ng-repeat="item in 'somewords'.split('')"
    ng-click="$log.debug($event)"
    >
    {{$index + 1}}. {{item}}
    {{ev.pageX}}
  </div>
</div>
```
The event details passed to the console.

And how to switch off?
```javascript
app.config(function($logProvider){
  $logProvider.debugEnabled(false);
});
```
