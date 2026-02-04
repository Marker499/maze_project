const widthInput = document.querySelector('#width');
const heightInput = document.querySelector('#height');
const seedInput = document.querySelector('#seed');

const button = document.querySelector('.generate-button');

const getMaze = async (width, height, seed) => {
    return await eel.generate(width, height, seed) ();
}

button.addEventListener('click', () => {
    const width = Number(widthInput.value);
    const height = Number(heightInput.value);
    const seed = Number(seedInput.value);
    console.log(width, height, seed);
    getMaze(width, height, seed).then(maze => console.log(maze))

})