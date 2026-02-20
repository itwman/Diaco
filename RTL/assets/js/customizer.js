$(function () {
  // **------ Load customizer ------**
  html_string = `<button class="customizer-btn" type="button" data-bs-toggle="offcanvas" data-bs-target="#customizerOptions"
        aria-controls="customizerOptions">
  <i class="ti ti-settings-2"></i>
</button>

<div class="offcanvas offcanvas-end app-customizer" data-bs-scroll="true" tabindex="-1" id="customizerOptions"
     aria-labelledby="customizerOptionsLabel">

  <div class="offcanvas-header flex-wrap bg-primary">
    <h5 class="offcanvas-title text-white" id="customizerOptionsLabel"> سفارشی سازی </h5>
    <p class="d-block text-white opacity-75">در اینجا میتوانید براساس سلیقه خود سفارشی کنید ..!</p>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="بستن"></button>
  </div>

  <div class="offcanvas-body">
    <div class="app-divider-v secondary py-3">
      <h6 class="mt-2">انتخاب های سایدبار</h6>
    </div>
    <ul class="sidebar-option">
      <li class="vertical-sidebar">
        <ul>
          <li class="header"></li>
          <li class="sidebar"></li>
          <li class="body"> <span class="badge text-bg-secondary b-r-6"> عمودی</span> </li>
        </ul>
      </li>
      <li class="horizontal-sidebar">
        <ul>
          <li class="header h-20"><span class="badge text-bg-secondary b-r-6"> افقی</span></li>
          <li class="body w-100"></li>
        </ul>
      </li>
      <li class="dark-sidebar">
        <ul>
          <li class="header"></li>
          <li class="sidebar bg-dark-600"></li>
          <li class="body"><span class="badge text-bg-secondary b-r-6"> تاریک </span></li>
        </ul>
      </li>
    </ul>

    <div class="app-divider-v secondary py-3">
      <h6 class="mt-2">لایه ها</h6>
    </div>
    <ul class="layout-option">
     <!-- <li class="ltr">
        <ul>
          <li class="header"></li>
          <li class="body"><span class="badge text-bg-secondary b-r-6"> چپ چین </span></li>
          <li class="sidebar"></li>
        </ul>
      </li> --!> 
      <li class="rtl">
        <ul>
          <li class="header"></li>
          <li class="sidebar"></li>
          <li class="body"> <span class="badge text-bg-secondary b-r-6"> راستچین </span> </li>
        </ul>
      </li>
      <li class="box-layout">
        <ul>
          <li class="header"></li>
          <li class="sidebar"></li>
          <li class="body"> <span class="badge text-bg-secondary b-r-6"> جعبه ای </span> </li>
        </ul>
      </li>
    </ul>
    <h6 class="mt-3">رنگ ها</h6>
    <ul class="color-hint p-0">
      <li class="default">
        <div></div>
      </li>
      <li class="gold">
        <div></div>
      </li>
      <li class="warm">
        <div></div>
      </li>
      <li class="happy">
        <div></div>
      </li>
      <li class="nature">
        <div></div>
      </li>
      <li class="hot">
        <div></div>
      </li>
    </ul>
    <div class="app-divider-v secondary py-3">
      <h6 class="mt-2 font-primary">اندازه متن</h6>
    </div>
    <ul class="text-size">
      <li class="small-text"> کوچک </li>
      <li class="medium-text"> متوسط </li>
      <li class="large-text"> بزرگ </li>
    </ul>
  </div>

  <div class="offcanvas-footer">
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-danger w-100" onclick="resetCustomizer()">بازنشانی</button>
      <a type="button" class="btn btn-success w-100" href="#" target="_blank">خرید</a>
    </div>
    <div class="d-flex gap-2 mt-2">
      <a type="button" class="btn btn-primary w-100" href="mailto:email@gmail.com" target="_blank">پشتیبانی</a>
      <a type="button" class="btn btn-dark w-100" href="#" target="_blank">مستندات</a>
    </div>

  </div>

</div>`;

  const customizer = $("#customizer");
  if (customizer.length > 0) {
    customizer.html(html_string);
  }

  setTimeout(() => {
    loadConfiguration();
  }, 1000);
});

$(document).on("click", ".sidebar-option > li", function () {
  const sidebarClassName = $(this).attr("class");
  try {
    $("nav")
      .removeClass("horizontal-sidebar vertical-sidebar dark-sidebar")
      .addClass(sidebarClassName);
    setLocalStorageItem("sidebar-option", sidebarClassName);

    if (sidebarClassName === "vertical-sidebar") {
      $(".main-nav").css("marginLeft", "0px").css("marginRight", "0px");
    }

    setUpHorizontalHeader();
  } catch (e) {
    console.log("Fail to change sidebar option");
  }
});

$(document).on("click", ".layout-option > li", function () {
  const layoutClassName = $(this).attr("class");
  try {
    if (layoutClassName == "box-layout") {
      $("html").attr("dir", "rtl");
      $("body").attr("class", "box-layout rtl");
    } else {
      $("body").attr("class", layoutClassName);
      $("html").attr("dir", layoutClassName);
    }

    setLocalStorageItem("layout-option", layoutClassName);
  } catch (e) {
    console.log("Fail to change layout option");
  }
});

$(document).on("click", ".color-hint > li", function () {
  const colorClassName = $(this).attr("class");
  try {
    const colorOption = getLocalStorageItem("color-option", "default");

    $(".app-wrapper").removeClass(colorOption).addClass(colorClassName);

    const primaryColorValues = $(`.${colorClassName}`)
      .css("--primary")
      .split(",");
    if (primaryColorValues.length === 3) {
      const primaryColorHex = rgbToHex(
        parseInt(primaryColorValues[0]),
        parseInt(primaryColorValues[1]),
        parseInt(primaryColorValues[2])
      );
      setLocalStorageItem("color-primary", primaryColorHex);
    }

    const secondaryColorValues = $(`.${colorClassName}`)
      .css("--secondary")
      .split(",");
    if (secondaryColorValues.length === 3) {
      const secondaryColorHex = rgbToHex(
        parseInt(secondaryColorValues[0]),
        parseInt(secondaryColorValues[1]),
        parseInt(secondaryColorValues[2])
      );
      setLocalStorageItem("color-secondary", secondaryColorHex);
    }

    setLocalStorageItem("color-option", colorClassName);
  } catch (e) {
    console.log("Fail to change color option");
  }
  window.location.reload();
});

$(document).on("click", ".text-size > li", function () {
  const fontClassName = $(this).attr("class");
  $("body").attr("text", fontClassName);
  setLocalStorageItem("text-option", fontClassName);
});

/* Handle click for Sidebar option, layout option and Text size */
$(document).on("click", ".offcanvas-body > ul > li", function () {
  $(this).parent().find("li").removeClass("selected");
  $(this).addClass("selected");
});

/* Theme name prepend to localStorage key */
const themeName = "ki-admin";

/* Get item from localStorage */
function getLocalStorageItem(key, defaultValue = null) {
  return localStorage.getItem(`${themeName}-${key}`) ?? defaultValue;
}

/* Set item in localStorage */
function setLocalStorageItem(key, value) {
  localStorage.setItem(`${themeName}-${key}`, value);
}

function hexToRGB(hex, alpha) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);

  return alpha ? `rgba(${r}, ${g}, ${b}, ${alpha})` : `rgb(${r}, ${g}, ${b})`;
}

function loadConfiguration() {
  $(".offcanvas-body > ul > li").removeClass("selected");

  const selectedSidebarOption = getLocalStorageItem(
    "sidebar-option",
    "vertical-sidebar"
  );
  $("nav").addClass(selectedSidebarOption);
  $(".offcanvas-body > ul")
    .find(`.${selectedSidebarOption}`)
    .addClass("selected");

  const textOption = getLocalStorageItem("text-option", "medium-text");
  $("body").attr("text", textOption);
  $(".offcanvas-body > ul").find(`.${textOption}`).addClass("selected");

  const layoutOption = getLocalStorageItem("layout-option", "rtl");
  if (layoutOption == "box-layout") {
    $("html").attr("dir", "rtl");
    $("body").attr("class", "box-layout rtl");
  } else {
    $("body").attr("class", layoutOption);
    $("html").attr("dir", layoutOption);
  }
  $(".offcanvas-body > ul").find(`.${layoutOption}`).addClass("selected");

  const colorOption = getLocalStorageItem("color-option", "default");
  $(".offcanvas-body > ul").find(`.${colorOption}`).addClass("selected");
  $(".app-wrapper").addClass(colorOption);

  setUpHorizontalHeader();
}

function setColor() {
  const primaryColor = $("#primary_color").val();
  const secondaryColor = $("#secondary_color").val();
  const root = document.querySelector(":root");

  root.style.setProperty("--primary", hexToRGB(primaryColor));
  root.style.setProperty("--secondary", hexToRGB(secondaryColor));
}

// **------ Reset Functionality ------**
function resetCustomizer() {
  const colorOption = getLocalStorageItem("color-option", "default");
  $(".app-wrapper").removeClass(colorOption);
  localStorage.clear();
  window.location.reload();
}

// **------ Convert RGB to HEX ------**
function rgbToHex(r, g, b) {
  return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function componentToHex(c) {
  const hex = c.toString(16);
  return hex.length === 1 ? "0" + hex : hex;
}
