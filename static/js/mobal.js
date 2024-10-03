document.addEventListener("DOMContentLoaded", () => {
    const mobal = document.querySelector(".mobal");
    const displayMobal = document.querySelector("#displayMobal");
    const body = document.querySelector("body");

    displayMobal.addEventListener("click", (event)=> {
        event.preventDefault();
        fetch("/CreatePost")
        .then(response => response.text())
        .then(data => {
            mobal.innerHTML = data;
            body.style.overflow = "hidden";
            mobal.style.display = 'block';
            const buttonExit = document.querySelector("#exit-mobal");
            buttonExit.addEventListener("click", ()=> {
                body.style.overflow = "auto";
                mobal.style.display = 'none';
            })
        })
        .catch(error => console.error("Error:", error))
    });
});