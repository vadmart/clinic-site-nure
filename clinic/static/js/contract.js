const doctorFieldBlock = window["field_id_doctor_fio"];
const searchedInfoBlock = document.createElement("div");
searchedInfoBlock.classList.add("searched-info-block");
doctorFieldBlock.appendChild(searchedInfoBlock);
const doctorField = window["id_doctor_fio"];
doctorField.addEventListener("input", (e) => {
    getEnteredInfo(e)
        .then(arr => {
            removeAllChildren(searchedInfoBlock);
            for (let doctor of arr) {
                const searchedInfoButton = document.createElement("button");
                searchedInfoButton.classList.add("searched-item-button");
                searchedInfoButton.classList.add("doctor-fio");
                searchedInfoButton.innerText = doctor;
                searchedInfoButton.addEventListener("mouseover", (e) => {
                    doctorField.value = e.target.innerText;
                });
                searchedInfoButton.addEventListener("click", (e) => {
                    searchedInfoBlock.removeChild(e.target);
                })
                searchedInfoBlock.appendChild(searchedInfoButton);
            }
        })
        .catch(err => alert(err))
})


async function getEnteredInfo() {
    const response = await fetch("doctor_fio", {
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


