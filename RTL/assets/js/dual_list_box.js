// Dual Listbox Initializations
const dlb1 = new DualListbox(".select1", {
  availableTitle: "انتخاب های دردسترس",
  selectedTitle: "موارد انتخاب شده",
  searchPlaceholder: "جستجو",
  addButtonText: "افزودن",
  removeButtonText: "حذف",
  addAllButtonText: "افزودن همه",
  removeAllButtonText: "حذف همه",
});

const dlb2 = new DualListbox(".select2", {
  availableTitle: "اعداد دردسترس",
  selectedTitle: "اعداد انتخاب شده",
  addButtonText: ">",
  removeButtonText: "<",
  addAllButtonText: ">>",
  removeAllButtonText: "<<",
  searchPlaceholder: "جستجوی عدد",
  enableDoubleClick: false,
});

dlb2.addEventListener("added", (event) => {
  document.querySelector(".changed-element").innerHTML =
    event.addedElement.outerHTML;
});

dlb2.addEventListener("removed", (event) => {
  document.querySelector(".changed-element").innerHTML =
    event.removedElement.outerHTML;
});

const dlb3 = new DualListbox(".select3", {
  showAddButton: false,
  showAddAllButton: false,
  showRemoveButton: false,
  showRemoveAllButton: false,
  availableTitle: "انتخاب های دردسترس",
  selectedTitle: "موارد انتخاب شده",
  searchPlaceholder: "جستجو",
  addButtonText: "افزودن",
  removeButtonText: "حذف",
  addAllButtonText: "افزودن همه",
  removeAllButtonText: "حذف همه",
});

const dlb4 = new DualListbox(".select4", {
  showSortButtons: true,
  availableTitle: "انتخاب های دردسترس",
  selectedTitle: "موارد انتخاب شده",
  searchPlaceholder: "جستجو",
  addButtonText: "افزودن",
  removeButtonText: "حذف",
  addAllButtonText: "افزودن همه",
  removeAllButtonText: "حذف همه",
  upButtonText: "بالا",
  downButtonText: "پایین",
});

// Toggle Source Code Blocks
const sources = document.querySelectorAll(".source");
sources.forEach((sourceEl) => {
  sourceEl.addEventListener("click", (event) => {
    const code = document.querySelector(
      "." + event.currentTarget.dataset.source
    );
    if (code) {
      code.classList.toggle("open");
    }
  });
});
