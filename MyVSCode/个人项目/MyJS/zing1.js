
var p = ["ctime", "id", "type", "page", "count", "version"];


var g = function(e) {
    var t = {};
    return Object.keys(e).sort().forEach((function(n) {
        t[n] = e[n]
    }
    )),
    t
}

v = function(e) {
    var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : "&"
      , n = encodeURIComponent;
    return Object.keys(e).map((function(t) {
        return n(e[t]).length > 5e3 ? "" : "".concat(n(t), "=").concat(n(e[t]))
    }
    )).filter((function(e) {
        return "" !== e
    }
    )).join(t)
}

var finalize = function(e) {
    return e && this._append(e),
    this._doFinalize()
}
var t = "ctime=1689236738version=1.9.52"

o = Object.create || function() {
    function e() {}
    return function(t) {
        var n;
        return e.prototype = t,
        n = new e,
        e.prototype = null,
        n
    }
}

var mixIn = function(e) {
    for (var t in e)
        e.hasOwnProperty(t) && (this[t] = e[t]);
    e.hasOwnProperty("toString") && (this.toString = e.toString)
}

var hh = function(e) {
    var t = o(this);
    return e && t.mixIn(e),
    t.hasOwnProperty("init") && this.init !== t.init || (t.init = function() {
        t.$super.init.apply(this, arguments)
    }
    ),
    t.init.prototype = t,
    t.$super = this,
    t
}

var f = function(t, n) {
    return hh(e).init(n).finalize(t)
}

function m(e, t) {
    var n = function(e) {
        var t = g(e)
          , n = [];
        for (var r in t)
            -1 !== p.indexOf(r) && null !== e[r] && void 0 !== e[r] && "" !== e[r] && (n[r] = t[r]);
        return v(n, "")
    }(t)
      , r = f()("" + n);
    return h()(e + r, "acOrvUS15XRW2o9JksiK1KgQ6Vbds8ZW")
}



e = "/api/v2/app/get/recommend-keyword"
t = {
    "ctime": 1689236517,
    "version": "1.9.52"
}

console.log(m(e,t))