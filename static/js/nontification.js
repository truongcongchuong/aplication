document.addEventListener("DOMContentLoaded", ()=>{
    const Block = document.querySelector(".nontification");
    const button = Block.querySelector("button");

    button.addEventListener("click", () => {
        Block.style.display = "none";
    })
})
