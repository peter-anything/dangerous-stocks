import{r as c,w as a}from"./index.1cdf4813.js";/**
 * tdesign v0.42.4
 * (c) 2022 tdesign
 * @license MIT
 */function o(s){var t=c.exports.useRef(s);t.current=s;var e=c.exports.useRef();return e.current||(e.current=function(){for(var u=arguments.length,n=new Array(u),r=0;r<u;r++)n[r]=arguments[r];return t.current.apply(this,n)}),e.current}/**
 * tdesign v0.42.4
 * (c) 2022 tdesign
 * @license MIT
 */var i=function(t,e,u){var n=o(t),r=c.exports.useCallback(a(n,e,u),[n,e,u]);return c.exports.useEffect(function(){return r.cancel},[r]),r};export{i as a,o as u};
