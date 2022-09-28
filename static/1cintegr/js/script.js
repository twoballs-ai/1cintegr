$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});

var token = "d9d839eea6af5bf1c146189a65c734a35651b6f2";
// Замените на свой API-ключ

// раскладываем по полочкам https://codepen.io/dadata/pen/vYRwEa
function join(arr /*, separator */) {
  var separator = arguments.length > 1 ? arguments[1] : ", ";
  return arr.filter(function(n){return n}).join(separator);
}

function geoQuality(qc_geo) {
  var localization = {
    "0": "точные",
    "1": "ближайший дом",
    "2": "улица",
    "3": "населенный пункт",
    "4": "город"
  };
  return localization[qc_geo] || qc_geo;
}

function geoLink(address) {
  return join(["<a target=\"_blank\" href=\"",
               "https://maps.yandex.ru/?text=",
               address.geo_lat, ",", address.geo_lon, "\">",
               address.geo_lat, ", ", address.geo_lon, "</a>"], "");
}

function showPostalCode(address) {
  $("#postal_code").val(address.postal_code);
}

function showRegion(address) {
  $("#region").val(join([
    join([address.region_type, address.region], " ")
    // ,
    // join([address.area_type, address.area], " ")
  ]));
}

function showCity(address) {
  $("#city").val(join([
    join([address.city_type, address.city], " "),
    join([address.settlement_type, address.settlement], " ")
  ]));
}

function showStreet(address) {
  $("#street").val(
    join([address.street_type, address.street], " ")
  );
}

function showHouse(address) {
  $("#house").val(join([
    join([address.house_type, address.house], " "),
    join([address.block_type, address.block], " ")
  ]));
}

function showFlat(address) {
  $("#flat").val(
    join([address.flat_type, address.flat], " ")
  );
}

function showGeo(address) {
  if (address.qc_geo != "5") {
    var geo = geoLink(address) + " (" + geoQuality(address.qc_geo) + ")";
    $("#geo").html(geo);
  }
}

function showSelected(suggestion) {
  var address = suggestion.data;
  showPostalCode(address);
  showRegion(address);
  showCity(address);
  showStreet(address);
  showHouse(address);
  showFlat(address);
  showGeo(address);
}

$("#address").suggestions({
  token: token,
  type: "ADDRESS",
  onSelect: showSelected
});


$('.btnTranslate1').click(function(){
  $('#form-2 [name="name"]').val($('#form-1 [name="name"]').val());
  $('#form-2 [name="description"]').val($('#form-1 [name="description"]').val());
  $('#form-2 [name="object_type"]').val($('#form-1 [name="object_type"]').val());
  $('#form-2 [name="PurposeObject"]').val($('#form-1 [name="PurposeObject"]').val());
  $('#form-2 [name="region"]').val($('#form-1 [name="region"]').val());
  $('#form-2 [name="address"]').val($('#form-1 [name="address"]').val());
  $('#form-2 [name="object_area"]').val($('#form-1 [name="object_area"]').val());
  $('#form-2 [name="LandCategory"]').val($('#form-1 [name="LandCategory"]').val());
  $('#form-2 [name="TypeOfPermittedUse"]').val($('#form-1 [name="TypeOfPermittedUse"]').val());
});
$('.btnTranslate2').click(function(){
  $('#form-3 [name="name"]').val($('#form-2 [name="name"]').val());
  $('#form-3 [name="description"]').val($('#form-2 [name="description"]').val());
  $('#form-3 [name="object_type"]').val($('#form-2 [name="object_type"]').val());
  $('#form-3 [name="PurposeObject"]').val($('#form-2 [name="PurposeObject"]').val());
  $('#form-3 [name="region"]').val($('#form-2 [name="region"]').val());
  $('#form-3 [name="address"]').val($('#form-2 [name="address"]').val());
  $('#form-3 [name="object_area"]').val($('#form-2 [name="object_area"]').val());
  $('#form-3 [name="LandCategory"]').val($('#form-2 [name="LandCategory"]').val());
  $('#form-3 [name="TypeOfPermittedUse"]').val($('#form-2 [name="TypeOfPermittedUse"]').val());
  // форма2
  $('#form-3 [name="RNFI"]').val($('#form-2 [name="RNFI"]').val());
  $('#form-3 [name="RNFI_date"]').val($('#form-2 [name="RNFI_date"]').val());
  $('#form-3 [name="owner_nomer"]').val($('#form-2 [name="owner_nomer"]').val());
  $('#form-3 [name="owner_date"]').val($('#form-2 [name="owner_date"]').val());
  $('#form-3 [name="RecordNumberVEGRP"]').val($('#form-2 [name="RecordNumberVEGRP"]').val());
  $('#form-3 [name="DateRecordsVEGRP"]').val($('#form-2 [name="DateRecordsVEGRP"]').val());
  $('#form-3 [name="TypeofRightOwner"]').val($('#form-2 [name="TypeofRightOwner"]').val());
  $('#form-3 [name="BalanceAccountNumber"]').val($('#form-2 [name="BalanceAccountNumber"]').val());
  $('#form-3 [name="date_of_registration_of_another_right"]').val($('#form-2 [name="date_of_registration_of_another_right"]').val());
  $('#form-3 [name="inventory_number').val($('#form-2 [name="inventory_number"]').val());
  $('#form-3 [name="balance_number"]').val($('#form-2 [name="balance_number"]').val());
  $('#form-3 [name="CadastralNumber"]').val($('#form-2 [name="CadastralNumber"]').val());
  $('#form-3 [name="Date_of_assignment_cadastral"]').val($('#form-2 [name="Date_of_assignment_cadastral"]').val());
  $('#form-3 [name="type_pravoobladatel"]').val($('#form-2 [name="type_pravoobladatel"]').val());
  $('#form-3 [name="Initial_cost"]').val($('#form-2 [name="Initial_cost"]').val());
  $('#form-3 [name="residual_value"]').val($('#form-2 [name="residual_value"]').val());
});
$('.btnTranslate3').click(function(){
  $('#form-4 [name="name"]').val($('#form-3 [name="name"]').val());
  $('#form-4 [name="description"]').val($('#form-3 [name="description"]').val());
  $('#form-4 [name="object_type"]').val($('#form-3 [name="object_type"]').val());
  $('#form-4 [name="PurposeObject"]').val($('#form-3 [name="PurposeObject"]').val());
  $('#form-4 [name="region"]').val($('#form-3 [name="region"]').val());
  $('#form-4 [name="address"]').val($('#form-3 [name="address"]').val());
  $('#form-4 [name="object_area"]').val($('#form-3 [name="object_area"]').val());
  $('#form-4 [name="LandCategory"]').val($('#form-3 [name="LandCategory"]').val());
  $('#form-4 [name="TypeOfPermittedUse"]').val($('#form-3 [name="TypeOfPermittedUse"]').val());
  // форма2
  $('#form-4 [name="RNFI"]').val($('#form-3 [name="RNFI"]').val());
  $('#form-4 [name="RNFI_date"]').val($('#form-3 [name="RNFI_date"]').val());
  $('#form-4 [name="owner_nomer"]').val($('#form-3 [name="owner_nomer"]').val());
  $('#form-4 [name="owner_date"]').val($('#form-3 [name="owner_date"]').val());
  $('#form-4 [name="RecordNumberVEGRP"]').val($('#form-3 [name="RecordNumberVEGRP"]').val());
  $('#form-4 [name="DateRecordsVEGRP"]').val($('#form-3 [name="DateRecordsVEGRP"]').val());
  $('#form-4 [name="TypeofRightOwner"]').val($('#form-3 [name="TypeofRightOwner"]').val());
  $('#form-4 [name="BalanceAccountNumber"]').val($('#form-3 [name="BalanceAccountNumber"]').val());
  $('#form-4 [name="date_of_registration_of_another_right"]').val($('#form-3 [name="date_of_registration_of_another_right"]').val());
  $('#form-4 [name="inventory_number').val($('#form-3 [name="inventory_number"]').val());
  $('#form-4 [name="balance_number"]').val($('#form-3 [name="balance_number"]').val());
  $('#form-4 [name="CadastralNumber"]').val($('#form-3 [name="CadastralNumber"]').val());
  $('#form-4 [name="Date_of_assignment_cadastral"]').val($('#form-3 [name="Date_of_assignment_cadastral"]').val());
  $('#form-4 [name="type_pravoobladatel"]').val($('#form-3 [name="type_pravoobladatel"]').val());
  $('#form-4 [name="Initial_cost"]').val($('#form-3 [name="Initial_cost"]').val());
  $('#form-4 [name="residual_value"]').val($('#form-3 [name="residual_value"]').val());
  // 3форма
  $('#form-4 [name="historical_Category"]').val($('#form-3 [name="historical_Category"]').val());
  $('#form-4 [name="UGROKN_number"]').val($('#form-3 [name="UGROKN_number"]').val());
});

$('.btnTranslate4').click(function(){
  $('#form-5 [name="name"]').val($('#form-4 [name="name"]').val());
  $('#form-5 [name="description"]').val($('#form-4 [name="description"]').val());
  $('#form-5 [name="object_type"]').val($('#form-4 [name="object_type"]').val());
  $('#form-5 [name="PurposeObject"]').val($('#form-4 [name="PurposeObject"]').val());
  $('#form-5 [name="region"]').val($('#form-4 [name="region"]').val());
  $('#form-5 [name="address"]').val($('#form-4 [name="address"]').val());
  $('#form-5 [name="object_area"]').val($('#form-4 [name="object_area"]').val());
  $('#form-5 [name="LandCategory"]').val($('#form-4 [name="LandCategory"]').val());
  $('#form-5 [name="TypeOfPermittedUse"]').val($('#form-4 [name="TypeOfPermittedUse"]').val());
  // форма2
  $('#form-5 [name="RNFI"]').val($('#form-4 [name="RNFI"]').val());
  $('#form-5 [name="RNFI_date"]').val($('#form-4 [name="RNFI_date"]').val());
  $('#form-5 [name="owner_nomer"]').val($('#form-4 [name="owner_nomer"]').val());
  $('#form-5 [name="owner_date"]').val($('#form-4 [name="owner_date"]').val());
  $('#form-5 [name="RecordNumberVEGRP"]').val($('#form-4 [name="RecordNumberVEGRP"]').val());
  $('#form-5 [name="DateRecordsVEGRP"]').val($('#form-4 [name="DateRecordsVEGRP"]').val());
  $('#form-5 [name="TypeofRightOwner"]').val($('#form-4 [name="TypeofRightOwner"]').val());
  $('#form-5 [name="BalanceAccountNumber"]').val($('#form-4 [name="BalanceAccountNumber"]').val());
  $('#form-5 [name="date_of_registration_of_another_right"]').val($('#form-4 [name="date_of_registration_of_another_right"]').val());
  $('#form-5 [name="inventory_number').val($('#form-4 [name="inventory_number"]').val());
  $('#form-5 [name="balance_number"]').val($('#form-4 [name="balance_number"]').val());
  $('#form-5 [name="CadastralNumber"]').val($('#form-4 [name="CadastralNumber"]').val());
  $('#form-5 [name="Date_of_assignment_cadastral"]').val($('#form-4 [name="Date_of_assignment_cadastral"]').val());
  $('#form-5 [name="type_pravoobladatel"]').val($('#form-4 [name="type_pravoobladatel"]').val());
  $('#form-5 [name="Initial_cost"]').val($('#form-4 [name="Initial_cost"]').val());
  $('#form-5 [name="residual_value"]').val($('#form-4 [name="residual_value"]').val());
  // 3форма
  $('#form-5 [name="historical_Category"]').val($('#form-4 [name="historical_Category"]').val());
  $('#form-5 [name="UGROKN_number"]').val($('#form-4 [name="UGROKN_number"]').val());
  // 4 форма
  $('#form-5 [name="KindEncumbrances"]').val($('#form-4 [name="KindEncumbrances"]').val());
  $('#form-5 [name="encumbrance_area"]').val($('#form-4 [name="encumbrance_area"]').val());
  $('#form-5 [name="encumbrance_cost"]').val($('#form-4 [name="encumbrance_cost"]').val());
  $('#form-5 [name="person_encumbrance"]').val($('#form-4 [name="person_encumbrance"]').val());
  $('#form-5 [name="Other_payments"]').val($('#form-4 [name="Other_payments"]').val());
  $('#form-5 [name="start_encumbrance"]').val($('#form-4 [name="start_encumbrance"]').val());
  $('#form-5 [name="end_encumbrance"]').val($('#form-4 [name="end_encumbrance"]').val());
  $('#form-5 [name="start_use"]').val($('#form-4 [name="start_use"]').val());
  $('#form-5 [name="end_use"]').val($('#form-4 [name="end_use"]').val());
  $('#form-5 [name="Payment_foruse"]').val($('#form-4 [name="Payment_foruse"]').val());


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