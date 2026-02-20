// Sweet Alert start //
$("#click_1").on("click", function () {
  Swal.fire({
    title: "لورم ایپسوم متن ساختگی با تولید سادگی",
    confirmButtonText: "بسیار خب",
    customClass: {
      confirmButton: "btn btn-primary",
    },
    buttonsStyling: false,
  });
});

$("#click_2").on("click", function () {
  Swal.fire({
    title: "لورم ایپسوم؟",
    text: "لورم ایپسوم متن ساختگی با تولید سادگی",
    icon: "question",
    confirmButtonText: "بسیار خب",
  });
});

$("#click_3").on("click", function () {
  Swal.fire({
    title: "بسیار خوب!",
    text: "لورم ایپسوم متن ساختگی با تولید سادگی",
    icon: "success",
    confirmButtonText: "بسیار خب",
  });
});
$("#click_4").on("click", function () {
  Swal.fire({
    position: "top-end",
    icon: "success",
    title: "لورم ایپسوم متن ساختگی با تولید سادگی",
    showConfirmButton: false,
    timer: 1500,
  });
});
$("#click_5").on("click", function () {
  Swal.fire({
    confirmButtonText: "بسیار خب",
    title: "انیمیشن سفارشی با Animate.css",
    showClass: {
      popup: "animate__animated animate__fadeInDown",
    },
    hideClass: {
      popup: "animate__animated animate__fadeOutUp",
    },
  });
});
$("#click_6").on("click", function () {
  Swal.fire({
    title: "عالی!",
    text: "مودال با عکس سفارشی.",
    imageUrl: "assets/images/blog-app/09.jpg",
    imageWidth: 400,
    imageHeight: 400,
    confirmButtonText: "بسیار خب",
    imageAlt: "تصویر سفارشی",
  });
});
$("#click_7").on("click", function () {
  Swal.fire({
    title: "نام کاربری گیتهاب خود را وارد کنید",
    cancelButtonText: "انصراف",
    input: "text",
    inputAttributes: {
      autocapitalize: "off",
    },
    showCancelButton: true,
    confirmButtonText: "نمایش",
    showLoaderOnConfirm: true,
    preConfirm: async (login) => {
      const response = await fetch(`//api.github.com/users/${login}`);
      if (!response.ok) {
        Swal.showValidationMessage(`Request failed: ${response.statusText}`);
        return;
      }
      return await response.json();
    },
    allowOutsideClick: () => !Swal.isLoading(),
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: `آواتار ${result.value.login} `,
        imageUrl: result.value.avatar_url,
      });
    }
  });
});

$("#click_8").on("click", function () {
  Swal.fire({
    title: "لورم ایپسوم ؟",
    confirmButtonText: "بسیار خب",
    icon: "question",
    input: "range",
    inputLabel: "سن شما",
    inputAttributes: {
      min: 8,
      max: 120,
      step: 1,
    },
    inputValue: 25,
  });
});
$("#click_9").on("click", function () {
  let timerInterval;
  Swal.fire({
    title: "هشدار خودکار!",
    html: "این دکمه پس از  <b></b> میلی ثانیه بسته میشود.",
    timer: 2000,
    timerProgressBar: true,
    didOpen: () => {
      Swal.showLoading();
      const b = Swal.getHtmlContainer().querySelector("b");
      timerInterval = setInterval(() => {
        b.textContent = Swal.getTimerLeft();
      }, 100);
    },
    willClose: () => {
      clearInterval(timerInterval);
    },
  }).then((result) => {
    /* Read more about handling dismissals below */
    if (result.dismiss === Swal.DismissReason.timer) {
      console.log("I was closed by the timer");
    }
  });
});
$("#click_10").on("click", function () {
  Swal.fire({
    title: "<strong>خوش آمدید</strong>",
    html: `
  لورم ایپسوم متن ساختگی با تولید سادگی
  `,
    showCloseButton: true,
    showCancelButton: true,
    focusConfirm: false,
    confirmButtonText: `
    <i class="fa fa-thumbs-up"></i> عالی!
  `,
    confirmButtonAriaLabel: "بسیار خوب!",
    cancelButtonText: `
    <i class="fa fa-thumbs-down"></i>
  `,
    cancelButtonAriaLabel: "انصراف",
  });
});
$("#click_11").on("click", function () {
  Swal.fire({
    title: "اطمینان دارید؟",
    text: "قابل بازیابی نیست!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "بله!",
    cancelButtonText: "انصراف!",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: "حذف شد!",
        text: "فایل با موفقیت حذف شد.",
        icon: "success",
        confirmButtonText: "بسیار خب",
      });
    }
  });
});
$("#click_12").on("click", function () {
  const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: "btn btn-primary me-2",
      cancelButton: "btn btn-danger",
    },
    buttonsStyling: false,
  });

  swalWithBootstrapButtons
    .fire({
      title: "اطمینان دارید؟",
      text: "این عملیات قابل بازیابی نیست!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "بله",
      cancelButtonText: "انصراف!",
      reverseButtons: true,
    })
    .then((result) => {
      if (result.isConfirmed) {
        swalWithBootstrapButtons.fire({
          title: "حذف شد!",
          text: "فایل با موفقیت حذف شد.",
          icon: "success",
          confirmButtonText: "بسیار خب",
        });
      } else if (
        /* Read more about handling dismissals below */
        result.dismiss === Swal.DismissReason.cancel
      ) {
        swalWithBootstrapButtons.fire({
          title: "کنسل شد",
          text: "فایل حذف نشد :)",
          icon: "error",
          confirmButtonText: "بسیار خب",
        });
      }
    });
});
$("#click_13").on("click", function () {
  Swal.fire({
    title: "عالی!",
    confirmButtonText: "بسیار خب",
    text: "لورم ایپسوم متن ساختگی با تولید سادگی..",
  });
});
$("#click_14").on("click", function () {
  (async () => {
    const ipAPI = "//api.ipify.org?format=json";

    const inputValue = fetch(ipAPI)
      .then((response) => response.json())
      .then((data) => data.ip);

    const { value: ipAddress } = await Swal.fire({
      title: "آیپی خود را وارد کنید",
      input: "text",
      inputLabel: "آیپی شما",
      confirmButtonText: "بسیار خب",
      cancelButtonText: "انصراف",
      inputValue: inputValue,
      showCancelButton: true,
      inputValidator: (value) => {
        if (!value) {
          return "مقداری وارد کنید!";
        }
      },
    });

    if (ipAddress) {
      Swal.fire({
        text: `آیپی شما :  ${ipAddress}`,
        confirmButtonText: "بسیار خب",
      });
    }
  })();
});
$("#click_15").on("click", function () {
  Swal.fire({
    icon: "error",
    title: "خطا...",
    text: "خطایی رخ داده است!",
    confirmButtonText: "بسیار خب",
    footer: '<a href="">چرا این اتفاق افتاد؟</a>',
  });
});
$("#click_16").on("click", function () {
  const Toast = Swal.mixin({
    toast: true,
    position: "top-start",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener("mouseenter", Swal.stopTimer);
      toast.addEventListener("mouseleave", Swal.resumeTimer);
    },
  });

  Toast.fire({
    icon: "success",
    title: "با موفقیت وارد شدید",
  });
});

// sweet alert end //
