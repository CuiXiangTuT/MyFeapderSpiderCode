var e = "/api/v2/app/get/recommend-keyword"
var t = {ctime:1675760196,version:'1.8.30'}
var o = "X5BM3w8N7MKozC0B85o4KMlzLZKhV00y"

o = function() {
    return Math.round((new Date).getTime() / 1e3)
}
p = ["ctime", "id", "type", "page", "count", "version"];
function f(){
    return function(t, n) {
        return e.init(n).finalize(t)
    }
}

function g(e){

    init: function(e) {
        this.cfg = this.cfg.extend(e),
        this.reset()
    }
    var t = {};
        return Object.keys(e).sort().forEach((function(n) {
            t[n] = e[n]
        }
        )),
        t
}


function h(t,n){
        return g.HMAC.init(e,n).finalize(t)
}



function v(e){
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
console.log(m(e,t))