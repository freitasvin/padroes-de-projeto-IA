
const button = document.querySelector('button');
const output = document.querySelector('output');

const entradas = [];
const respostas = [];

cores.forEach((cor, indice) => {
    const codigoCor = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    codigoCor[indice] = 1;
    cor.valores.forEach(corRGB => {
        entradas.push(corRGB);
        respostas.push(codigoCor);
    });
})

const dadosTreino = tf.tensor2d(entradas, [entradas.length, 3]);
const dadosResposta = tf.tensor2d(respostas, [respostas.length, 9]);
const modelo = tf.sequential();

modelo.add(tf.layers.dense({
    inputShape: 3,
    units: 10,
    activation: 'sigmoid'
}));

modelo.add(
    tf.layers.dense({
        inputShape: 10,
        units: 9,
        activation: "softmax"
    })
);

modelo.compile({
    loss: "categoricalCrossentropy",
    optimizer: tf.train.adam()
});

async function treinarDados(){
    for(let i = 0; i < 15; i++){
          await modelo.fit(dadosTreino, dadosResposta, {epochs: 20});
    }
}