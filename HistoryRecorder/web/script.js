function setRecorderEnabled(isEnabled){
    let indicator = document.querySelector("#history-recorder-status > #indicator");
    let label = document.querySelector("#history-recorder-status > span.text");
    let input = document.querySelector("#history-recorder-status #history-recorder-checkbox");

    if (isEnabled){
        if (indicator){
            indicator.innerText = "ON";
            indicator.classList.remove('off');
            indicator.classList.add('on');
        }
        if (label) {
            label.classList.remove('off');
            label.classList.add('on');
            label.innerText = "Your answers are being recorded";
        }
        if (input) {
            input.checked = true;
        }
    } else {
        if (indicator) {
            indicator.innerText = "OFF";
            indicator.classList.remove('on');
            indicator.classList.add('off');
        }
        if (label) {
            label.classList.remove('on');
            label.classList.add('off');
            label.innerText = "Answer recording is stopped";
        }
        if (input) {
            input.checked = false;
        }
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    let checkbox = document.getElementById("history-recorder-checkbox");
    if (checkbox){
        checkbox.addEventListener("change", function (event) {
            setRecorderEnabled(event.target.checked);
            pycmd("recorder_status_changed")
        })
    }
});