angular.module('functionalities', [])
.directive("entering", function(){
 return function(scope, element, attrs) {
     console.log(element);
      element.bind("mouseenter", function(){
        element.addClass(attrs.entering);
      })
    }
})

.directive("leaving", function(){
 return function(scope, element, attrs) {
      element.bind("mouseleave", function(){
        element.removeClass(attrs.entering);
      })
    }
});

/*
 // long hand
 angular.module('functionalities', [])
.directive("entering", function(){
return {
    link: function(scope, element){
         element.bind("mouseenter", function(){
        console.log("Mouse has entered the div");
        })
        
    }
    
}})
 
 */