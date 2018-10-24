function adjustBars(bar) {
    text = bar.innerText;
    grade = text.split(': ')[1];
    const progressBar = bar.querySelector('.progress > span');
    const colorBar = progressBar.querySelector('span');
    progressBar.style.width = grade;
    gradeNum = parseFloat(grade.replace('%', ''));
    let color;
    if (isNaN(gradeNum)) {
        color = '#000000';
    } else if (gradeNum >= 90) {
        color = '#2fee00';
    } else if (gradeNum >= 80) {
        color = '#f4db1d'
    } else if (gradeNum >= 70) {
        color = '#f4971d'
    } else {
        color = '#ff0000'
    }

    colorBar.style.backgroundColor = color;

}

function addArrow(box) {
    if (box.querySelector('.assignments')) {
        var arrow = document.createElement('img');
        arrow.src = 'static/assets/down.svg';
        arrow.classList.add('arrow');
        arrow.onclick = function() { arrowTrigger(box); } ;
        box.appendChild(arrow);
    }
}

function arrowTrigger(box) {
    var arrow = box.querySelector('.arrow');
    if (arrow) {
        if (arrow.src.endsWith('down.svg')) {
            box.querySelector('.assignments').style.display = 'inherit';
            arrow.src = 'static/assets/up.svg';
        } else {
            box.querySelector('.assignments').style.display = 'none';
            arrow.src = 'static/assets/down.svg';
        }
    }
}

function hideMissingBlurb(box) {
    text = box.innerText;
    grade = text.split(': ')[1];
    missingBox = box.querySelector('.gradeSansMissing');
    gradeSansMissing = missingBox.innerText.split('you have a ')[1];
    if (gradeSansMissing === grade) {
        missingBox.style.display = 'none';
    }
}

function arrowVisible() {
    return Boolean(document.querySelector('.assignments'))
}

for (const i of document.getElementsByClassName('surround')){
    adjustBars(i);
    addArrow(i);
    hideMissingBlurb(i);
}

if (arrowVisible()) {
    var footer = document.querySelector('footer');
    footer.style.display = 'inherit';
}