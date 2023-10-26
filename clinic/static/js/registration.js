const contractSenderButton = document.getElementById("registration-contract-num-button");
const contractSenderButtonText = document.querySelector("button#registration-contract-num-button i");
const contractField = window["registration-contract-num"];
const submitButton = document.querySelector(".form-actions input[type=submit]");
let timerDeadline = 0;
let timerID = 0;
let contractNum = null;

contractSenderButton.addEventListener("click", getContractNum);

submitButton.addEventListener("click", () => {
    if (contractNum !== contractField.value) {
        contractField.setCustomValidity("Введите номер контракта из СМС");
        return
    }
    contractField.setCustomValidity("");
})


function getContractNum(e) {
    const phoneNumber = window["registration-phone-num"].value;
    console.log(phoneNumber)
    // if (!phoneNumber) {
    //     window["registration-phone-num"].setCustomValidity("Set your phone number");
    //     return;
    // } else if (window["registration-phone-num"].validity.patternMismatch) {
    //     window["registration-phone-num"].setCustomValidity("Set your phone number in a format +38XXXXXXXXXX");
    //     return
    // }
    if (!phoneNumber || window["registration-phone-num"].validity.patternMismatch) return
    const xhr = new XMLHttpRequest();
    xhr.open("post", "send_contract_num");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                contractNum = xhr.responseText;
                window["ajax-info"].innerText = "Номер контракту готовий до валідації";
                window["ajax-info"].classList.add("green");
                window["ajax-info"].classList.remove("red")
            } else {
                window["ajax-info"].innerText = "Щось пішло не так. Спробуйте зареєструватися пізніше";
                window["ajax-info"].classList.add("red");
                window["ajax-info"].classList.remove("green");
            }
        }
    }
    xhr.send(`phone_number=${phoneNumber}`);

    timerDeadline = new Date();
    timerDeadline.setSeconds(timerDeadline.getSeconds() + 15);
    contractSenderButton.disabled = true;
    timerID = setInterval(countdownTimer, 1000);
    e.preventDefault();
}

function countdownTimer() {
    const diff = timerDeadline - new Date();
    if (diff < 0) {
        clearInterval(timerDeadline);
        contractSenderButton.disabled = false;
        contractSenderButtonText.innerText = "Отримати номер контракту";
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

