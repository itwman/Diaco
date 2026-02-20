(function () {
  "use strict";
  const forms = document.querySelectorAll(".needs-validation");
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false
    );
  });
})();

$(function () {
  $("#form-validation").submit(function (event) {
    const userName = $("#userName").val();
    const email = $("#email").val();
    const password = $("#password").val();
    const address = $("#address").val();
    const address2 = $("#address2").val();
    const city = $("#city").val();
    const zipCode = $("#zipCode").val();

    const userNameRegex = /^[A-Za-z0-9]+$/;
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    const passwordRegex = /^.{1,8}$/;
    const addressRegex = /^[A-Za-z0-9\s,-]+/;
    const addressRegex2 = /^[A-Za-z0-9\s,-]+/;
    const cityRegex = /^[A-Za-z\s-]+/;
    const zipCodeRegex = /^\d{5}$/;

    const userNameError = $("#userNameError");
    const emailError = $("#emailError");
    const passwordError = $("#passwordError");
    const addressError = $("#addressError");
    const addressError2 = $("#addressError2");
    const cityError = $("#cityError");
    const zipCodeError = $("#zipCodeError");

    userNameError.text("");
    emailError.text("");
    passwordError.text("");
    addressError.text("");
    addressError2.text("");
    cityError.text("");
    zipCodeError.text("");

    if (!userNameRegex.test(userName)) {
      userNameError.text(
        "نام کاربری نامعتبر. لطفاً از کاراکترهای الفبا استفاده کنید."
      );
      event.preventDefault();
    }
    if (!emailRegex.test(email)) {
      emailError.text("ایمیل نامعتبر. لطفاً یک ایمیل معتبر وارد کنید.");
      event.preventDefault();
    }
    if (!passwordRegex.test(password)) {
      passwordError.text("رمز ورود نامعتبر. حداکثر 8 کاراکتر.");
      event.preventDefault();
    }
    if (!addressRegex.test(address)) {
      addressError.text("آدرس نامعتبر. لطفاً یک آدرس معتبر وارد کنید.");
      event.preventDefault();
    }
    if (!addressRegex2.test(address2)) {
      addressError2.text("آدرس نامعتبر. لطفاً یک آدرس معتبر وارد کنید.");
      event.preventDefault();
    }
    if (!cityRegex.test(city)) {
      cityError.text("شهر نامعتبر. لطفاً یک شهر معتبر وارد کنید.");
      event.preventDefault();
    }
    if (!zipCodeRegex.test(zipCode)) {
      zipCodeError.text("کد پستی نامعتبر. لطفاً یک کد پستی معتبر وارد کنید.");
      event.preventDefault();
    }
  });
});
