function adjustBars(bar) {
    text = bar.innerText;
    grade = text.split(': ')[1];
    const progressBar = bar.querySelector('.progress > div');
    console.log(grade);
    progressBar.style.width = grade;
    gradeNum = parseFloat(grade.replace('%', ''))
    let color;
    if (gradeNum > 90) {
        color = '#2fee00';
    } else if (gradeNum > 80) {
        color = '#f4db1d'
    } else if (gradeNum > 70) {
        color = '#f4971d'
    } else {
        color = '#ff0000'
    }

    progressBar.style.backgroundColor = color;

}

for (const i of document.getElementsByClassName('surround')){
    adjustBars(i);
}