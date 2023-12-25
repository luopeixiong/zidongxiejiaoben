function m(t) {
    return m = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
        return typeof t
    }
    : function(t) {
        return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
    }
    ,
    m(t)
}
function y(t, e, r) {
    return (e = function(t) {
        var e = function(t, e) {
            if ("object" !== m(t) || null === t)
                return t;
            var r = t[Symbol.toPrimitive];
            if (void 0 !== r) {
                var n = r.call(t, "string");
                if ("object" !== m(n))
                    return n;
                throw new TypeError("@@toPrimitive must return a primitive value.")
            }
            return String(t)
        }(t);
        return "symbol" === m(e) ? e : String(e)
    }(e))in t ? Object.defineProperty(t, e, {
        value: r,
        enumerable: !0,
        configurable: !0,
        writable: !0
    }) : t[e] = r,
    t
}
function v(t) {
    for (var e = 1; e < arguments.length; e++) {
        var r = null != arguments[e] ? arguments[e] : {};
        e % 2 ? h(Object(r), !0).forEach((function(e) {
            y(t, e, r[e])
        }
        )) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(r)) : h(Object(r)).forEach((function(e) {
            Object.defineProperty(t, e, Object.getOwnPropertyDescriptor(r, e))
        }
        ))
    }
    return t
}
var t = {
    "Api": "zeldaEasy.broadscope-bailian.enterprise-data.upload-policy",
    "V": "1.0",
    "Data": {
        "reqDTO": {
            "mainAccountUid": "1031035430341318",
            "fileName": "cs.docx"
        },
        "cornerstoneParam": {
            "protocol": "V2",
            "console": "ONE_CONSOLE",
            "productCode": "p_efm",
            "switchAgent": 22928,
            "switchUserType": 3,
            "domain": "bailian.console.aliyun.com",
            "userNickName": "",
            "userPrincipalName": "",
            "xsp_lang": "zh-CN"
        }
    }
}
var e = "zeldaEasy.broadscope-bailian.enterprise-data.upload-policy"
var h = v({params: JSON.stringify(v({Api: e, V: c.V || "1.0", Data: m}, r._params))}, s)