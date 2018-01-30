
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
    data = {};

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

    data.order = order;
    data.sort = sort;

    $('.filter').each(function(){
        if (this.value != ''){
            name = $(this).data('field');
            data[name] = this.value;
        }
    });

    $.ajax({
        url: listURL,
        type: 'POST',
        data: data,
        dataType: 'json',
        success: function(data){
            $('.list-table tbody').html(data.reply);
            $('.pagin').html(data.pagin);
            $('.selectpicker').selectpicker('refresh');
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
    $('body').on('keyup', '.keyup', function(){
        updateTable();
    });
    $('body').on('change', '.change', function(){
        updateTable();
    });
    $('body').on('click', '.page_select', function(){
        $('.page_filter').val($(this).text());
        updateTable();
    });
    $('.selectpicker').selectpicker('refresh');
    $('.datepicker').val('');
    $('.datepicker').daterangepicker({
        autoUpdateInput: false,
        locale: {
            cancelLabel: 'Clear',
            applyLabel: 'OK',
        },
        'applyClass': 'btn-info',
    });
    $('.datepicker').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
        updateTable();
    });

    $('.datepicker').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
        updateTable();
    });
});
