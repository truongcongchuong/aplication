const dropArea = document.querySelector(".drop_box"),
    button = dropArea.querySelector("button"),
    dragText = dropArea.querySelector("header"),
    input = dropArea.querySelector("input"),
    avatar = document.querySelector("#avatar"); // Phần tử img để hiển thị avatar

button.onclick = () => {
    input.click(); // Mở hộp thoại chọn file
}

const reader = new FileReader(); // Tạo một đối tượng FileReader để đọc file

input.addEventListener("change", (event) => {
    const files = event.target.files; // Lấy danh sách file từ input
    console.log(files[0]); // In thông tin file đầu tiên ra console
    
    reader.readAsDataURL(files[0]); // Đọc file dưới dạng Base64

    reader.addEventListener("load", (event) => {
        const url = event.target.result; // Lấy chuỗi Base64 từ FileReader
        avatar.src = url; // Gán đường dẫn ảnh cho thuộc tính src của thẻ img
    });
});
