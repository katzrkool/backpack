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
    } else if (gradeNum > 90) {
        color = '#2fee00';
    } else if (gradeNum > 80) {
        color = '#f4db1d'
    } else if (gradeNum > 70) {
        color = '#f4971d'
    } else {
        color = '#ff0000'
    }

    colorBar.style.backgroundColor = color;

}

for (const i of document.getElementsByClassName('surround')){
    adjustBars(i);
}