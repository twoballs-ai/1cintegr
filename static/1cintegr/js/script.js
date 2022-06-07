$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});



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