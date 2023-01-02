const URL = "../json/info.json";
const necessaryFields = {
    lastname: window["lastname"],
    firstname: window["firstname"],
    contractNum: window["contract"]
};

for (var elem in necessaryFields) {
    necessaryFields[elem].addEventListener("change", checkInvalid);
    necessaryFields[elem].addEventListener("change", (e) => makeRequest(e, URL));
}

const familyDoctor = document.getElementById("family-doctor");
const date = document.getElementById("date");
const time = document.getElementById("time");

const clear = document.getElementById("clear");
clear.addEventListener("click", clearForm);

const submitButton = document.getElementById("record");
submitButton.addEventListener("click", (e) => {
    submitForm(e);
});

const complaint = document.getElementById("complaint");

const plainText = document.createElement("span");

const errSpan = document.createElement("span");
errSpan.className = "err-msg";
errSpan.innerText = "Поле не може бути порожнім";

console.log(window.lastname);

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


function makeRequest(event, url) {
    var httpRequest = false;
    if (window.XMLHttpRequest) {
        httpRequest = new XMLHttpRequest();
        if (httpRequest.overrideMimeType) {
            httpRequest.overrideMimeType("text/xml");
        }
    } else if (window.ActiveXObject) {
        httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (!httpRequest) {
        alert("Невозможно создать экземпляр класса XMLHTTP");
        return false;
    }
    httpRequest.onreadystatechange = function () {
        getInfo(event, httpRequest);
    };
    httpRequest.open("POST", url);
    httpRequest.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    httpRequest.send(null);
}

function getInfo(event, httpRequest) {
    try {
        if (httpRequest.readyState == 4) {
            if (httpRequest.status == 200) {
                showDoctor(event, JSON.parse(httpRequest.responseText));
            } else {
                alert("Із запитом виникла проблема");
            }
        }
    } catch
        (e) {
        alert("Було призведено виняток " + e.description);
    }
}



function showDoctor(e, doctorData) {
    clearFields(time, date, familyDoctor);
    const patient = {
        "lastName": necessaryFields.lastname.value,
        "firstName": necessaryFields.firstname.value,
        "contractNum": necessaryFields.contractNum.value
    };
    const doctor = findDoctor(patient, doctorData);
    if (doctor) {
        plainText.innerText = doctor;
        plainText.className = "doctor-block";
        familyDoctor.appendChild(plainText);
        showDateTime(doctorData[doctor]);
    } else {
        plainText.innerText = "не визначено";
        plainText.className = "unknown-block";
        familyDoctor.appendChild(plainText);
        date.appendChild(plainText.cloneNode(true));
        time.appendChild(plainText.cloneNode(true));
    }
}

function findDoctor(patient, doctorData) {
    for (var doctor in doctorData) {
        for (var pat of doctorData[doctor]["patients"]) {
            if (Object.compare(pat, patient)) {
                return doctor;
            }
        }
    }
    return null;
}

function checkInvalid(event) {
    if (!event.target.checkValidity() && !document.querySelector(`#${event.target.parentNode.id} .err-msg`)) {
        event.target.parentNode.append(errSpan.cloneNode(true));
        return false;
    } else if (event.target.checkValidity() && document.querySelector(`#${event.target.parentNode.id} .err-msg`)) {
        event.target.parentNode.removeChild(document.querySelector(`#${event.target.parentNode.id} .err-msg`));
    }
    return true;
}

function clearFields(...fields) {
    for (var field of fields) {
        while (field.firstChild) {
            field.removeChild(field.firstChild);
        }
    }
}

function showDateTime(doctorInfo) {
    const workDatetimeObj = doctorInfo["workSchedule"];
    const calendar = document.createElement("input");
    var min_date_value = "2500-01-01";
    var max_date_value = "";
    calendar.type = "date";
    for (var dt in workDatetimeObj) {
        if (dt > max_date_value) max_date_value = dt;
        if (dt < min_date_value) min_date_value = dt;
    }
    calendar.min = min_date_value;
    calendar.max = max_date_value;
    calendar.required = true;
    calendar.id = "calendar";
    date.appendChild(calendar);
    calendar.addEventListener("change", showTime);

    function showTime(e = null) {
        clearFields(time);
        clearIds(document.getElementsByClassName(e.target.className));
        // створюємо кнопки із часом та додаємо у блок часів
        for (var tm of workDatetimeObj[e.target.value]) {
            const timeBtn = document.createElement("input");
            timeBtn.type = "button";
            timeBtn.value = tm;
            timeBtn.id = tm;
            timeBtn.className = "time-button";
            time.appendChild(timeBtn);
            timeBtn.addEventListener("click", function (e) {
                // убирати id кнопок часу при натисканні на одну з них
                clearIds(document.getElementsByClassName(e.target.className));
                e.target.id = "active-time";
                // убирати колір на випадок, якщо кнопки червоні
                for (var btn of document.getElementsByClassName(e.target.className)) {
                    btn.style.backgroundColor = "";
                }
            });
        }
    }

    function clearIds(elems) {
        for (var elem of elems) {
            elem.id = "";
        }
    }
}

function submitForm(e) {
    const form = document.querySelector(".form-container form");
    if (form.checkValidity() && document.getElementById("active-time")) {
        showModal();
        e.preventDefault();
    } else {
        checkTimeButtons();
        showModal(false);
        return
    }
    const dt = document.getElementById("calendar").value.split("-").map((elem) => Number(elem));
    const tm = document.getElementById("active-time").value.split(":").map((elem) => Number(elem));
    const obj = JSON.stringify({
        firstName: necessaryFields.firstname.value,
        lastName: necessaryFields.lastname.value,
        contractNum: necessaryFields.contractNum.value,
        familyDoctor: familyDoctor.innerText,
        dateTime: new Date(dt[0], dt[1] - 1, dt[2], tm[0] + 2, tm[1]),
        complaint: complaint.value
    });

    function showModal(isValid = true) {
        const popUp = document.getElementById("popup");
        const popupTitle = document.querySelector(".popup__title");
        const popupText = document.querySelector(".popup__text");
        const modalCloseButton = document.querySelector(".popup__close");
        if (!isValid) {
            popupTitle.innerText = "Помилка";
            popupTitle.style.color = "rgb(217, 36, 36)";
            popupText.innerText = "Дані на сервер НЕ відправлені. Перевірте, будь-ласка, правильність введених полів та спробуйте ще";
        } else {
            popupTitle.innerText = "Успіх!";
            popupTitle.style.color = "rgb(36, 217, 36)";
            popupText.innerText = "Запис на прийом вже передано. Скорішого Вам одужання:)";
        }
        popUp.classList.add("open");
        modalCloseButton.addEventListener("click", closeModal)

        function closeModal(e) {
            e.preventDefault();
            popUp.classList.remove("open");
        }
    }

    function checkTimeButtons() {
        for (var btn of document.getElementsByClassName("time-button"))
            if (!document.getElementById("active-time")) {
                btn.style.backgroundColor = "red";
            }
    }

    console.log(obj);
}

function clearForm() {
    clearFields(time, date, familyDoctor, complaint);
    plainText.innerText = "не визначено";
    plainText.className = "unknown-block";
    familyDoctor.appendChild(plainText);
    date.appendChild(plainText.cloneNode(true));
    time.appendChild(plainText.cloneNode(true));
    window.scrollTo(0, 0);
}