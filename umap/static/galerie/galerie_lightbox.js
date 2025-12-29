const pictureEls = document.querySelectorAll(".galerie_picture a:has(img)");
document.addEventListener("click", (e) => {
    if (!!e.metaKey || !!e.ctrlKey) return;
    if (e.originalTarget.nodeName != "IMG") return;
    if (e.originalTarget.parentElement.nodeName != "A") return;

    const container = e.originalTarget.closest(".galerie_picture, .content-galerie");
    if (!container) return;

    e.preventDefault();

    let dialogEl = document.getElementById("lightbox");

    if (!dialogEl) {
        dialogEl = document.createElement("dialog");
        const dialogDivEl = document.createElement("div");
        const dialogFormEl = document.createElement("form");
        const dialogButtonEl = document.createElement("button");

        dialogEl.id = "lightbox";

        dialogDivEl.classList.add("img_holder");
        dialogFormEl.setAttribute("method", "dialog");
        dialogButtonEl.textContent = "Fermer";

        dialogFormEl.append(dialogButtonEl);

        dialogEl.append(dialogFormEl);
        dialogEl.append(dialogDivEl);

        document.body.append(dialogEl);
    }

    dialogEl.showModal();
    dialogEl.querySelector(".img_holder").innerHTML = `<img src="${e.originalTarget.parentElement.href}" alt="">`;
});
