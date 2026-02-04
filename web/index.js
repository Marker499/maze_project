const widthInput = document.querySelector('#width');
const heightInput = document.querySelector('#height');
const seedInput = document.querySelector('#seed');

const button = document.querySelector('.generate-button');

const mazeElement = document.querySelector('#maze');

const getMaze = async (width, height, seed) => {
    return await eel.generate(width, height, seed) ();
}

const renderMaze = (maze) => {
    mazeElement.innerHTML = '';
    maze.forEach(row => {
        const rowElement = document.createElement('div');
        rowElement.classList.add('row');
        row.forEach(cell => {
            const cellElement = document.createElement('div');
            cellElement.classList.add('cell');
            if(cell === 1){
                cellElement.classList.add('wall');
            }
            rowElement.appendChild(cellElement);
        })
        mazeElement.appendChild(rowElement);
    })
}

button.addEventListener('click', () => {
    const width = Number(widthInput.value);
    const height = Number(heightInput.value);
    const seed = Number(seedInput.value);

    getMaze(width, height, seed).then(maze => {
        renderMaze(maze);
    })
})