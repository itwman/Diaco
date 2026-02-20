// ---- code copy js ---- //
const shadowBoxes = document.querySelectorAll(".box-shadow-box"); // Cache DOM node access

shadowBoxes.forEach(box => {
    box.addEventListener("click", () => {
        try {
            const classNameToCopy = box.classList[1];
            copyTextToClipboard(classNameToCopy);

            Toastify({
                text: "نام کلاس با موفقیت کپی شد.",
                duration: 3000,
                close: true,
                gravity: "top",
                position: "left",
                stopOnFocus: true,
                style: { background: "rgba(var(--success),1)" },
                onClick: function () {}
            }).showToast();
        } catch (error) {
            console.error("Error copying class name:", error);
            Toastify({
                text: "خطایی رخ داده است",
                duration: 3000,
                close: true,
                gravity: "top",
                position: "left",
                stopOnFocus: true,
                style: { background: "rgba(var(--danger),1)" },
                onClick: function () {}
            }).showToast();
        }
    });
});
