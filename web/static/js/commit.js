function getRandomGradient() {
    const r1 = Math.floor(Math.random() * 256);
    const g1 = Math.floor(Math.random() * 256);
    const b1 = Math.floor(Math.random() * 256);
    const r2 = Math.floor(Math.random() * 256);
    const g2 = Math.floor(Math.random() * 256);
    const b2 = Math.floor(Math.random() * 256);
    return `radial-gradient(circle, rgba(${r1},${g1},${b1},1) 0%, rgba(${r2},${g2},${b2},1) 100%)`;
}

document.addEventListener('DOMContentLoaded', function() {
    const messageBoxes = document.querySelectorAll('.message-box');
    messageBoxes.forEach(function(box) {
        box.style.background = getRandomGradient();
    });
});
