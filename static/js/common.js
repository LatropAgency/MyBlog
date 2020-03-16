let menu_btn = document.getElementById('menu_btn');
let menu = document.getElementById('menu');
let notifications = document.getElementById('notifications');
menu_btn.onclick = function () {
    if (menu.classList.contains('show')) {
        menu.classList.remove('show');
        menu.classList.add('hide');
        menu.style.flex = 0
        menu.style.display = 'block'
    } else {
        menu.classList.remove('hide');
        menu.classList.add('show');
        menu.style.flex = 2
        menu.style.display = 'block'
    }
}

notifications.onclick = function () {
    notifications.style.display = 'none'
}