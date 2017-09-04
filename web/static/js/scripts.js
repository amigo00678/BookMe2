
function updateTable(){
    $.ajax({
        url: listURL,
        success: function(){console.log('AJAX success!!!')},
    });
}

$(document).ready(function(){
    $('body').on('click', '.sortable', updateTable);
});
