function showPopup(popupId) {
    let overlay = document.getElementById(`${popupId}-overlay`);

    if (overlay === null) {
        return;
    }

    overlay.style.display = "block"
    document.body.style.overflow = "hidden";
}

function closePopup(popupId) {
    let overlay = document.getElementById(`${popupId}-overlay`);

    if (overlay === null) {
        return;
    }

    overlay.style.display = "none"
    document.body.style.overflow = "auto";

}