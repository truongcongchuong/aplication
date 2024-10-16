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

            const form = document.querySelector("#Create-post");
            const buttonSubmit = document.querySelector("#post");
            const choose_file = document.querySelectorAll("#choose-file");
            const file_input = document.querySelector("#file-input");
            const buttonExit = document.querySelector("#exit-mobal");
            const block_choose_file = document.querySelector(".block-choose-file");
            const block_preview = document.querySelector(".preview");
            const number_file_allow_display = 5;

            buttonExit.addEventListener("click", ()=> {
                body.style.overflow = "auto";
                mobal.style.display = 'none';
            });

            // choose file
            choose_file.forEach(button => {
                button.onclick = () => {
                    file_input.click();
                };
            });
            let old_class_ = "preview-0-file";
            let selected_file = [];
            let count = 1;
            function previewFiles() {
                const files = Array.from(file_input.files);
                selected_file = selected_file.concat(files);
                console.log(selected_file.length);
                console.log("array",selected_file)
                const number_file_disallow_display = selected_file.length - number_file_allow_display;

                console.log("file1: ", old_class_)
                var new_class_ = `preview-${selected_file.length}-file`;
                if (new_class_ != old_class_) {
                    if (number_file_disallow_display > 0 ) {
                        new_class_ = "display-out-file";
                    }
    
                    var preview_old = document.querySelector(`.${old_class_}`);
                    preview_old.classList.replace(old_class_, new_class_);
                    old_class_ = new_class_;
                }
                var preview = document.querySelector(`.${old_class_}`);
                
                function readAndPreview(file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        var url = e.target.result;

                        if (file.type != null && count <=  number_file_allow_display + 1 ){
                            if (count <=  number_file_allow_display) {
                                if  (/\.(jpe?g|png|gif)$/i.test(file.name)) {
                                    const img = new Image();
                                    img.title = file.name;
                                    img.src = url;
                                    img.id = `file_${count}`;
                                    preview.appendChild(img);
                                    count++;
                                }
                                else if  (/\.(mp4|webm|ogg)$/i.test(file.name)) {
                                    const video = document.createElement("video");
                                    video.id = `file_${count}`;
                                    video.controls = true;
                                    
                                    const source = document.createElement("source");
                                    source.src = url;
                                    source.type = file.type;
                                    video.style.width = "100%";
                                    video.style.height = "100%";   
                                    video.style.maxHeight = "400px";
            
                                    video.appendChild(source);
                                    preview.appendChild(video);
                                    count++;
                                }
                            }
                            else {
                                var div = document.createElement("div");
                                div.id = "out-of-range";
                                div.innerText = "+ 1";
                                preview.appendChild(div);
                            }
                        }
                        else if (file.type != null && count >  number_file_allow_display + 1) {
                            if (count === file.length) {
                                let text = document.querySelector("#out-of-range");
                                text.innerHTML = `+ ${count}`;
                            } 
                            count++;
                        }
                        else {
                            console.log("file không hợp lệ vui lòng chọn file khác")
                        }
                    }.bind(this)

                    reader.readAsDataURL(file);
                }

                if (files) {
                    block_choose_file.style.display = "none";
                    block_preview.style.display = "block";
                    Array.prototype.forEach.call(files, readAndPreview);
                }
            }
            file_input.addEventListener("change", previewFiles);
            // submit form
            buttonSubmit.addEventListener("click", () => {
                var form_data = new FormData(form);
                form_data.delete("file[]");
                selected_file.forEach((file, index) => {
                    form_data.append("files[]", file);
                });
                fetch("/CreatePost", {
                    method: "POST",
                    body: form_data
                })
                .then(response => response.text())
                .then(data => {
                    console.log("hiển thị biến data : ",data);
                    location.reload();
                })
                .catch(error => {
                    console.error("Error: ", error)
                })
            });
        })
        .catch(error => console.error("Error:", error))
    });
});