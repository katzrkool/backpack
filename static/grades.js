function adjustBars(bar) {
    const text = bar.innerText;
    const grade = text.split(': ')[1];
    const progressBar = bar.querySelector('.progress > span');
    const colorBar = progressBar.querySelector('span');
    progressBar.style.width = grade;
    const gradeNum = parseFloat(grade.replace('%', ''));
    let color;
    if (isNaN(gradeNum)) {
        color = '#000000';
    } else if (gradeNum >= 89.5) {
        color = '#2fee00';
    } else if (gradeNum >= 79.5) {
        color = '#cbff53'
    } else if (gradeNum >= 69.5) {
        color = '#f4971d'
    } else {
        color = '#ff0000'
    }

    colorBar.style.backgroundColor = color;

}

function addArrow(box) {
    console.log(box.querySelector('.assignments'))
    if (box.querySelector('.assignments')) {
        const arrow = document.createElement('img');
        arrow.src = 'static/assets/down.svg';
        arrow.classList.add('arrow');
        arrow.onclick = function() { arrowTrigger(box); } ;
        box.appendChild(arrow);
    }
}

function arrowTrigger(box) {
    const arrow = box.querySelector('.arrow');
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
    const text = box.innerText;
    const grade = text.split(': ')[1];
    const missingBox = box.querySelector('.gradeWithMissing');
    if (missingBox) {
        const gradeWithMissing = missingBox.innerText.split('you have a ')[1];
        if (gradeWithMissing === grade) {
            missingBox.style.display = 'none';
        }
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
    const footer = document.querySelector('footer');
    footer.style.display = 'inherit';
}