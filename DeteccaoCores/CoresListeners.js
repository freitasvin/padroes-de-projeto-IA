const currentColor = document.querySelector('.current-color');

const redValue = document.querySelector('#red-value');
document.querySelector('#red').addEventListener('input', (event) => {
    const value = event.target.value;;
    redValue.innerText = value;
    currentColor.style.setProperty('--red', value);
})

const greenValue = document.querySelector('#green-value');
document.querySelector('#green').addEventListener('input', (event) => {
    const value = event.target.value;;
    greenValue.innerText = value;
    currentColor.style.setProperty('--green', value);
})

const blueValue = document.querySelector('#blue-value');
document.querySelector('#blue').addEventListener('input', (event) => {
    const value = event.target.value;;
    blueValue.innerText = value;
    currentColor.style.setProperty('--blue', value);
})

button.addEventListener('click', prever);
