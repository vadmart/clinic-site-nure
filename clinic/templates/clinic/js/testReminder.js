if (localStorage.isTestFailed) {
    const closePopupButton = document.querySelector(".reminder-popup__close");
    window["reminder-popup"].classList.add("open");
    closePopupButton.addEventListener("click", (e) => {
        window["reminder-popup"].classList.remove("open");
        e.preventDefault();
    })
}