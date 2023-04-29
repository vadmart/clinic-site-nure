// get .menu element and also another instance of it
// const menu = document.querySelector(".menu");
// const mobileMenu = document.querySelector(".mobile-menu");
// const menuBtn = document.querySelector(".mobile-menu button");
// const mobMenuContent = document.querySelector(".mobile-menu-content");
// mobMenu();
//
// // when resizing the window
// window.addEventListener("resize", function () {
//     //make "display: none" for menu elements id window's width less than 768px
//     mobMenu();
// });
// menuBtn.addEventListener("click", function () {
//     if (mobMenuContent.style.display === "none") {
//         mobMenuContent.style.display = "block";
//     } else {
//         mobMenuContent.style.display = "none";
//     }
// })
//
// function mobMenu() {
//     if (window.outerWidth <= 1024) {
//         menu.style.display = "none";
//         mobileMenu.style.display = "flex";
//     } else {
//         menu.style.display = "flex";
//         mobMenuContent.style.display = "none";
//         mobileMenu.style.display = "none";
//     }
// }


const mobMenuButton = document.querySelector(".mobile-menu button");
const mobileMenuContent = document.querySelector(".mobile-menu-content");
mobMenuButton.addEventListener("click", ()=>{
    mobileMenuContent.classList.contains("hidden") ? mobileMenuContent.classList.remove("hidden") : mobileMenuContent.classList.add("hidden");
}
)



