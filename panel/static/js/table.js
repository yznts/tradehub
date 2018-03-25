function update() {
    // Extract selected services
    var selected_services = [];
    $(".service-checkbox").find("input").each(function (_, item) {
        if ($(item).is(":checked")) {
            selected_services.push($(item).val());
        }
    });
    //Extract selected S1 and S2
    var s1_name = $("#s1-select").val();
    var s2_name = $("#s2-select").val();

    // Extract commissions
    var s1_commission = $("#s1-commission").val();
    var s2_commission = $("#s2-commission").val();

    // Extract filters
    // Price
    var price_target = $("#price-filter-target").val();
    var price_from = $("#price-filter-from").val();
    var price_to = $("#price-filter-to").val();
    // Rates
    var rates_s1_s2_from = $("#rates-filter-s1-s2-from").val();
    var rates_s1_s2_to = $("#rates-filter-s1-s2-to").val();
    var rates_s2_s1_from = $("#rates-filter-s2-s1-from").val();
    var rates_s2_s1_to = $("#rates-filter-s2-s1-to").val();
    // Other
    var stattrack = $("#stattrack-checkbox").is(":checked");

    // Base url
    var url = "/table/"+GAME+"?";
    // Append selected services
    url += "services="+selected_services.join(",");
    // Append s1/s2 and commissions if all are filled with params
    if (s1_name !== "" && s2_name !== "" && s1_commission !== "" && s2_commission !== "") {
        url += "&s1_name="+s1_name;
        url += "&s2_name="+s2_name;
        url += "&s1_commission="+s1_commission;
        url += "&s2_commission="+s2_commission;
    }
    // Append price filter if fields are filled
    if (price_target !== "" && price_from !== "" && price_to !== "") {
        url += "&price_target="+price_target;
        url += "&price_from="+price_from;
        url += "&price_to="+price_to;
    }
    // Append rates filter if fields are filled
    if (rates_s1_s2_from !== "" && rates_s1_s2_to) {
        url += "&rates_s1_s2_from="+rates_s1_s2_from;
        url += "&rates_s1_s2_to="+rates_s1_s2_to;
    }
    if (rates_s2_s1_from !== "" && rates_s2_s1_to) {
        url += "&rates_s2_s1_from="+rates_s2_s1_from;
        url += "&rates_s2_s1_to="+rates_s2_s1_to;
    }
    if (stattrack) { url += "&stattrack=1" }
    else {url += "&stattrack=0"}
    // Relocate with new params
    window.location.replace(url);
}

function updateTimer() {
    $("#last-update-timer").text(parseInt($("#last-update-timer").text())+1);
}

function setUpdateTimes() {
    console.log($("#items-table").find("th"));
    $("#items-table").find("th").each(function () {
        var service = $(this).text();
        var u_time = last_updates[service];
        if (u_time !== undefined) {
            var temp = moment.unix(u_time);
            u_time = temp.format("DD/MM/YYYY HH:mm:ss");
            var node = $("<span>").addClass("last-update").text(u_time);
            $(this).append(node);
        }
    })
}

function setClipboard() {
    console.log($(this).attr("data-key"));
    var temp = $("<input>");
    $("body").append(temp);
    temp.val($(this).attr("data-key")).select();
    document.execCommand("copy");
    temp.remove();
}

$(document).ready(function () {

    // Update button
    $("#btn-update").click(update);

    // Bind clipboard
    $(".clipboard").click(setClipboard);

    // Data table
    $('#items-table').DataTable();

    // Timer
    setInterval(updateTimer, 1000);

    // Last updates times
    setUpdateTimes();
});