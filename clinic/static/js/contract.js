for (let radio of document.getElementsByClassName("choose-way-radio")) {
    radio.addEventListener("change", (ev) => {
            try {
                document.getElementsByClassName("chosen")[0].classList.remove("chosen");
            } catch (e) {
            }
            ev.target.parentNode.classList.add("chosen");
    })
}

const doctorFieldBlock = window["doctor-block"];
const searchedInfoBlock = document.createElement("div");
searchedInfoBlock.classList.add("searched-info-block");
searchedInfoBlock.classList.add("hidden");
doctorFieldBlock.appendChild(searchedInfoBlock);
const doctorField = window["id_doctor_lfp"];
doctorField.addEventListener("input", (e) => {
    getEnteredInfo(e)
        .then(arr => {
            if (arr.length != 0) {
                doctorField.style.borderBottom = "none";
                doctorField.style.borderBottomLeftRadius = "0";
                doctorField.style.borderBottomRightRadius = "0";
                searchedInfoBlock.classList.remove("hidden");
            } else {
                doctorField.style = "";
                searchedInfoBlock.classList.add("hidden");
            }
            removeAllChildren(searchedInfoBlock);
            for (let doctor of arr) {
                const searchedInfoButton = document.createElement("button");
                searchedInfoButton.classList.add("searched-item-button");
                searchedInfoButton.innerText = doctor;
                searchedInfoButton.addEventListener("click", (e) => {
                    doctorField.value = e.target.innerText;
                    doctorField.style = "";
                    searchedInfoBlock.classList.add("hidden");
                    removeAllChildren(searchedInfoBlock);
                })
                searchedInfoBlock.appendChild(searchedInfoButton);
            }
        })
        .catch(err => {
        })
})


async function getEnteredInfo() {
    const response = await fetch("doctor_lfp", {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        headers: {
            "Content-Type": "application/json"
        },
        referrerPolicy: "no-referrer",
        body: doctorField.value
    });
    return (await response.json())["searchedDoctors"];
}

function removeAllChildren(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}


