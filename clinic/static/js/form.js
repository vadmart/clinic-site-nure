const URL = "doctor-info";
const errSpan = document.createElement("span");
const dateInputs = document.getElementsByClassName("date");
const timeBlocks = document.getElementsByClassName("appointment-time");

errSpan.className = "err-msg";
errSpan.innerText = "Поле не може бути порожнім";

for (let inp of dateInputs) {
    inp.addEventListener("click", showTime);
}

function showTime(e = null) {
    // створюємо кнопки із часом та додаємо у блок часів
    for (let block of timeBlocks) {
        if (block.classList.contains(e.target.value)) {
            block.style.display = "grid";
        } else {
            block.style.display = "none"
        }
    }
}
