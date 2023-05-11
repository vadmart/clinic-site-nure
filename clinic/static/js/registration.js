const contractSenderButton = document.getElementById("registration-contract-num-button");
const contractSenderButtonText = document.querySelector("button#registration-contract-num-button i");
const contractField = window["registration-contract-num"];
const submitButton = document.querySelector(".form-actions input[type=submit]");
let timerDeadline = 0;
let timerID = 0;
let contractNum = null;

contractSenderButton.addEventListener("click", (e) => {
    window["registration-phone-num"].setCustomValidity("");
    const phoneNumber = window["registration-phone-num"].value;
    if (!phoneNumber) {
        window["registration-phone-num"].setCustomValidity("Укажите номер телефона");
        return;
    } else if (window["registration-phone-num"].validity.patternMismatch) {
        window["registration-phone-num"].setCustomValidity("Укажите номер телефона в формате +38XXXXXXXXXX");
        return
    }
    fetch("send_contract_num", {
        "method": "POST",
        "mode": "same-origin",
        "credentials": "same-origin",
        "headers": {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        "body": JSON.stringify(
            {
                "phone_number": phoneNumber
            })
    })
        .then((response) => response.text())
        .then((data) => contractNum = data)
        .catch((err) => console.error("Помилка " + err));
    timerDeadline = new Date();
    timerDeadline.setSeconds(timerDeadline.getSeconds() + 15);
    contractSenderButton.disabled = true;
    timerID = setInterval(countdownTimer, 1000);
    e.preventDefault();
})

submitButton.addEventListener("click", () => {
    if (contractNum !== contractField.value) {
        contractField.setCustomValidity("Введите номер контракта из СМС");
        return
    }
    contractField.setCustomValidity("");
})

function countdownTimer() {
    const diff = timerDeadline - new Date();
    if (diff < 0) {
        clearInterval(timerDeadline);
        contractSenderButton.disabled = false;
        contractSenderButtonText.innerHTML = "<i>Відправити номер контракту</i>";
        return;
    }
    const minutes = diff > 0 ? Math.floor(diff / 1000 / 60) : 0;
    const seconds = (diff > 0 ? Math.floor(diff / 1000) % 60 : 0).toString().padStart(2, "0");
    contractSenderButtonText.innerText = `Повторити через ${minutes}:${seconds}`;
}

function getCookie(name) {
    if (!document.cookie) {
        return null;
    }
    return document.cookie.split(";")
        .map(el => el.trim())
        .filter(el => el.startsWith(name + "="))[0].split("=")[1];
}

