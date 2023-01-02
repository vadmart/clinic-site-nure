// get .menu element and also another instance of it
const menu = document.querySelector(".menu");
const mobileMenu = document.querySelector(".mobile-menu");
const menuBtn = document.querySelector(".mobile-menu button");
const mobMenuContent = document.querySelector(".mobile-menu-content");
mobMenu();

// when resizing the window
window.addEventListener("resize", function (event) {
    //make "display: none" for menu elements id window's width less than 768px
    mobMenu();
})

function mobMenu() {
    if (window.outerWidth <= 1024) {
        menu.style.display = "none";
        mobileMenu.style.display = "flex";
        menuBtn.addEventListener("click", function (event) {
            if (mobMenuContent.style.display === "none") {
                mobMenuContent.style.display = "block";
            } else {
                mobMenuContent.style.display = "none";
            }
        })
    } else {
        menu.style.display = "flex";
        mobileMenu.style.display = "none";
    }
}
