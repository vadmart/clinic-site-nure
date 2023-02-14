export let ReviewForm = {
    lastnameField: window["lastname"],
    nameField: document.getElementById("name"),
    contractNumField: window["contract-num"],
    textArea: window["review-text"],
    send: document.querySelector("input[type=submit]"),
    addHandlerForAll(callback) {
        this.lastnameField.addEventListener("change", callback);
        this.nameField.addEventListener("change", callback);
        this.contractNumField.addEventListener("change", callback);
        this.lastnameField.addEventListener("change", callback);
    },
    areNecessaryFieldsFull() {
        return this.lastnameField.value != "" && this.nameField.value != "" && this.contractNumField.value != "";
    },
    patientWithoutContract() {
        ReviewForm._setAlertFont();
        this.textArea.innerText = "Для залишення відгуків про цього доктора необхідно заключити з ним контракт";
        this.textArea.disabled = true;
    },
    unlockReviewArea() {
        ReviewForm._setDefaultFont();
        this.textArea.innerText = "";
        this.textArea.disabled = false;
    },
    _setDefaultFont() {
        this.textArea.style = ""
    },
    _setAlertFont() {
        this.textArea.style.fontType = "italic";
        this.textArea.style.textAlign = "center";
    }
}