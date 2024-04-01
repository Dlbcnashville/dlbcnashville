const menuBar1 = document.querySelector('.ham-1');
const menuBar2 = document.querySelector('.ham-2');
const menuBar3 = document.querySelector('.ham-3');

function displaySideMenu() {
    document.querySelector('.ham-side-nav-bar').classList.toggle('translate-left-right');
    menuBar2.classList.toggle('disappear');
    menuBar1.classList.toggle('rotate45');
    menuBar3.classList.toggle('rotateneg45');
}