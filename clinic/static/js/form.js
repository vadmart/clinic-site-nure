const URL = "doctor-info";
const necessaryFields = {
    lastname: window["lastname"],
    firstname: window["firstname"],
    contractNum: window["contract"]
};

const formElems = {
    form: window["record-form"],
    familyDoctor: window["family-doctor"],
    dateBlock: window["date"],
    timeBlock: window["time"],
    complaint: window["complaint"],
    submitButton: window["record"],
    clearButton: window["clear"]
}

const plainText = document.createElement("span");
const errSpan = document.createElement("span");
errSpan.className = "err-msg";
errSpan.innerText = "Поле не може бути порожнім";

for (var elem in necessaryFields) {
    necessaryFields[elem].addEventListener("change", checkInvalid);
    necessaryFields[elem].addEventListener("change", (e) => makeRequest(e, URL));
}

formElems.submitButton.addEventListener("click", submitForm);
formElems.clearButton.addEventListener("click", clearForm);


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
    if (!checkNecessary()) return false;
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
        alert("Неможливо створити екземпляр класу XMLHTTP");
        return false;
    }
    httpRequest.open("POST", url);
    httpRequest.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    httpRequest.send(
        `lastname=${necessaryFields.lastname.value}&name=${necessaryFields.firstname.value}&contract_num=${necessaryFields.contractNum.value}`
    );
    httpRequest.onreadystatechange = function () {
        getInfo(event, httpRequest);
    };

    function checkNecessary() {
        for (let elem in necessaryFields) {
            if (!necessaryFields[elem].checkValidity()) {
                return false;
            }
        }
        return true;
    }
}

function getInfo(event, httpRequest) {
    try {
        if (httpRequest.readyState == 4) {
            if (httpRequest.status == 200) {
                console.log(JSON.parse(httpRequest.responseText))
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
    clearFields(formElems.timeBlock, formElems.dateBlock, formElems.familyDoctor);
    if (doctorData["status"] !== "undefined") {
        formElems.form.dataset.personId = doctorData["personId"];
        formElems.form.dataset.doctorId = doctorData["doctorId"];
        plainText.innerText = `${doctorData["lastname"]} ${doctorData["name"]} ${doctorData["patronymic"]}`;
        plainText.className = "doctor-block";
        formElems.familyDoctor.appendChild(plainText);
        showDateTime(doctorData);
    } else {
        plainText.innerText = "не визначено";
        plainText.className = "unknown-block";
        formElems.familyDoctor.appendChild(plainText);
        formElems.dateBlock.appendChild(plainText.cloneNode(true));
        formElems.timeBlock.appendChild(plainText.cloneNode(true));
    }
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
    let min_dt = ""
    let max_dt = ""
    let i = 0
    for (let key in workDatetimeObj) {
        if (!i) {
            min_dt = key
        }
        if (Object.keys(workDatetimeObj).length - 1 == i) {
            max_dt = key
        }
        i++;
    }
    if (min_dt === "") return;
    const calendar = document.createElement("input");
    calendar.type = "date";
    calendar.min = min_dt;
    calendar.max = max_dt;
    calendar.required = true;
    calendar.id = "calendar";
    formElems.dateBlock.appendChild(calendar);
    calendar.addEventListener("change", showTime);

    function showTime(e = null) {
        clearFields(formElems.timeBlock);
        clearIds(document.getElementsByClassName(e.target.className));
        // створюємо кнопки із часом та додаємо у блок часів
        for (var tm of workDatetimeObj[e.target.value]) {
            const timeBtn = document.createElement("input");
            timeBtn.type = "button";
            timeBtn.value = tm;
            timeBtn.id = tm;
            timeBtn.className = "time-button";
            formElems.timeBlock.appendChild(timeBtn);
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
    e.preventDefault();
    if (formElems.form.checkValidity() && document.getElementById("active-time")) {
        const formAJAX = new XMLHttpRequest();
        formAJAX.open("POST", "record");
        formAJAX.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        formAJAX.onreadystatechange = function () {
            if (formAJAX.readyState == 4) {
                if (formAJAX.status == 200) {
                    showModal();
                } else {
                    showModal(false);
                }
            }
        }
        formAJAX.send(`person_id=${formElems.form.dataset.personId}&` +
            `doctor_id=${formElems.form.dataset.doctorId}&` +
            `dt_tm=${window["calendar"].value} ${window["active-time"].value}&` +
            `complaint=${formElems.complaint.value}&` +
            `csrfmiddlewaretoken=${document.querySelector("input[name=csrfmiddlewaretoken]").value}`);
    } else {
        checkTimeButtons();
        showModal(false);
    }

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

    function checkTimeButtons() {
        for (var btn of document.getElementsByClassName("time-button"))
            if (!document.getElementById("active-time")) {
                btn.style.backgroundColor = "red";
            }
    }
}

function clearForm() {
    clearFields(formElems.timeBlock, formElems.dateBlock, formElems.familyDoctor, formElems.complaint);
    plainText.innerText = "не визначено";
    plainText.className = "unknown-block";
    formElems.familyDoctor.appendChild(plainText);
    formElems.dateBlock.appendChild(plainText.cloneNode(true));
    formElems.timeBlock.appendChild(plainText.cloneNode(true));
    window.scrollTo(0, 0);
}