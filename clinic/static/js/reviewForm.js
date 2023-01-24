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
    patientIsNotInDB() {
        ReviewForm._setAlertFont();
        this.textArea.innerText = "Необхідно заключити контракт із цим лікарем та відвідати хоча б 1 раз"
        this.textArea.disabled = true;
    },
    patientWithoutVisits() {
        ReviewForm._setAlertFont();
        this.textArea.innerText = "Необхідно відвідати цього лікаря щонайменш 1 раз";
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