const URL = "doctor-info";

const plainText = document.createElement("span");
const errSpan = document.createElement("span");
errSpan.className = "err-msg";
errSpan.innerText = "Поле не може бути порожнім";

const dateInputs = document.getElementsByClassName("date");
const timeBlocks = document.getElementsByClassName("appointment-time");

for (let inp of dateInputs) {
    inp.addEventListener("click", showTime);
}

Object.compare = function (obj1, obj2) {
    for (var el in obj1) {
        if (obj1.hasOwnProperty(el) !== obj2.hasOwnProperty(el)) return false;
        switch (typeof (obj1[el])) {
            case 'object':
                if (!Object.compare(obj1[el], obj2[el])) return false;
                break;
            case 'function':
                if (typeof (obj2[el]) == 'undefined' || (el != 'compare' && obj1[el].toString() != obj2[el].toString())) return false;
                break;
            default:
                if (obj1[el] != obj2[el]) return false;
        }
    }
    for (var elem in obj2) {
        if (typeof (obj1[elem]) == 'undefined') return false;
    }
    return true;
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

// function submitForm(e) {
//     e.preventDefault();
//     if (formElems.form.checkValidity() && document.getElementById("active-time")) {
//         const formAJAX = new XMLHttpRequest();
//         formAJAX.open("POST", "record");
//         formAJAX.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
//         formAJAX.onreadystatechange = function () {
//             if (formAJAX.readyState == 4) {
//                 if (formAJAX.status == 200) {
//                     showModal();
//                 } else {
//                     showModal(false);
//                 }
//             }
//         }
//         formAJAX.send(`person_id=${formElems.form.dataset.personId}&` +
//             `doctor_id=${formElems.form.dataset.doctorId}&` +
//             `dt_tm=${window["calendar"].value} ${window["active-time"].value}&` +
//             `complaint=${formElems.complaint.value}&` +
//             `csrfmiddlewaretoken=${document.querySelector("input[name=csrfmiddlewaretoken]").value}`);
//     } else {
//         checkTimeButtons();
//         showModal(false);
//     }

function showModal(isValid = true) {
    const popUp = document.getElementById("popup");
    const popupTitle = document.querySelector(".popup__title");
    const popupText = document.querySelector(".popup__text");
    const modalCloseButton = document.querySelector(".popup__close");
    if (!isValid) {
        popupTitle.innerText = "Помилка";
        popupTitle.style.color = "rgb(217, 36, 36)";
        popupText.innerText = "Дані на сервер НЕ відправлені. Перевірте, будь-ласка, правильність введених полів або з'єднання та спробуйте ще";
    } else {
        popupTitle.innerText = "Успіх!";
        popupTitle.style.color = "rgb(36, 217, 36)";
        popupText.innerText = "Запис на прийом вже передано. Скорішого Вам одужання:)";
    }
    popUp.classList.add("open");
    modalCloseButton.addEventListener("click", closeModal)

    function closeModal(e) {
        if (!isValid) e.preventDefault();
        popUp.classList.remove("open");
    }
}
