

$(document).ready(function () {
    LoadSettings(function () {
        API.setApiAddr(settings.API_ADDR, ()=>(null));
        API.CNY(function (CNY) {

            $(".price").each(function () {
                var cny_price = $(this).text().replace("￥", "");
                var usd_price = cny_price / CNY;
                $(this).text(cny_price+"￥"+"/"+usd_price.toFixed(2)+"$");
                $(this).parent().html($(this).parent().html().replace("Purchase Price", "PO"));
            })

        })
    });
});
