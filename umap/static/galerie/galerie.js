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
        const dialogButtonsHolder = document.createElement('div');
        const dialogNextEl = document.createElement("button");
        const dialogPrevEl = document.createElement("button");

        lightboxDialogEl.id = "lightbox";

        dialogDivEl.classList.add("img_holder");
        dialogFormEl.setAttribute("method", "dialog");
        dialogButtonEl.textContent = "Fermer";

        dialogButtonsHolder.classList.add('navigation')
        dialogNextEl.setAttribute('type', 'button');
        dialogNextEl.addEventListener('click', handleNextClick);
        dialogNextEl.innerHTML = "<span>Suivante</span>";
        dialogPrevEl.setAttribute('type', 'button');
        dialogPrevEl.addEventListener('click', handlePrevClick);
        dialogPrevEl.innerHTML = "<span>Précédente</span>";

        dialogButtonsHolder.append(dialogPrevEl, dialogNextEl);
        dialogFormEl.append(dialogButtonEl);

        lightboxDialogEl.append(dialogFormEl, dialogDivEl, dialogButtonsHolder);

        document.body.append(lightboxDialogEl);
    }

    lightboxDialogEl.showModal();
    updateLightboxImage(imgEl.parentElement.href);
    const galleryUrls = [...imgEl.closest(".galerie_picture-list, .content-galerie, .point_pictures").querySelectorAll("a[href]:has(img)")].map(i => i.href);
    window.lightbox_current_urls = galleryUrls;

    lightboxDialogEl.addEventListener('keydown', handleLightboxKeydown)
    lightboxDialogEl.addEventListener('close', () => {
        lightboxDialogEl.removeEventListener('keydown', handleLightboxKeydown)
    })
}

const handleLightboxKeydown = e => {
    if (e.key == "Escape") { document.querySelector("#lightbox")?.close() };
    if (e.key == "ArrowLeft") { handlePrevClick() };
    if (e.key == "ArrowRight") { handleNextClick() };
}

const handleNextClick = () => {
    const currentIndex = window.lightbox_current_urls.indexOf(window.lightbox_current_img);
    let newIndex = currentIndex + 1;
    if (newIndex > window.lightbox_current_urls.length - 1) {
        newIndex = 0;
    }
    updateLightboxImage(window.lightbox_current_urls[newIndex]);
}
const handlePrevClick = () => {
    const currentIndex = window.lightbox_current_urls.indexOf(window.lightbox_current_img);
    let newIndex = currentIndex - 1;
    if (newIndex < 0) {
        newIndex = window.lightbox_current_urls.length - 1
    }
    updateLightboxImage(window.lightbox_current_urls[newIndex]);
}

const updateLightboxImage = (imgUrl) => {
    const imageHolder = document.querySelector("#lightbox .img_holder");
    if (!imageHolder) return;
    imageHolder.innerHTML = `<img src="${imgUrl}" alt="">`;
    window.lightbox_current_img = imgUrl;
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
