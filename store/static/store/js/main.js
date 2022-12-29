/*
Navigation
*/

//
const navBar = document.querySelector(".navigation");
const navOpen = document.querySelector(".nav__hamburger");
const navClose = document.querySelector(".close__toggle");
const menu = document.querySelector(".nav__menu");

navOpen.addEventListener("click", () => {
  const navLeft = menu.getBoundingClientRect().left;
  if (navLeft < 0) {
    menu.style.left = "0";
    document.body.classList.add("active");
  } else {
    menu.style.left = "-40rem";
    document.body.classList.remove("active");
  }
});

navClose.addEventListener("click", () => {
  const navLeft = menu.getBoundingClientRect().left;
  if (navLeft > 0) {
    menu.style.left = "0";
  } else {
    menu.style.left = "-40rem";
    document.body.classList.remove("active");
  }
});

// FixNav
window.addEventListener("scroll", () => {
  const navHeight = navBar.getBoundingClientRect().height;
  const scrollHeight = window.pageYOffset;

  if (scrollHeight > navHeight) {
    navBar.classList.add("fix__nav");
  } else {
    navBar.classList.remove("fix__nav");
  }
});

//slider
const slider = document.getElementById("glide1");
if (slider){
  new Glide(slider, {
    type: "carousel",
    startAt: 0,
    perview: 1,
    animationDuration: 800,
    animationTimingFunc: "linear",
  }).mount();
}

if (document.getElementsByClassName('.header').length !== 0){
  document.getElementsByClassName('.header').style.backgroundImage = "url(pic1.png)";
}

//filter form auto load
function submitForm(){
  document.getElementById('filterform').submit()
}
