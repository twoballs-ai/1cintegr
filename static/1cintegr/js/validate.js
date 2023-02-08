// document.addEventListener("DOMContentLoaded", function() {
const btn = document.getElementById("modalactivation");
// const btnform2open = document.getElementById("form-2openbutton");
// const btnform3open = document.getElementById("form-3openbutton");
// const btnform4open = document.getElementById("form-4openbutton");
// const btnform5open = document.getElementById("form-5openbutton");
const backbtnform4open = document.getElementById("form-4backopenbutton");
const backbtnform3open = document.getElementById("form-3backopenbutton");
const backbtnform2open = document.getElementById("form-2backopenbutton");
const backbtnform1open = document.getElementById("form-1backopenbutton");
//     const modal1 = document.getElementById("exampleModalToggle1");
// //     btnform2open.disabled = true;
// //

// const form = document.querySelector('#form-1')
// const validateBtn = form.querySelector('.form-2openbutton')
// const name = form.querySelector('#name')
// const description = form.querySelector('#description')
// const object_type = form.querySelector('#object_type')
// const PurposeObject = form.querySelector('#PurposeObject')
// const Condition = form.querySelector('#Condition')
// const technicalFloor = form.querySelector('#technicalFloor')
// const Lift = form.querySelector('#Lift')
// const remontDate = form.querySelector('#remontDate')
// const SecurityObligation = form.querySelector('#SecurityObligation')
// const region = form.querySelector('#region')
// const address = form.querySelector('#address')
// const object_area = form.querySelector('#object_area')
// const LandCategory = form.querySelector('#LandCategory')
// const TypeOfPermittedUse = form.querySelector('#TypeOfPermittedUse')
// const fields = form.querySelectorAll('.field')
//
//

//attaching "change" event to the file upload button




(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
    var forms2 = document.querySelectorAll('.needs-validation2')
    var forms3 = document.querySelectorAll('.needs-validation3')
    var forms4 = document.querySelectorAll('.needs-validation4')
    var forms4redact = document.querySelectorAll('.needs-validation4redact')
    var forms5 = document.querySelectorAll('.needs-validation5')


    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    console.log('не валидно')
                } else if (form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    console.log('валидно')
                    const myModalEl = document.getElementById('exampleModalToggle1');
                    const modal = bootstrap.Modal.getInstance(myModalEl)
                    modal.hide();

                    const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle2"));
                    myModal.show();


                }

                form.classList.add('was-validated')
            }, false)
        })

    Array.prototype.slice.call(forms2)
        .forEach(function (form2) {
            form2.addEventListener('submit', function (event) {
                if (!form2.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    console.log('не валидно')
                } else if (form2.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    console.log('валидно')
                    const myModalEl = document.getElementById('exampleModalToggle2');
                    const modal = bootstrap.Modal.getInstance(myModalEl)
                    modal.hide();

                    const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle3"));
                    myModal.show();


                }

                form2.classList.add('was-validated')
            }, false)
        })

    Array.prototype.slice.call(forms3)
        .forEach(function (form3) {
            form3.addEventListener('submit', function (event) {
                if (!form3.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    console.log('не валидно')
                } else if (form3.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    console.log('валидно')
                    const myModalEl = document.getElementById('exampleModalToggle3');
                    const modal = bootstrap.Modal.getInstance(myModalEl)
                    modal.hide();

                    const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle4"));
                    myModal.show();


                }

                form3.classList.add('was-validated')
            }, false)
        })
    Array.prototype.slice.call(forms4)
        .forEach(function (form4) {
            form4.addEventListener('submit', function (event) {
                if (!form4.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    console.log('не валидно')
                } else if (form4.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    console.log('валидно')
                    const myModalEl = document.getElementById('exampleModalToggle4');
                    const modal = bootstrap.Modal.getInstance(myModalEl)
                    modal.hide();

                    const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle5"));
                    myModal.show();


                }

                form4.classList.add('was-validated')
            }, false)
        })
    Array.prototype.slice.call(forms4redact)
        .forEach(function (form4r) {
            form4r.addEventListener('submit', function (event) {
                if (!form4r.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    console.log('не валидно')
                } else if (form4r.checkValidity()) {

                    console.log('валидно')



                }

                form4r.classList.add('was-validated')
            }, false)
        })
    Array.prototype.slice.call(forms5)
        .forEach(function (form5) {
            form5.addEventListener('submit', function (event) {
                if (!form5.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    console.log('не валидно')
                } else if (form5.checkValidity()) {

                    console.log('валидно')



                }

                form5.classList.add('was-validated')
            }, false)
        })

})()



btn.addEventListener("click", function () {
    const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle1"));
    myModal.show();
});

backbtnform1open.addEventListener("click", function () {
    const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle1"));
    console.log('назад на первую');
    myModal.show();
});

backbtnform2open.addEventListener("click", function () {
    const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle2"));
    myModal.show();
});

backbtnform3open.addEventListener("click", function () {
    const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle3"));
    myModal.show();
});

backbtnform4open.addEventListener("click", function () {
    const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle4"));
    myModal.show();
});

document.getElementById("formFile").addEventListener("change", validateFile)
function validateFile(){
    const allowedExtensions =  ['jpg','jpeg','png','gif'],
        sizeLimit = 10000000; // 1 megabyte

    // destructuring file name and size from file object
    const { name:fileName, size:fileSize } = this.files[0];

    /*
    * if the filename is apple.png, we split the string to get ["apple","png"]
    * then apply the pop() method to return the file extension (png)
    *
    */
    const fileExtension = fileName.split(".").pop();

    /*
      check if the extension of the uploaded file is included
      in our array of allowed file extensions
    */
    if(!allowedExtensions.includes(fileExtension)){
        alert("Пожалуйста загружайте только jpg, jpeg and png файлы");
        this.value = null;
    }else if(fileSize > sizeLimit){
        alert("Максимальный размер картинки 10 мб.")
        this.value = null;
    }
}

/* javascript function to validate file type */
document.getElementById("files[]").addEventListener("change", validateFilesType)

function validateFilesType() {
    let inputElement = document.getElementById('files[]');
    let files = inputElement.files;
    const allowedExtensions =  ['jpg','jpeg','png','gif']
    const sizeLimit = 10000000;
    if(files.length===0){
        alert("Сначала выберите файл");
        return false;
    }else{

        /* iterating over the files array */
        for(let i=0;i<files.length;i++){
            // let filename = files[i].name;
            const { name:fileName, size:fileSize } = this.files[i];
            /* getting file extenstion eg- .jpg,.png, etc */
            // let extension = filename.substring(filename.lastIndexOf("."));
            const fileExtension = fileName.split(".").pop();

            /* define allowed file types */
            // let allowedExtensionsRegx = /(\.jpg|\.jpeg|\.png|\.gif)$/i;

            /* testing extension with regular expression */
            // let isAllowed = allowedExtensionsRegx.test(extension);

    if(!allowedExtensions.includes(fileExtension)){
        alert("Пожалуйста загружайте только jpg, jpeg and png файлы");
        this.value = null;
    }else if(fileSize > sizeLimit){
        alert("Максимальный размер картинки 10 мб.")
        this.value = null;
    }
        }
    }
}
