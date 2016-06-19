# ngAnimations


Must use the ngAnimations module.

Enable transitions on the element in the css and add an `opacity:0` to the element class `.ng-hide`.
You can now customize the hide and shows.  Fading, spinny etc.

```html
<div class="box-one" ng-show="test.showBoxOne">
  Hello! I am <b>box one</b>.
</div>
```

```css
.box-one {
  -webkit-transition:all linear 0.5s;
  transition:all linear 0.5s;
}
.box-one.ng-hide {
  opacity:0;
}
```

[Playaround here](http://codepen.io/EricSimons/pen/PwdKNE )


At some point you may want to have different animations for showing and hiding, entering and leaving, etc. The simplest way to perform this is by hooking into ngAnimate's add and remove classes (for ng-hide, these are .ng-hide-add and .ng-hide-remove). This way, when ng-hide is being added to the element you can fire an animation through .ng-hide-add, but when it's being removed, you can specify a different animation altogether with .ng-hide-remove.

```css
.box-one { }

.box-one.ng-hide-add {
  -webkit-animation:0.5s hide;
  animation:0.5s hide;
}

@keyframes hide {
  0% {
    opacity:1;
    transform: scale(1);
  }
  30% {
    transform: scale(1.02);
  }
  100% {
    opacity:0;
    transform: scale(0.5);
  }
}

@-webkit-keyframes hide {
  0% {
    opacity:1;
    transform: scale(1);
  }
  30% {
    transform: scale(1.02);
  }
  100% {
    opacity:0;
    transform: scale(0.5);
  }
}


.box-one.ng-hide-remove {
  -webkit-animation:0.3s show;
  animation:0.3s show;
}

@keyframes show {
  0% {
    opacity:0;
    transform: scale(0.5);
  }
  70% {
    transform: scale(1.02);
  }
  100% {
    opacity:1;
    transform: scale(1);
  }
}

@-webkit-keyframes show {
  0% {
    opacity:0;
    transform: scale(0.5);
  }
  70% {
    transform: scale(1.02);
  }
  100% {
    opacity:1;
    transform: scale(1);
  }
}
```
