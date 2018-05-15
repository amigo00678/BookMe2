
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
        if ($(this).attr('type') == 'checkbox'){
            if ($(this)[0].checked){
                name = $(this).data('field');
                data[name] = $(this).data('value');
            }
        } else if (this.value != ''){
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
            $('.files-list-js').html(data.reply);
            $('.files-list-js').html(data.reply);
            $('.pagin-js').html(data.pagin);
            $('.selectpicker').selectpicker('refresh');
        },
    });
}

function clearFilters(){
    $('.filter[type=checkbox]').each(function(index, object){
        object.checked = false;
    });
    updateTable();
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
    $('body').on('click', '.pagination-link', function(){
        $('.page_filter').val($(this).data('page'));
        updateTable();
    });

    $('body').on('click', '.modal-button', function(){
        var target = $(this).data('target');
        var title = $(this).data('title');
        openModal(target, title);
    });
    $('body').on('click',
        '.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button',
        function(){
            closeModals();
    });

    $('body').on('click', '.dropdown', function(event){
        event.stopPropagation();
        $(this).addClass('is-active');
    });
    $(document).click(function(){
        $('.dropdown').removeClass('is-active');
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
    $('.datetimepicker').datepicker({ autoclose: true });
    var carousels = bulmaCarousel.attach();

    $('body').on('click', '.book-button', function(){
        data = {};
        price_ids = [];
        $('.room-select').each(function(el){
            if (this.checked){
                id = $(this).data('id');
                price_ids.push(id);
            }
        });

        prices = price_ids.join("-");
        prices = encodeURI(prices);

        href = $(this).data('href')+'?prices='+(prices);
        window.location.replace(href);
    });
});

// Modals

function openModal(target, title) {
    $(document.documentElement).addClass('is-clipped');
    $('#'+target).find('.modal-card-title').text(title);
    $('#'+target).addClass('is-active');
}

function closeModals() {
    $(document.documentElement).removeClass('is-clipped');
    $('.modal').removeClass('is-active');
}
