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
    for (let appointment of document.getElementsByClassName("appointment-cabinet")) {
        appointment.classList.add("hidden");
    }
    for (let timeBlock of timeBlocks) {
        if (timeBlock.classList.contains(e.target.value)) {
            timeBlock.classList.remove("hidden");
            timeBlock.querySelector("input").addEventListener("click", showCabinet);
        } else {
            timeBlock.classList.add("hidden");
        }
    }
}

function showCabinet(e) {
    for (let appointment of document.getElementsByClassName("appointment-cabinet")) {
        if (appointment.id.split(" ")[0] === e.target.id)
            appointment.classList.remove("hidden");
        else appointment.classList.add("hidden");
    }
}
