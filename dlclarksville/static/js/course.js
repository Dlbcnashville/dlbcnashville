let textMenuist = document.querySelectorAll('.menu-card a');
let sidebarMenu = document.querySelector('.sidebar-menu');
let leftArrow = document.querySelector('.collapse-menu svg');

function toggleMenu() {
    textMenuist.forEach((ele) => {
        ele.classList.toggle('disappear');
    })
}

function toggleSidebar() {
    sidebarMenu.classList.toggle('disappear');
    leftArrow.classList.toggle('rotate180');
}

function openCity(evt, courseType) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(courseType).style.display = "block";
    evt.currentTarget.className += " active";
}

document.getElementById("defaultOpen").click();