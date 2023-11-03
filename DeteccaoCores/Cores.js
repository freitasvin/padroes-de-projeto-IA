async function iniciar() {
    await treinarDados();
    document.querySelector('.training').classList.add('done');
}

async function prever() {
    const colorRGB = [
        parseInt(redValue.innerText, 10),
        parseInt(greenValue.innerText, 10),
        parseInt(blueValue.innerText, 10),
    ];
    console.log(colorRGB)
    const newData = tf.tensor2d(
        [colorRGB],
        [1, 3]
    )
    const predicao = modelo.predict(newData);

    mostrarResultado(predicao);
}

async function mostrarResultado(prediction) {
    const dados = await prediction.data();
    let maxProbability = Math.max(...dados);
    let predictionIndex = dados.indexOf(maxProbability);
    output.innerText = cores[predictionIndex].nome;
    output.classList.add('refresh');
    setTimeout(() => {
        output.classList.remove('refresh');
    }, 150);
}

iniciar();