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
/* 
 
            file_input.addEventListener("change", (event) => {
                const files = event.target.files;
                const number_file_upload = files.length;
                var display_file = "";
                    const reader = new FileReader();
                    idx++;
                    console.log("test");
                    reader.addEventListener("load", (event) => {
                        const  url = event.target.result;

                        let file = files[idx];
                        reader.readAsDataURL(file);
                        console.log("test 0");

                        if (file.type.startsWith("image/")){
                            display_file += `<img src="${ url }" id="file">`
                            console.log("test1");
                        }
                        else if (file.type.startsWith("video/")) {
                            display_file += `<video width="100%" height="100%" controls id="file">`
                            display_file += `<source src="${ url }" type="video/mp4">`
                            display_file += `</video>`
                            console.log("test2");
                        }
                        else {
                            console.log("không hỗ trợ các file khác ngoài file video và file image");
                        }
                    });
                }
                    
                /* 
                thiết lập id cho khối mới tạo hiển thị file ảnh và video được đăng tải
                -> tên id khi file chọn từ 1 -> 5 thì sẽ có id là display-file-(số file)
                -> tên id khi file chọn từ 6 đổ lên thì sẽ có id là display-file-bigger
                */
               /*s
                let block_display_file_class = `display-file-${number_file_upload}`;
                let number_file_disallow_display = number_file_upload - number_file_allow_display;
                if (number_file_upload >= number_file_allow_display) {
                    block_display_file_class = "display-file-bigger";
                    display_file += `<div id="not_display">+ ${number_file_disallow_display}</div>`
                }

                let html = `
                <div class="function-edit">
                    <button type="button"><i class="bi bi-pencil-fill"></i> edit</button>
                    <button type="button"><i class="bi bi-bookmark-plus-fill"></i> add video/image </button>
                <div>
                <div class="${block_display_file_class}">
                    ${display_file}
                </div>
                ` ;
                console.log(html);
                console.log(display_file);
                block_edit_file.innerHTML = html;
            });*/