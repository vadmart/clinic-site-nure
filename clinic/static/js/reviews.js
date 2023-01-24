import {ReviewForm} from "./reviewForm.js";


const reviewOptions = {
    backgroundColor: window["background"],
    fontSize: window["font-size"],
    fontType: window["font-type"],

};

const accounts = document.getElementsByClassName("account");
const comments = document.getElementsByClassName("comment");
const reviews = document.getElementsByClassName("review");
const defaultButton = window["default-button"];
const reviewsMenu = document.querySelector(".reviews .reviews__menu");
if (!reviews.length) {
    reviewsMenu.style.display = "none";
}

const addReviewButton = document.querySelector(".feedback_btn");
addReviewButton.addEventListener("click", showModal);

setSettings();

defaultButton.addEventListener("click", () => {
    setBackgroundColor("");
    setFontType("serif");
    setFontSize("");
    localStorage.clear();
})

reviewOptions.backgroundColor.addEventListener("change", (e) => {
    setBackgroundColor(e.target.value);
    if (e.target.value) {
        localStorage["backgroundColor"] = e.target.value;
    } else {
        localStorage.removeItem("backgroundColor");
    }
    e.preventDefault();
})

reviewOptions.fontSize.addEventListener("change", (e) => {
    setFontSize(e.target.value);
    localStorage["fontSize"] = e.target.value;
    e.preventDefault();
})

reviewOptions.fontType.addEventListener("change", (e) => {
    setFontType(e.target.value);
    localStorage["fontType"] = e.target.value;
    e.preventDefault();
})


function setSettings() {
    if (localStorage.backgroundColor) {
        setBackgroundColor(localStorage.backgroundColor);
        reviewOptions.backgroundColor.value = localStorage.backgroundColor;
    }
    if (localStorage.fontSize) {
        setFontSize(localStorage.fontSize);
        reviewOptions.fontSize.value = localStorage.fontSize;
    }
    if (localStorage.fontType) {
        setFontType(localStorage.fontType);
        reviewOptions.fontType.value = localStorage.fontType;
    }
}

function setBackgroundColor(val) {
    for (let block of reviews) {
        block.style.backgroundColor = val;
    }
}

function setFontSize(val) {
    for (let acc of accounts) {
        for (let ch of acc.children) {
            ch.style.fontSize = val;
        }
    }
    for (let comm of comments) {
        comm.style.fontSize = val;
    }
}

function setFontType(val) {
    for (let acc of accounts) {
        for (let ch of acc.children) {
            ch.style.fontFamily = `Inter, ${val}`;
        }
    }
    for (let comm of comments) {
        comm.style.fontFamily = `Inter, ${val}`;
    }
}

function showModal(e) {
    const reviewWrapper = document.querySelector(".review-blank-wrapper");
    const closeButton = document.querySelector(".close-button");
    reviewWrapper.classList.remove("hidden");
    closeButton.addEventListener("click", (e) => {
        reviewWrapper.classList.add("hidden");
        e.preventDefault();
    })
    e.preventDefault();
}

ReviewForm.addHandlerForAll(sendPersonData);
function sendPersonData() {
    let personData = false
    if (!ReviewForm.areNecessaryFieldsFull()) return;
    if (window.XMLHttpRequest) {
        personData = new XMLHttpRequest();
        if (window.overrideMimeType) {
            personData.overrideMimeType("text/xml");
        }
    } else if (window.ActiveXObject) {
        personData = new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (!personData) {
        alert("Неможливо створити екземпляр класу XMLHttp");
        return false;
    }
    personData.open("POST", "check-person");
    personData.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    personData.send(`lastname=${ReviewForm.lastnameField.value}&` +
        `name=${ReviewForm.nameField.value}&` +
        `contract_num=${ReviewForm.contractNumField.value}&` +
        `doctor_id=${document.querySelector(".review-blank form").dataset.doctorId}`);
    personData.onreadystatechange = function () {
        if (personData.readyState == 4) {
            if (personData.status == 200) {
                const receivedData = JSON.parse(personData.responseText);
                if (receivedData.status == "canLeaveReview") {
                    ReviewForm.unlockReviewArea();
                } else if (receivedData.status == "didntVisitADoctor") {
                    ReviewForm.patientWithoutVisits();
                } else {
                    ReviewForm.patientIsNotInDB();
                }
            }
        }
    }
}
