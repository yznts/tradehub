
function _API() {
    
    // Local vars
    var API_ADDR = undefined;
    

    // ---------------------
    // Prototype-related
    // ---------------------
    this.setApiAddr = function (addr, callback) {
        if (!addr.endsWith("/")) { addr += "/" }
        this.API_ADDR = addr;
        callback();
    }

    // ---------------------
    // Minor
    // ---------------------
    this.ping = function (callback) {
        $.get(this.API_ADDR+"version", callback);
    }
    this.CNY = function (callback) {
        $.get(this.API_ADDR+"currencies/CNY", function (data) {
            callback(parseFloat(data));
        });
    }

    // ---------------------
    // Services
    // ---------------------
    this.getAvServices = function (game, callback) {
        $.get(this.API_ADDR+"services/available/"+game, function (data) {
            var ordered = {}
            Object.keys(data).sort().forEach(function(key) {
                ordered[key] = data[key];
            });
            callback(ordered);
        })
    }


    // ---------------------
    // Rates
    // ---------------------
    this.getRatesByNames = function (game, s1, s2, s1_commission, s2_commission, names, callback) {
        $.post(this.API_ADDR+"rates/by_names/"+game, 
            {
                "names": names.join(","),
                "s1_name": s1,
                "s2_name": s2,
                "s1_commission": s1_commission,
                "s2_commission": s2_commission,
            }
        ).done(function (data) {
            callback(data);
        })
    }


}

var API = new _API();