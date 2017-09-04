
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var csrftoken = getCookie('csrftoken');

function updateTable(){
    asc = $('.asc').data('field');
    desc = $('.desc').data('field');
    if (typeof asc != 'undefined'){
        sort = asc;
        order = 'asc';
    } else if (typeof desc != 'undefined'){
        sort = desc;
        order = 'desc';
    } else {
        order = '';
        sort = '';
    }
    data = {
        order: order,
        sort: sort,
    }
    $.ajax({
        url: listURL,
        type: 'POST',
        data: JSON.stringify(data),
        dataType: 'json',
        success: function(data){
            $('.list-table tbody').replaceWith(data);
        },
    });
}

$(document).ready(function(){
    $('body').on('click', '.sortable', function(){
        if ($(this).hasClass('asc')){
            sortClass='desc';
        } else if ($(this).hasClass('desc')){
            sortClass='asc';
        } else {
            sortClass='desc';
        }
        $('.sortable').removeClass('asc');
        $('.sortable').removeClass('desc');
        $(this).addClass(sortClass);
        updateTable();
    });
});
