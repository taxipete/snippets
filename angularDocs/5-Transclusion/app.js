angular.module('greetings', [])
.directive("welcome", function() {
  return {
    restrict: "E",
    scope: {},
    transclude: true,  // Include the content in the view
    template: "<div>This is the welcome component</div><ng-transclude></ng-transclude>"   // Add ng-transclude (transclude is not in the directive scope)
  }
});
