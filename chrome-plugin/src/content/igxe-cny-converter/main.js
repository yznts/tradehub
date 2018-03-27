

$(document).ready(function () {
    LoadSettings(function () {
        API.setApiAddr(settings.API_ADDR, ()=>(null));
        API.CNY(function (CNY) {

            // Main page
            $(".mod-hotEquipment").each(function (_, element) {
                var price_field = $(element).find(".s3").find("strong");
                var price = parseFloat(price_field.html());
                price_field.html(price+"¥/"+(price/CNY).toFixed(2)+"$");
            });

            // Product page
                // Overview
            $(".s2").each(function (_, element) {
                var price_field = $(element).find("b");
                if (price_field.html() === undefined)
                    return;
                var price = parseFloat(price_field.html().replace("￥", ""));
                price_field.html(price+"¥/"+(price/CNY).toFixed(2)+"$");
            });
            $(".s3").each(function (_, element) {
                var price_field = $(element).find("strong");
                if (price_field.html() === undefined)
                    return;
                var price = parseFloat(price_field.html().replace("￥", ""));
                price_field.html(price+"¥/"+(price/CNY).toFixed(2)+"$");
            });
                // Tables
            $(".t4").each(function (_, element) {
                var price_field = $(element).find("strong");
                if (price_field.html() === undefined)
                    return;
                var price = parseFloat(price_field.html().replace("￥", ""));
                price_field.html(price+"¥/"+(price/CNY).toFixed(2)+"$");
            });
                // Bind to purchases button (table not loading on start)
            $("#product_purchases").click(function () {
                $("#purcheases_div").find("tr").each(function (_, element) {
                    var price_field = $($(element).find("td")[1]);
                    if (price_field === undefined)
                        return;
                    if (price_field.html() === undefined)
                        return;
                    var price = parseFloat(price_field.html().replace("￥", ""));
                    price_field.html(price+"¥/"+(price/CNY).toFixed(2)+"$");
                })
            });


        })
    });
});
