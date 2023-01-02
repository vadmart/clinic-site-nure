const isStorageAllowed = window.confirm("Чи дозволяєте Ви запис даних у локальне сховище?");
const questions = [["Скільки разів можна використовувати маску для захисту дихальних шляхів?", ["radio", "1 раз", "Скільки завгодно", "Взагалі не має сенсу надягати"]],
    ["Яку відстань необхідно тримати у відношенні до інших людей? Оберіть декілька варіантів",
        ["checkbox", "3м", "5м", "1м", "0.5м"]],
    ["Скільки днів необхідно залишатися вдома після одужання від COVID-19?", ["radio", "14 днів", "2 дні", "Жодної різниці", "5 днів"]],
    ["Із якого віку можна з'являтися у місцях масового скупчення людей під час посилення пандемії COVID-19", ["radio", "Вік значення не має - взагалі не можна", "З 18 років", "З 21 року"]]];
const correctAnswers = [["1 раз"], ["3м", "5м"], ["14 днів"], ["Вік значення не має - взагалі не можна"]];
var userAnswers = [];
const formWrapper = document.querySelector(".form-wrapper");
const form = document.querySelector(".form-wrapper__form");
const fieldset = window["form__content"];
const formTitle = window["form__title"];
const formVariants = window["form__variants"];
const nextButton = document.querySelector(".form__button");
const variantsBlock = document.getElementById("form__variants");
var ind = 1;


getQuestion(questions[0][0], questions[0][1]);

nextButton.addEventListener("click", (e) => {
    e.preventDefault();
    if (!validateAnswer()) {
        form.style.borderColor = "red";
        fieldset.style.borderColor = "red";
        alert("Оберіть варіант відповіді!");
        return;
    }
    form.style.borderColor = "#000";
    fieldset.style.borderColor = "";
    if (ind <= questions.length - 1) {
        getQuestion(questions[ind][0], questions[ind][1]);
        if (ind == questions.length - 1) {
            nextButton.value = "Показати результати";
        }
        ind++;
    } else {
        const testFailed = showResults();
        if (isStorageAllowed && !testFailed) {
            addDataToWebStorage(testFailed);
        } else {
            localStorage.clear();
        }
    }
});

function validateAnswer() {
    var answerFlag = false;
    var answer = [];
    for (var el of document.getElementsByName("variant")) {
        if (el.checked) {
            answerFlag = true;
            answer.push(el.value);
        }
    }
    if (answerFlag) {
        userAnswers.push(answer);
    }
    return answerFlag;
}

function getQuestion(question, variants) {
    clearVariants();
    formTitle.innerText = question;
    for (var i = 1; i < variants.length; i++) {
        const btn = document.createElement("input");
        btn.type = variants[0];
        btn.name = "variant";
        btn.value = variants[i];
        btn.id = `var${i}`;
        const label = document.createElement("label");
        label.innerText = variants[i];
        label.htmlFor = btn.id;
        variantsBlock.appendChild(btn);
        variantsBlock.appendChild(label);
    }
}

function showResults() {
    const resultsWrapper = document.querySelector(".results-wrapper");
    const questionsTitles = document.getElementsByClassName("variants__title");
    const chosenAnswers = document.getElementsByClassName("variants__answer chosen");
    const corrAnswers = document.getElementsByClassName("variants__answer correct");
    var corr_answ_amount = 0;
    document.querySelector(".title-box h2").innerText = "Результати тестування";
    formWrapper.classList.add("hidden");
    resultsWrapper.classList.remove("hidden");
    for (var i = 0; i < questionsTitles.length; i++) {
        questionsTitles[i].innerText = `Питання: ${questions[i][0]}`;
        chosenAnswers[i].innerText = `Обрана відповідь: ${userAnswers[i]}`;
        corrAnswers[i].innerText = `Правильна відповідь: ${correctAnswers[i]}`;
        if (Array.compare(userAnswers[i], correctAnswers[i])) {
            corr_answ_amount++;
        }
    }
    const correct_perc = (corr_answ_amount / questionsTitles.length) * 100;
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

function addDataToWebStorage(isTestFailed) {
    for (var i = 0; i < userAnswers.length; i++) {
        localStorage[`question${i}`] = questions[i][0];
        localStorage[`answer${i}`] = userAnswers[i];
    }
    localStorage["isTestFailed"] = isTestFailed;
}