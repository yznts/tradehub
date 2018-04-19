
let start_time = 0;

$(document).ready(function () {
    start_time = new Date().getTime();
    setInterval(updateTimer, 1000);
    InitDatatable();

    // Backport: Clear GET request params
    window.history.replaceState({}, document.title, "/table/"+game);
});

function updateTimer() {
    let timer = $("#timer");
    timer.html(Math.trunc((new Date().getTime() - start_time)/1000));
}

function InitDatatable() {
    let table = $('#dt');
    table = table.DataTable(dt);
    $("#dt").removeClass('dataTable');
    $('#dt_wrapper').click(postProcessor);
    postProcessor();
}

function postProcessor() {
    $('#dt td').each(function (index, element) {
        try {
            let cell = JSON.parse($(element).text());

            $(element).html('');

            if (cell['copy']) {
                $(element).append($('<button>', {class: 'btn btn-outline-dark copy', copytext: cell['val']}).append(
                    $('<i>', {class: 'fas fa-paste'})
                ).click(copyToClipboard));
            }

            if (cell['type'] === 'text')
                $(element).append($('<a>', {href: cell['link'], target: '_blank'}).text(cell['val']));
            if (cell['type'] === 'price')
                $(element).append($('<a>', {href: cell['link'], target: '_blank'}).text(parseFloat(cell['val']).toFixed(2)+'$'));
            if (cell['type'] === 'percent')
                $(element).append($('<a>', {href: cell['link'], target: '_blank'}).text(parseFloat(cell['val']).toFixed(2)+'%'));

            $(element).addClass(cell['class']);
        } catch (error) { }
        
    });
}

function copyToClipboard() {
    var $temp = $("<input>");
    $("body").append($temp);
    console.log($(this));
    $temp.val($(this).attr('copytext')).select();
    document.execCommand("copy");
    $temp.remove();
}


jQuery.fn.dataTableExt.oSort["text-desc"] = function(x, y) {
    x = JSON.parse(x);
    y = JSON.parse(y);
    return (x == 0 && y == 0) ? 0 : (x['val'] < y['val'] ? 1 : -1);
};

jQuery.fn.dataTableExt.oSort["text-asc"] = function(x, y) {
    x = JSON.parse(x);
    y = JSON.parse(y);
    return (x == 0 && y == 0) ? 0 : (x['val'] > y['val'] ? 1 : -1);
};


jQuery.fn.dataTableExt.oSort["number-desc"] = function(x, y) {
    x = JSON.parse(x);
    y = JSON.parse(y);
    return (x == 0 && y == 0) ? 0 : (parseFloat(x['val']) < parseFloat(y['val']) ? 1 : -1);
};

jQuery.fn.dataTableExt.oSort["number-asc"] = function(x, y) {
    x = JSON.parse(x);
    y = JSON.parse(y);
    return (x == 0 && y == 0) ? 0 : (parseFloat(x['val']) > parseFloat(y['val']) ? 1 : -1);
};
