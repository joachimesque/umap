const handleUploadDialog = (linkEl) => {
    let uploadDialogEl = document.getElementById("uploadDialog");

    if (!uploadDialogEl) {
        uploadDialogEl = document.createElement("dialog");
        const dialogDivEl = document.createElement("div");
        const dialogFormEl = document.createElement("form");
        const dialogButtonEl = document.createElement("button");

        uploadDialogEl.id = "uploadDialog";

        dialogDivEl.classList.add("form_holder");
        dialogFormEl.setAttribute("method", "dialog");
        dialogButtonEl.textContent = "Fermer";

        dialogFormEl.append(dialogButtonEl);

        uploadDialogEl.append(dialogFormEl);
        uploadDialogEl.append(dialogDivEl);

        document.body.append(uploadDialogEl);
    }

    uploadDialogEl.showModal();

    let formAction = linkEl.href;

    if (linkEl.hasAttribute("data-dialog-upload-back")) {
        formAction += `&back=${linkEl.dataset.dialogUploadBack}`
    }

    window
        .fetch(`/galerie/upload_form?point=${linkEl.dataset.dialogUpload}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return response.text();
          })
        .then(content => {
            uploadDialogEl.querySelector(".form_holder").innerHTML = content;
            uploadDialogEl.querySelector("form[method='POST']").setAttribute("action", formAction);
            uploadDialogEl.querySelector("form[method='POST']").addEventListener('submit', (e) => {
                e.target.querySelector("[type='submit']").setAttribute('disabled', true);
            })
        })
}

const handleLightbox = (imgEl) => {
    const container = imgEl.closest(".galerie_picture, .content-galerie");
    if (!container) return;

    let lightboxDialogEl = document.getElementById("lightbox");

    if (!lightboxDialogEl) {
        lightboxDialogEl = document.createElement("dialog");
        const dialogDivEl = document.createElement("div");
        const dialogFormEl = document.createElement("form");
        const dialogButtonEl = document.createElement("button");

        lightboxDialogEl.id = "lightbox";

        dialogDivEl.classList.add("img_holder");
        dialogFormEl.setAttribute("method", "dialog");
        dialogButtonEl.textContent = "Fermer";

        dialogFormEl.append(dialogButtonEl);

        lightboxDialogEl.append(dialogFormEl);
        lightboxDialogEl.append(dialogDivEl);

        document.body.append(lightboxDialogEl);
    }

    lightboxDialogEl.showModal();
    lightboxDialogEl.querySelector(".img_holder").innerHTML = `<img src="${imgEl.parentElement.href}" alt="">`;
}

document.addEventListener("click", (e) => {
    if (!!e.metaKey || !!e.ctrlKey) return;

    if (e.target.nodeName == "A" && e.target.hasAttribute("data-dialog-upload")) {
        e.preventDefault();
        handleUploadDialog(e.target);
    }

    if (e.target.nodeName == "IMG" && e.target.hasAttribute("data-lightbox")) {
        e.preventDefault();
        handleLightbox(e.target);
    }
});
