// Tour js
const tour = new Shepherd.Tour({
  useModalOverlay: true,
  defaultStepOptions: {
    cancelIcon: {
      enabled: true,
    },
    classes: "shepherd-theme-custom",
    scrollTo: {
      behavior: "smooth",
      block: "center",
    },
  },
});

tour.addStep({
  id: "profile-tabs",
  title: "همه تب ها!",
  text: " ادامه دهید 👍\n",
  attachTo: {
    element: "#profile-tabs",
    on: "bottom",
  },
  buttons: [
    { text: "< قبل", action: tour.back },
    { text: "بعد >", action: tour.next },
  ],
});

tour.addStep({
  id: "featured-Stories",
  title: "داستان ها !",
  text: " لورم ایپسوم متن ساختگی \n",
  attachTo: {
    element: "#featured-Stories",
    on: "bottom",
  },
  buttons: [
    { text: "< قبل", action: tour.back },
    { text: "بعد >", action: tour.next },
  ],
});

tour.addStep({
  id: "post",
  title: "پست ها",
  text: " لورم ایپسوم متن ساختگی ..\n",
  attachTo: {
    element: "#post",
    on: "bottom",
  },
  buttons: [
    { text: "< قبل", action: tour.back },
    { text: "بعد >", action: tour.next },
  ],
});

tour.addStep({
  id: "about-me",
  title: "درباره من",
  text: " لورم ایپسوم متن ساختگی !!\n",
  attachTo: {
    element: "#about-me",
    on: "bottom",
  },
  buttons: [
    { text: "< قبل", action: tour.back },
    { text: "بعد >", action: tour.next },
  ],
});

tour.addStep({
  id: "friend",
  title: "دوستان",
  text: " لورم ایپسوم متن ساختگی !\n",
  attachTo: {
    element: "#friend",
    on: "bottom",
  },
  buttons: [
    { text: "< قبل", action: tour.back },
    { text: "پایان &#x1F44D;", action: tour.cancel },
  ],
});

tour.start();

//  **------ slider**

$(".story-container").slick({
  slidesToShow: 4,
  slidesToScroll: 1,
  autoplay: true,
  arrows: false,
  autoplaySpeed: 1000,
  responsive: [
    {
      breakpoint: 1366,
      settings: {
        slidesToShow: 2,
      },
    },
    {
      breakpoint: 768,
      settings: {
        slidesToShow: 3,
      },
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 2,
      },
    },
  ],
});
