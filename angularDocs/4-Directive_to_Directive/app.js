angular.module('greetings', [])
.directive("welcome", function() {
  return {
    restrict: "E",
    scope: {},  // Multiple instances dont share scope
    controller: function($scope) {      // controller added to directive
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