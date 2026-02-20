// **------ Table 1 ------**
$(function () {
  $("#example").DataTable({
    language: {
      url: "assets/vendor/datatable/fa.json",
    },
  });
  $("#example1").DataTable({
    language: {
      url: "assets/vendor/datatable/fa.json",
    },
  });
});

$(function () {
  $("#example2").DataTable({
    language: {
      url: "assets/vendor/datatable/fa.json",
    },
    dom: "Bfrtip",
    buttons: ["کپی", "سی اس وی", "اکسل", "پی دی اف", "پرینت"],
  });
});

$(function () {
  $("#example3").DataTable({
    language: {
      url: "assets/vendor/datatable/fa.json",
    },
    createdRow: function (row, data) {
      const salary = parseFloat(data[5].replace(/[\$,]/g, ""));
      if (salary > 150000) {
        $("td", row).eq(5).addClass("highlight");
      }
    },
  });
});

/* Formatting function for row details - modify as needed */
function format(d) {
  return `
    <table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">
      <tr>
        <td>نام کامل:</td>
        <td>${d.name}</td>
      </tr>
      <tr>
        <td>شماره:</td>
        <td>${d.extn}</td>
      </tr>
      <tr>
        <td>اطلاعات :</td>
        <td>اطلاعات و جزئیات دیگر...</td>
      </tr>
    </table>`;
}

$(function () {
  const table = $("#example4").DataTable({
    language: {
      url: "assets/vendor/datatable/fa.json",
    },
    ajax: "assets/vendor/datatable/ajax/objects.txt",
    rowId: "id",
    columns: [
      {
        className: "dt-control",
        orderable: false,
        data: null,
        defaultContent: "",
      },
      { data: "name" },
      { data: "position" },
      { data: "office" },
      { data: "salary" },
    ],
    order: [[1, "asc"]],
    dom: "Blfrtip",
    buttons: ["createState", "savedStates"],
  });

  // Open/close row details
  $("#example4").on("click", "tbody td.dt-control", function () {
    const tr = $(this).closest("tr");
    const row = table.row(tr);

    if (row.child.isShown()) {
      row.child.hide();
    } else {
      row.child(format(row.data())).show();
    }
  });

  $("#example4").on("requestChild.dt", function (e, row) {
    row.child(format(row.data())).show();
  });

  table.on("stateLoaded", (e, settings, data) => {
    for (let i = 0; i < data.childRows.length; i++) {
      const row = table.row(data.childRows[i]);
      row.child(format(row.data())).show();
    }
  });
});

// Delete btn JS
document.addEventListener("DOMContentLoaded", () => {
  const table = document.querySelector("table");

  if (table) {
    table.addEventListener("click", (event) => {
      const target = event.target;

      if (target.classList.contains("delete-btn")) {
        const row = target.closest("tr");
        if (row) {
          row.remove();
        }
      }
    });
  }
});
