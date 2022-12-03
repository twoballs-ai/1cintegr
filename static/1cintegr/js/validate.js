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
(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
    var forms2 = document.querySelectorAll('.needs-validation2')
    var forms3 = document.querySelectorAll('.needs-validation3')
    var forms4 = document.querySelectorAll('.needs-validation4')


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

})()



btn.addEventListener("click", function () {
    const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle1"));
    myModal.show();
});
// (() => {
//   'use strict'
//
//   // Fetch all the forms we want to apply custom Bootstrap validation styles to
//   const forms = document.querySelectorAll('.needs-validation')
//
//   // Loop over them and prevent submission
//   Array.from(forms).forEach(form => {
//     form.addEventListener('submit', event => {
//       if (!form.checkValidity()) {
//         event.preventDefault()
//         event.stopPropagation()
//       }
//
//       form.classList.add('was-validated')
//     }, false)
//   })
// })()
//
// let generateError = function (text) {
//   let error = document.createElement('div')
//   error.className = 'error'
//   error.style.color = 'red'
//   error.innerHTML = text
//   return error
// }
//
// let removeValidation = function () {
//   let errors = form.querySelectorAll('.error')
//
//   for (let i = 0; i < errors.length; i++) {
//     errors[i].remove()
//   }
// }
// //
// // let counterForm1 = function () {
// //     let counter = 100
// //     counter++
// //     console.log(counter)
// //
// //
// // }
//
// let checkFieldsPresence = function () {
//
//   for (let i = 0; i < fields.length; i++) {
//     if (!fields[i].value) {
//       console.log('field is blank', fields[i])
//       let error = generateError('Cant be blank')
//       form[i].parentElement.insertBefore(error, fields[i])
//
//     }
//   }
// }
//
// form.addEventListener('submit', function (event) {
//     event.preventDefault()
//
//     removeValidation()
//
//     checkFieldsPresence()
//
//
//
// })


// form.addEventListener('submit', function (event) {
//     event.preventDefault()
//     console.log('clicked on validate')
//     console.log('name: ', name.value)
//     console.log('description: ', description.value)
//     console.log('object_type: ', object_type.value)
//     console.log('PurposeObject: ', PurposeObject.value)
//     console.log('Condition: ', Condition.value)
//     console.log('technicalFloor: ', technicalFloor.value)
//     console.log('Lift: ', Lift.value)
//     console.log('remontDate: ', remontDate.value)
//     console.log('SecurityObligation: ', SecurityObligation.value)
//     console.log('region: ', region.value)
//     console.log('address: ', address.value)
//     console.log('object_area: ', object_area.value)
//     console.log('LandCategory: ', LandCategory.value)
//     console.log('TypeOfPermittedUse: ', TypeOfPermittedUse.value)
// })


// btnform2open.addEventListener("click", function() {
//     const myModalEl = document.getElementById('exampleModalToggle1');
//     const modal = bootstrap.Modal.getInstance(myModalEl)
//     modal.hide();
//
//     const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle2"));
//     myModal.show();
//
// });

// btnform3open.addEventListener("click", function() {
//     const myModalEl = document.getElementById('exampleModalToggle2');
//     const modal = bootstrap.Modal.getInstance(myModalEl)
//     modal.hide();
//
//     const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle3"));
//     myModal.show();
//
// });
//
//     btnform4open.addEventListener("click", function() {
//     const myModalEl = document.getElementById('exampleModalToggle3');
//     const modal = bootstrap.Modal.getInstance(myModalEl)
//     modal.hide();
//
//     const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle4"));
//     myModal.show();
//
// });
//
//     btnform5open.addEventListener("click", function() {
//     const myModalEl = document.getElementById('exampleModalToggle4');
//     const modal = bootstrap.Modal.getInstance(myModalEl)
//     modal.hide();
//
//     const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle5"));
//     myModal.show();
//
// });
// var modalToggle = document.getElementById('toggleMyModal') // relatedTarget
// myModal.show(modalToggle)


//
// const form  = document.getElementById('form-1');
//
// const name = document.getElementById('name');
// const nameError = document.querySelector('#name + span.error');
//
// name.addEventListener('input', function (event) {
//   // Каждый раз, когда пользователь что-то вводит,
//   // мы проверяем, являются ли поля формы валидными
//
//   if (name.validity.valid) {
//     // Если на момент валидации какое-то сообщение об ошибке уже отображается,
//     // если поле валидно, удаляем сообщение
//     nameError.textContent = ''; // Сбросить содержимое сообщения
//     nameError.className = 'error'; // Сбросить визуальное состояние сообщения
//   } else {
//     // Если поле не валидно, показываем правильную ошибку
//     showError();
//   }
// });
//
// btnform2open.addEventListener("click", function(event) {
//   // Если поле email валдно, позволяем форме отправляться
//     if (name.validity.valid ===true ) {
//                 console.log('svdsvd1')
//     const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle2"));
//     myModal.show();
//     modal1.hide();
//     myModal.hide();
//     console.log('leftform2');
//
//
//
//     } else if(name.validity.valid ===false ){
//       console.log('svdsvd2')
//
//
//     // Если поле email не валидно, отображаем соответствующее сообщение об ошибке
//     showError();
//     // Затем предотвращаем стандартное событие отправки формы
//     event.preventDefault();
//     // alert('sdv');
//   }
// });
//
// function showError() {
//   if(name.validity.valueMissing) {
//     // Если поле пустое,
//     // отображаем следующее сообщение об ошибке
//     nameError.textContent = 'You need to enter an e-mail address.';
//   } else if(name.validity.typeMismatch) {
//     // Если поле содержит не email-адрес,
//     // отображаем следующее сообщение об ошибке
//     nameError.textContent = 'Entered value needs to be an e-mail address.';
//   } else if(name.validity.tooShort) {
//     // Если содержимое слишком короткое,
//     // отображаем следующее сообщение об ошибке
//     nameError.textContent = `Email should be at least ${ name.minLength } characters; you entered ${ name.value.length }.`;
//   }
//
//   // Задаём соответствующую стилизацию
//   nameError.className = 'error active';
// }
//
//     // btnform2open.addEventListener("click", function() {
//     //     const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle2"));
//     //     console.log('leftform2');
//     //     myModal.show();
//     // });
//
//     btnform3open.addEventListener("click", function() {
//         const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle3"));
//         myModal.show();
//     });
//
//     btnform4open.addEventListener("click", function() {
//         const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle4"));
//         myModal.show();
//     });
//
//     btnform5open.addEventListener("click", function() {
//         const myModal = new bootstrap.Modal(document.getElementById("exampleModalToggle5"));
//         myModal.show();
//     });
//
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
//
//
// });

// // Существуют разные способы получить DOM-узел; здесь мы определяем саму форму и
// // поле ввода email и элемент span, в который поместим сообщение об ошибке
// const form  = document.getElementsByTagName('form')[0];
//
// const email = document.getElementById('name');
// const emailError = document.querySelector('#mail + span.error');
//
// email.addEventListener('input', function (event) {
//   // Каждый раз, когда пользователь что-то вводит,
//   // мы проверяем, являются ли поля формы валидными
//
//   if (email.validity.valid) {
//     // Если на момент валидации какое-то сообщение об ошибке уже отображается,
//     // если поле валидно, удаляем сообщение
//     emailError.textContent = ''; // Сбросить содержимое сообщения
//     emailError.className = 'error'; // Сбросить визуальное состояние сообщения
//   } else {
//     // Если поле не валидно, показываем правильную ошибку
//     showError();
//   }
// });
//
// form.addEventListener('submit', function (event) {
//   // Если поле email валдно, позволяем форме отправляться
//
//   if(!email.validity.valid) {
//     // Если поле email не валидно, отображаем соответствующее сообщение об ошибке
//     showError();
//     // Затем предотвращаем стандартное событие отправки формы
//     event.preventDefault();
//   }
// });
//
// function showError() {
//   if(email.validity.valueMissing) {
//     // Если поле пустое,
//     // отображаем следующее сообщение об ошибке
//     emailError.textContent = 'You need to enter an e-mail address.';
//   } else if(email.validity.typeMismatch) {
//     // Если поле содержит не email-адрес,
//     // отображаем следующее сообщение об ошибке
//     emailError.textContent = 'Entered value needs to be an e-mail address.';
//   } else if(email.validity.tooShort) {
//     // Если содержимое слишком короткое,
//     // отображаем следующее сообщение об ошибке
//     emailError.textContent = `Email should be at least ${ email.minLength } characters; you entered ${ email.value.length }.`;
//   }
//
//   // Задаём соответствующую стилизацию
//   emailError.className = 'error active';
// }
