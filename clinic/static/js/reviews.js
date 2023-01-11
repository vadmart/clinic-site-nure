const reviewOptions = {
    backgroundColor: window["background"],
    fontSize: window["font-size"],
    fontType: window["font-type"],

};

const reviewCommentsBlocks = document.getElementsByClassName("review comment");
const comments = document.getElementsByClassName("comment");
const defaultButton = window["default-button"];


setSettings();

defaultButton.addEventListener("click", () => {
    setBackgroundColor("");
    setFontType("");
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
    for (let block of reviewCommentsBlocks) {
        block.style.backgroundColor = val;
    }
}

function setFontSize(val) {
    for (let comm of comments) {
        comm.style.fontSize = val;
    }
}

function setFontType(val) {
    for (let comm of comments) {
        comm.style.fontFamily = `Inter, ${val}`;
    }
}

