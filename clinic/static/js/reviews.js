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
