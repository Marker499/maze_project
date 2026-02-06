const generateSection = document.querySelector(".generate");
const exportSection = document.querySelector(".export");

const widthInput = document.querySelector('#width');
const heightInput = document.querySelector('#height');
const seedInput = document.querySelector('#seed');

const cellSizeInput = document.querySelector('#cell_size');
const wallHeightInput = document.querySelector('#wall_height');
const wallThicknessInput = document.querySelector('#wall_thickness');
const floorThicknessInput = document.querySelector('#floor_thickness');

const isAsciiBinaryRadio = document.querySelector("#binary");
const isAsciiAsciiRadio = document.querySelector("#ascii");

const generateButton = document.querySelector('#generate-button');
const regenerateButton = document.querySelector('#regenerate-button');
const exportButton = document.querySelector("#export-button");

const mazeElement = document.querySelector('#maze');

const getMaze = async (width, height, seed) => {
    return await eel.generate(width, height, seed) ();
}

const exportToStl = async (
        file_name, 
        cell_size,
        wall_height,
        wall_thickness,
        floor_thickness,
        is_ascii
    ) => {
    return await eel.export_to_stl(
        file_name, 
        cell_size,
        wall_height,
        wall_thickness,
        floor_thickness,
        is_ascii
    ) ();
}

const renderMaze = (maze) => {
    mazeElement.innerHTML = '';
    maze.forEach((row, y) => {
        const rowElement = document.createElement('div');
        rowElement.classList.add('row');
        row.forEach((cell, x) => {
            const cellElement = document.createElement('div');
            cellElement.classList.add('cell');
            const isEntranceOrExit = (x === 0 && y === 1) || (x === row.length - 1 && y === maze.length - 2);
            if(cell === 1 && !isEntranceOrExit){
                cellElement.classList.add('wall');
            }
            rowElement.appendChild(cellElement);
        })
        mazeElement.appendChild(rowElement);
    })
}

generateButton.addEventListener('click', () => {
    const width = Number(widthInput.value);
    const height = Number(heightInput.value);
    const seed = Number(seedInput.value);

    getMaze(width, height, seed).then(maze => {
        renderMaze(maze);
        generateSection.classList.toggle("hidden");
        exportSection.classList.toggle("hidden");
    })
})

regenerateButton.addEventListener('click', () => {
    generateSection.classList.toggle("hidden");
    exportSection.classList.toggle("hidden");
})

exportButton.addEventListener('click', () => {
    const cellSize = Number(cellSizeInput.value);
    const wallHeight = Number(wallHeightInput.value);
    const wallThickness = Number(wallThicknessInput.value);
    const floorThickness = Number(floorThicknessInput.value);

    const isAscii = isAsciiAsciiRadio.checked;
    
    exportToStl(
        "", 
        cellSize, 
        wallHeight, 
        wallThickness, 
        floorThickness, 
        isAscii
    ).then(res => (res) ? alert("Лабиринт успешно сгенерирован") : alert("Ошибка при генерации лабиринта"));
})