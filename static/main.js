// Show Images on Image Button
const profileUploaderBtn = document.querySelector(".profile_uploader-btn");
const profiteInputButton = document.querySelector(".profile_input-button");
const profileImage = document.querySelector(".profile_image");

profileUploaderBtn.addEventListener("click", () => {
    profiteInputButton.click();
});

profiteInputButton.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            const result = reader.result;
            profileImage.src = result;
        };
        reader.readAsDataURL(file);
    }
});

// validation
let user_name = document.getElementById("name");
let surname = document.getElementById("surname");
let age = document.getElementById("age");
let city = document.getElementById("city");
let email = document.getElementById("email");
let checkbox = document.getElementById("validationFormCheck1");

let pattern = /^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$/;
let mailformat =/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;

function form_validate() {
    var flag = validate();
    if (flag) {
        generateImage();
    }
}

//Live form validation
user_name.addEventListener("keyup", function (e) {
    if (user_name.value.match(pattern) || user_name.value.length != 0) {
        user_name.style.border = "3px solid #14A44D";
    } else {
        user_name.style.border = "3px solid #DC4C64";
    }
});

surname.addEventListener("keyup", function (e) {
    if (surname.value.match(pattern) || surname.value.length != 0) {
        surname.style.border = "3px solid #14A44D";
    } else {
        surname.style.border = "3px solid #DC4C64";
    }
});

age.addEventListener("keyup", function (e) {
    if ((age.value > 0 && age.value < 70) || age.value.length != 0) {
        age.style.border = "3px solid #14A44D";
    } else {
        age.style.border = "3px solid #DC4C64";
    }
});

city.addEventListener("keyup", function (e) {
    if (city.value.match(pattern) || age.value.length != 0) {
        city.style.border = "3px solid #14A44D";
    } else {
        city.style.border = "3px solid #DC4C64";
    }
});

email.addEventListener("keyup", function (e) {
    if (mailformat.test(email.value) || email.value.length != 0) {
        email.style.border = "3px solid #14A44D";
    } else {
        email.style.border = "3px solid #DC4C64";
    }
});
checkbox.addEventListener("change", (event) => {
    if (event.currentTarget.checked) {
        document.getElementById("checkbox_label").style.color = "#14A44D";
    } else {
        document.getElementById("checkbox_label").style.color = "#DC4C64";
    }
});

// Form validation
function validate() {
    var status = true;
    var inputImage = document.getElementById("image");
    var files = inputImage.files;

    if (files.length === 0) {
        alert("Please choose a file first...");
        status= false;
    }

    if (!pattern.test(user_name.value)) {
        user_name.style.border = "3px solid #DC4C64";
        status = false;
    } 
    if (!pattern.test(surname.value)) {
        surname.style.border = "3px solid #DC4C64";
        status = false;
    } 
    if (age.value <= 0 || age.value >= 70) {
        age.style.border = "3px solid #DC4C64";
        status = false;
    } 
    if (!pattern.test(city.value)) {
        city.style.border = "3px solid #DC4C64";
        status = false;
    }
    if (!mailformat.test(email.value) ) {
        email.style.border = "3px solid #DC4C64";
        status = false;
    } 
    if (!document.getElementById("validationFormCheck1").checked) {
        document.getElementById("checkbox_label").style.color = "#DC4C64";
        status = false;
    }
    return status;
}

const loginPopup = document.querySelector(".popup");
const close = document.querySelector(".close");
var loading = document.getElementById("loading");
var generats = document.getElementById("generats");
// Close the popup
close.addEventListener("click", function () {
    loginPopup.classList.remove("show");
    location.reload();
});

function generateImage() {
    // Get the input image file
    var gender = document.querySelector('input[name="gender"]:checked');

    var inputImage = document.getElementById("image").files[0];
    const profileImage = document.querySelector(".profile_image");

    // Set the image button icon on upload image area.
    profileImage.src = "/static/public/Upload Button.png";

    // Show the Popup
    loginPopup.classList.add("show");

    // Create a FormData object to send the image to the server
    var formData = new FormData();
    formData.append("image", inputImage);
    
    formData.append("name", user_name.value);
    formData.append("surname", surname.value);
    formData.append("age", age.value);
    formData.append("city", city.value);
    formData.append("email", email.value);
    formData.append("gender", gender.value);
    console.log(gender.value)

    // Send the image to the server for generation
    fetch("/generate", {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            // Display the generated images 1
            var generatedImagesElement_1 =document.getElementById("generate_img_1");
            generatedImagesElement_1.innerHTML = "";
            console.log(data)
            // Display the generated images 2
            var generatedImagesElement_2 =document.getElementById("generate_img_2");
            generatedImagesElement_2.innerHTML = "";
            if (data.success) {
                if (data.data != null) {
                    var imageElement_1 = document.createElement("img");
                    var imageElement_2 = document.createElement("img");

                    window.img1 = "data:image/png;base64,"+data.data[0];
                    window.img2 = "data:image/png;base64,"+data.data[1];

                    window.img1_url = data.data[2];
                    // window.img2_url = data.data[3];

                    loading.style.display = "none";
                    generats.style.display = "block";
                    
                    imageElement_1.src = "data:image/png;base64,"+data.data[0];
                    
                    imageElement_1.style.width = "155px";
                    imageElement_1.style.height = "155px";
                    imageElement_1.classList.add("img-fluid");
                    generatedImagesElement_1.appendChild(imageElement_1);

                    imageElement_2.src = "data:image/png;base64,"+data.data[1];
                    imageElement_2.style.width = "155px";
                    imageElement_2.style.height = "155px";
                    imageElement_2.classList.add("img-fluid");
                    generatedImagesElement_2.appendChild(imageElement_2);
                }
            } else {
                // Display error message
                var errorMessage = document.createElement("p");
                errorMessage.textContent = data.error;
                console.log(errorMessage);
            }
        })
        .catch((error) => console.error("Error:", error));
    // Reset form data
    document.getElementById("generate_form").reset();
}

// Download images
function downloadImages() {
    // Create a new JSZip instance
    var zip = new JSZip();

    // Add the first image to the zip file
    zip.file("image1.png", base64toBlob(img1));

    // Add the second image to the zip file
    zip.file("image2.png", base64toBlob(img2));

    // Generate the zip file
    zip.generateAsync({ type: "blob" })
        .then(function (blob) {
            // Create a download link
            var link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "images.zip";

            // Append the link to the body and click it
            document.body.appendChild(link);
            link.click();

            // Remove the link from the DOM
            document.body.removeChild(link);
        })
        .catch(function (error) {
            console.error("Error generating zip file:", error);
        });
}

function base64toBlob(base64Data) {
    const byteString = atob(base64Data.split(',')[1]);
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);

    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: 'image/png' });
}

// Share images
const shareButton = document.getElementById('shareButton');
    // Add click event listener to the share button
    shareButton.addEventListener('click', async () => {
        try {
            // Check if the navigator supports the Share API
            if (navigator.share) {
                // Use the Share API to trigger the native sharing dialog
                await navigator.share({
                    title: 'Share Image',
                    text: 'Check out this generated image!',
                    url: img1_url
                });
            } else {
                // Fallback for browsers that do not support the Share API
                alert('Sorry, your browser does not support the Share API.');
            }
        } catch (error) {
            console.error('Error sharing image:', error);
        }
    });

// Share Popup 
// const section = document.querySelector(".share_popup"),
//     overlay = document.querySelector(".overlay"),
//     showBtn = document.querySelector(".show-modal");

// showBtn.addEventListener("click", () => section.classList.add("active"));

// overlay.addEventListener("click", () =>
//     section.classList.remove("active")
// );
