let menu_btn = document.getElementById('menu_btn');
    let menu = document.getElementById('menu');
    menu_btn.onclick = function () {
        if (menu.classList.contains('show')) {
            menu.classList.remove('show');
            menu.classList.add('hide');
            menu.style.flex = 0
        } else {
            menu.classList.remove('hide');
            menu.classList.add('show');
            menu.style.flex = 2
        }
    }