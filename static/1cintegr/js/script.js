$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});

var token = "d9d839eea6af5bf1c146189a65c734a35651b6f2";

var type = "ADDRESS";
var $region = $("#region");
var $area = $("#area");
var $city = $("#city");
var $settlement = $("#settlement");
var $street = $("#street");
var $house = $("#house");

function showPostalCode(suggestion) {
  $("#postal_code").val(suggestion.data.postal_code);
}

function clearPostalCode() {
  $("#postal_code").val("");
}

// регион
$region.suggestions({
  token: token,
  type: type,
  hint: false,
  bounds: "region"
});

// район
$area.suggestions({
  token: token,
  type: type,
  hint: false,
  bounds: "area",
  constraints: $region
});

// город и населенный пункт
$city.suggestions({
  token: token,
  type: type,
  hint: false,
  bounds: "city",
  constraints: $area,
  onSelect: showPostalCode,
  onSelectNothing: clearPostalCode
});

// geolocateCity($city);

// город и населенный пункт
$settlement.suggestions({
  token: token,
  type: type,
  hint: false,
  bounds: "settlement",
  constraints: $city,
  onSelect: showPostalCode,
  onSelectNothing: clearPostalCode
});

// улица
$street.suggestions({
  token: token,
  type: type,
  hint: false,
  bounds: "street",
  constraints: $settlement,
  onSelect: showPostalCode,
  onSelectNothing: clearPostalCode
});

// дом
$house.suggestions({
  token: token,
  type: type,
  hint: false,
  bounds: "house",
  constraints: $street,
  onSelect: showPostalCode,
  onSelectNothing: clearPostalCode
});

$('.btn').click(function(){
  $('#form-2 [name="postal_code"]').val($('#form-1 [name="postal_code"]').val());
  $('#form-2 [name="flat"]').val($('#form-1 [name="flat"]').val());
  $('#form-2 [name="house"]').val($('#form-1 [name="house"]').val());
  $('#form-2 [name="street"]').val($('#form-1 [name="street"]').val());
  $('#form-2 [name="settlement"]').val($('#form-1 [name="settlement"]').val());
  $('#form-2 [name="city"]').val($('#form-1 [name="city"]').val());
  $('#form-2 [name="area"]').val($('#form-1 [name="area"]').val());
  $('#form-2 [name="region"]').val($('#form-1 [name="region"]').val());
});

// const myModal = document.getElementById('myModal')
// const myInput = document.getElementById('myInput')
//
// myModal.addEventListener('shown.bs.modal', () => {
//   myInput.focus()
// })


// $('#editable').click(function (){
//
// });
// $('#save').hide();
//
// $('#editButton').click(function (){
//     $('#editable').focus();
//     $('#editButton').hide();
//     $('#save').show();
// });
//
// $('#save').click(function (){
//     $('#editButton').show();
//     $('#save').hide();
//
// });

Fancybox.bind('[data-fancybox="gallery"]', {
  animated: false,
  showClass: false,
  hideClass: false,

  click: false,

  dragToClose: false,

  Image: {
    zoom: false,
  },

  Toolbar: {
    display: [{ id: "counter", position: "center" }, "close"],
  },
});