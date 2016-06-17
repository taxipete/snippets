

angular.module('coolApp', [])
.controller('FunCtrl', function() {
  var self = this;

  self.start = function() {
    console.log("Fun times have been started!");
  }

})
.directive("entering", function(){
 return function(scope, element, attrs) {
      element.bind("mouseenter", function(){
        scope.$apply(attrs.entering);
      })
    }
});

// Rewritten to look like a normal controller and directive.
