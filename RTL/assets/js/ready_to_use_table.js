$(function () {
  $("#exampledatatable").DataTable({
    language: {
      url: "assets/vendor/datatable/fa.json",
    },
  });
  $("#exampledatatable1").DataTable({
    language: {
      url: "assets/vendor/datatable/fa.json",
    },
  });
  $("#exampledatatable2").DataTable({
    language: {
      url: "assets/vendor/datatable/fa.json",
    },
  });
  $("#exampledatatable3").DataTable({
    language: {
      url: "assets/vendor/datatable/fa.json",
    },
  });
  $("#exampledatatable4").DataTable({
    language: {
      url: "assets/vendor/datatable/fa.json",
    },
  });
});

// checkbox js
const selectAllCheckbox = document.getElementById("select-all");

if (selectAllCheckbox) {
  selectAllCheckbox.addEventListener("click", () => {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const isChecked = selectAllCheckbox.checked;

    checkboxes.forEach((checkbox) => {
      checkbox.checked = isChecked;
    });
  });
}
