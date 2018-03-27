

// Shared

function UpdateRates(callback) {
    flow.exec(
        function () { UpdateCache(this) },
        function () { UpdateView(this) },
        function () { callback() },
    )
}

var cache = {};
function UpdateCache(callback) {
    flow.exec(
        function () { ExtractNames(this) },
        function (names) { 
            API.getRatesByNames(
                settings.game,
                settings.s1,
                FULLNAME,
                settings.s1_commission,
                settings.s2_commission,
                names,
                this
            )
        },
        function (rates) { cache = rates; this() },
        function () { UpdateView(this) },
    )
    
}



// Service-related

function ExtractNames(callback) {
    var needed_items = [];
    $(".itemblock").each(function (_, element) {
        needed_items.push($(element).attr("data-name"))
    });
    needed_items.filter(function (value, index, self) {
        return self.indexOf(value) === index;
    });
    callback(needed_items);
}

function UpdateView(callback) {
    $(".itemblock").each(function (index, item) {
        
        // Bind update cache event if no bind yet
        if ($(item).attr("bind") === undefined) {
            $(item).bind("click", function () {
                setTimeout(function(){ UpdateView(function(){}) }, 300);
            });
            $(item).attr("bind", true);
        }
        
        // Remove prev data
        $(item).removeAttr("s1-s2-rate");
        $(item).removeAttr("s2-s1-rate");
        $(item).find(".rates-node").remove();

        // Extract info
        var info = cache[$(item).attr("data-name")];
        if (!info) {
            return;
        }

        // Pass if no price in info
        if (!("s1-price" in info) || !("s2-price" in info)) {
            return;
        }
        if (info["s1-price"] === 0 || info["s2-price"] === 0) {
            return;
        }

        // Create rates node
        var rates_node = $("<a>").addClass("rates-node");
        rates_node.attr("href", info["s1-link"]);
        rates_node.html(
            "<span class='s1-s2'></span>" +
            "<span class='separator'>/</span>" +
            "<span class='s2-s1'></span><br>" +
            "<span class='price'></span>"
        );
        $(item).append(rates_node);
        $(item).css("position", "relative");

        // Set fields content
        rates_node.find(".s1-s2").html(info["s1-s2-rate"].toFixed(2)+"%");
        rates_node.find(".s2-s1").html(info["s2-s1-rate"].toFixed(2)+"%");
        rates_node.find(".price").html(info["s1-price"].toFixed(2)+"$");
        $(item).attr("s1-s2-rate", info["s1-s2-rate"].toFixed(2));
        $(item).attr("s2-s1-rate", info["s2-s1-rate"].toFixed(2));
        // Set color
        if (!info["s1-av"]) {
            rates_node.css("color", "#aaa");
        } else {
            rates_node.css("color", "white");
        }
    });
    callback();
}

function SortS1S2(callback) {
    $("#bots_inv").find(".itemwrap").sort(function (a, b) {
        a = $(a).find(".itemblock")[0];
        b = $(b).find(".itemblock")[0];
        var a_rate = a.getAttribute("s1-s2-rate");
        var b_rate = b.getAttribute("s2-s1-rate");
        if (a_rate === null) a_rate = -1000;
        if (b_rate === null) b_rate = -1000;
        return b_rate-a_rate;
    }).appendTo("#bots_inv");
    callback();
}

function SortS2S1(callback) {
    $("#bots_inv").find(".itemwrap").sort(function (a, b) {
        a = $(a).find(".itemblock")[0];
        b = $(b).find(".itemblock")[0];
        var a_rate = a.getAttribute("s2-s1-rate");
        var b_rate = b.getAttribute("s2-s1-rate");
        if (a_rate === null) a_rate = -1000;
        if (b_rate === null) b_rate = -1000;
        return b_rate-a_rate;
    }).appendTo("#bots_inv");
    callback();
}

function AddControls(callback) {
    callback();
}

function UpdateControls(callback) {
    callback();
}