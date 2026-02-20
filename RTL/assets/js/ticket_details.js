// File upload js
const fileInput = document.querySelector(".ticket-file-upload");

if (fileInput) {
  try {
    FilePond.create(fileInput, {
      labelIdle: `
                <i class="fa-solid fa-cloud-arrow-up me-2 f-s-30 mb-3 text-primary"></i>
                <p class="f-s-18">یک فایل انتخاب کنید</p>
                <p class="f-s-14 text-secondary text-center pe-3 ps-3"> فرمت مجاز : JPEG, PNG , PDF , حداکثر  50 مگابایت</p>
                <p class="btn btn-lg file-btn btn-primary mt-3 f-s-14">انتخاب فایل</p>
            `,
      acceptedFileTypes: ["image/jpeg", "image/png", "application/pdf"],
      maxFileSize: "50MB",
    });
  } catch (error) {
    console.error("FilePond initialization failed:", error);
  }
}

// Editor js
$("#editor-1").trumbowyg({
  lang: "fa",
  btns: [
    ["viewHTML"],
    ["undo", "redo"], // Only supported in Blink browsers
    ["formatting"],
    ["strong", "em", "del"],
    ["superscript", "subscript"],
    ["justifyLeft", "justifyCenter", "justifyRight", "justifyFull"],
    ["unorderedList", "orderedList"],
    ["horizontalRule"],
    ["removeformat"],
    ["fullscreen"],
  ],
});
