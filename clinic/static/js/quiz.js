var qa = null;
const formWrapper = document.querySelector(".form-wrapper");
const form = document.querySelector(".form");
const fieldset = window["form__content"];
let formTitle = window["form__title"];
const formVariants = window["form__variants"];
const nextButton = document.querySelector(".form__button");
const variantsBlock = document.getElementById("form__variants");
let ind = 2;

function receiveQuestions(method, requestURL) {
    return new Promise((resolve, reject) => {
            let ajax_obj = new XMLHttpRequest();
            ajax_obj.open(method, requestURL);
            ajax_obj.responseType = "json";
            ajax_obj.setRequestHeader("Content-Type", "application/json");
            ajax_obj.onload = function () {
                if (ajax_obj.status >= 400) {
                    reject(ajax_obj.response)
                } else {
                    resolve(ajax_obj.response);
                }
            }
            ajax_obj.onerror = () => {
                console.error(ajax_obj.response);
            }
            ajax_obj.send(null);
        }
    )
}

receiveQuestions("POST", "get-questions")
    .then(data => {
        qa = data;
        form.classList.remove("hidden");
        document.getElementById("loader").classList.add("hidden");
        getQuestion(qa[1]["question"], qa[1]["correctAnswers"], qa[1]["incorrectAnswers"], qa[1]["inputType"]);
    })
    .catch(err => console.error(err));


nextButton.addEventListener("click", switchQuestions);

function switchQuestions(e) {
    e.preventDefault();
    if (!validateAnswer(ind - 1)) {
        form.style.backgroundColor = "rgba(220, 70, 50, 0.6)";
        fieldset.style.backgroundColor = "rgba(220, 70, 50, 0.6)";
        alert("Оберіть варіант відповіді!");
        return;
    }
    form.style.backgroundColor = "";
    fieldset.style.backgroundColor = "";
    if (ind <= Object.keys(qa).length) {
        getQuestion(qa[ind]["question"], qa[ind]["correctAnswers"], qa[ind]["incorrectAnswers"], qa[ind]["inputType"]);
        if (ind == Object.keys(qa).length) {
            getQuestion(qa[ind]["question"], qa[ind]["correctAnswers"], qa[ind]["incorrectAnswers"], qa[ind]["inputType"]);
            nextButton.value = "Показати результати";
            nextButton.addEventListener("click", showResults);
        }
        ind++;
    }
}

function validateAnswer(i) {
    let flag = false;
    for (let el of document.getElementsByName("variant")) {
        if (el.checked) {
            flag = true;
            qa[i]["chosenAnswers"].push(el.value);
        }
    }
    return flag;
}

function getQuestion(question, correct, incorrect, inputType) {
    clearVariants();
    let allVariants = correct.concat(incorrect);
    formTitle.innerText = question;
    for (let i = 0; i < allVariants.length; i++) {
        const div = document.createElement("div");
        div.classList.add("form__variant__block");
        const btn = document.createElement("input");
        btn.type = inputType;
        btn.name = "variant";
        btn.value = allVariants[i];
        btn.id = `var${i}`;
        const label = document.createElement("label");
        label.innerText = allVariants[i];
        label.htmlFor = btn.id;
        div.appendChild(btn);
        div.appendChild(label);
        variantsBlock.appendChild(div)
    }
}

function showResults(e) {
    e.preventDefault();
    const resultsWrapper = document.querySelector(".results-wrapper");
    const questionsTitles = document.getElementsByClassName("variants__title");
    const chosenAnswers = document.getElementsByClassName("variants__answer chosen");
    const corrAnswers = document.getElementsByClassName("variants__answer correct");
    let totalPoints = 0;
    let correctAnswersAmount = 0;
    document.querySelector(".title-box h2").innerText = "Результати тестування";
    formWrapper.classList.add("hidden");
    resultsWrapper.classList.remove("hidden");
    for (let i = 0; i < questionsTitles.length; i++) {
        questionsTitles[i].innerText = `Питання: ${qa[i + 1]["question"]}`;
        chosenAnswers[i].innerText = `Обрані відповіді: ${qa[i + 1]["chosenAnswers"]}`;
        corrAnswers[i].innerText = `Правильні відповіді: ${qa[i + 1]["correctAnswers"]}`;
        correctAnswersAmount += Object.keys(qa[i + 1]["correctAnswers"]).length;
        totalPoints += pointsPerQuestion(qa[i + 1]["chosenAnswers"], qa[i + 1]["correctAnswers"]);
    }
    const correct_perc = (totalPoints / correctAnswersAmount) * 100;
    const incorrect_perc = 100 - correct_perc;
    return initDiagrams(correct_perc, incorrect_perc);
}

function initDiagrams(val1, val2) {
    const percentages = document.getElementsByClassName("percentage");
    const percentageScales = document.getElementsByClassName("scale");
    const verdict = document.querySelector(".verdict");
    percentages[0].innerText = `${val1.toFixed(2)}%`;
    percentages[1].innerText = `${val2.toFixed(2)}%`;
    percentageScales[0].style.width = `${val1}%`;
    percentageScales[1].style.width = `${val2}%`;
    if (val1 > val2) {
        verdict.innerText = "Ви пройшли тестування, а отже, гарно знаєтеся на заходах протидії COVID-19. Бувайте здорові!"
        return true;
    } else {
        verdict.innerText = "Тестування не пройдено. Рекомендуємо ознайомитися із заходами протидії COVID-19. Бувайте здорові!";
        verdict.style.color = "rgba(85, 26, 17, 1)";
        return false;
    }
}

function clearVariants() {
    while (formVariants.lastChild) {
        formVariants.removeChild(formVariants.lastChild);
    }
}

Array.compare = (obj1, obj2) => {
    for (var i = 0; i < obj1.length; i++) {
        if (obj1[i] != obj2[i]) return false;
    }
    return true;
}

function pointsPerQuestion(arrUser, arrCorrect) {
    let points = 0
    for (let el of arrCorrect) {
        if (arrUser.includes(el)) points++;
    }
    return points;
}

