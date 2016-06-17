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
