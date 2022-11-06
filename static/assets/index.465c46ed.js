var he=Object.defineProperty,pe=Object.defineProperties;var me=Object.getOwnPropertyDescriptors;var U=Object.getOwnPropertySymbols;var xe=Object.prototype.hasOwnProperty,ge=Object.prototype.propertyIsEnumerable;var J=(e,t,r)=>t in e?he(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,W=(e,t)=>{for(var r in t||(t={}))xe.call(t,r)&&J(e,r,t[r]);if(U)for(var r of U(t))ge.call(t,r)&&J(e,r,t[r]);return e},k=(e,t)=>pe(e,me(t));import{r as n,R as p,ap as be,a0 as te,o as ae,q as Q,aP as Oe,c as ne,y as z,j as m,C as V,bq as X}from"./index.21cb48c3.js";function Se(e,t){var r=n.exports.useRef(null),a=n.exports.useRef(null);a.current=t;var c=n.exports.useRef(null);n.exports.useEffect(function(){s()});var s=n.exports.useCallback(function(){var u=c.current,l=a.current,i=u||(l?l instanceof Element?l:l.current:null);r.current&&r.current.element===i&&r.current.subscriber===e||(r.current&&r.current.cleanup&&r.current.cleanup(),r.current={element:i,subscriber:e,cleanup:i?e(i):void 0})},[e]);return n.exports.useEffect(function(){return function(){r.current&&r.current.cleanup&&(r.current.cleanup(),r.current=null)}},[]),n.exports.useCallback(function(u){c.current=u,s()},[s])}function Y(e,t,r){return e[t]?e[t][0]?e[t][0][r]:e[t][r]:t==="contentBoxSize"?e.contentRect[r==="inlineSize"?"width":"height"]:void 0}function ze(e){e===void 0&&(e={});var t=e.onResize,r=n.exports.useRef(void 0);r.current=t;var a=e.round||Math.round,c=n.exports.useRef(),s=n.exports.useState({width:void 0,height:void 0}),u=s[0],l=s[1],i=n.exports.useRef(!1);n.exports.useEffect(function(){return i.current=!1,function(){i.current=!0}},[]);var o=n.exports.useRef({width:void 0,height:void 0}),b=Se(n.exports.useCallback(function(O){return(!c.current||c.current.box!==e.box||c.current.round!==a)&&(c.current={box:e.box,round:a,instance:new ResizeObserver(function(v){var P=v[0],E=e.box==="border-box"?"borderBoxSize":e.box==="device-pixel-content-box"?"devicePixelContentBoxSize":"contentBoxSize",x=Y(P,E,"inlineSize"),h=Y(P,E,"blockSize"),g=x?a(x):void 0,d=h?a(h):void 0;if(o.current.width!==g||o.current.height!==d){var S={width:g,height:d};o.current.width=g,o.current.height=d,r.current?r.current(S):i.current||l(S)}})}),c.current.instance.observe(O,{box:e.box}),function(){c.current&&c.current.instance.unobserve(O)}},[e.box,a]),e.ref);return n.exports.useMemo(function(){return{ref:b,width:u.width,height:u.height}},[b,u.width,u.height])}/**
 * tdesign v0.42.4
 * (c) 2022 tdesign
 * @license MIT
 */var H=p.createContext("default"),T=function(t){var r=t.children,a=t.size;return p.createElement(H.Consumer,null,function(c){return p.createElement(H.Provider,{value:a||c},r)})};/**
 * tdesign v0.42.4
 * (c) 2022 tdesign
 * @license MIT
 */var Pe={hideOnLoadFailed:!1,shape:"circle"},Ee={cascading:"right-up",size:"medium"};/**
 * tdesign v0.42.4
 * (c) 2022 tdesign
 * @license MIT
 */var Re=["className","cascading","collapseAvatar","max","placement","popupProps","size","children"];function ee(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter(function(c){return Object.getOwnPropertyDescriptor(e,c).enumerable})),r.push.apply(r,a)}return r}function y(e){for(var t=1;t<arguments.length;t++){var r=arguments[t]!=null?arguments[t]:{};t%2?ee(Object(r),!0).forEach(function(a){z(e,a,r[a])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):ee(Object(r)).forEach(function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(r,a))})}return e}var K=function(t){var r,a=ae(),c=a.classPrefix,s="".concat(c,"-avatar"),u=t.className,l=t.cascading,i=t.collapseAvatar,o=t.max,b=t.placement,O=t.popupProps,v=t.size,P=t.children,E=te(t,Re),x=p.Children.toArray(P),h;x.length>0&&(h=x.map(function(R,w){return p.cloneElement(R,y({key:"avatar-group-item-".concat(w)},R.props))}));var g=ne("".concat(s,"-group"),u,(r={},z(r,"".concat(s,"--offset-right"),l==="right-up"),z(r,"".concat(s,"--offset-left"),l==="left-up"),r)),d=x.length;if(o&&d>o){var S=h.slice(0,o),j=h.slice(o,d),_="+".concat(d-o),A=y(y({},O),{},{placement:b}),L=O?m(X,k(W({},y({},A)),{children:i?p.createElement(C,{size:v},i):p.createElement(C,{size:v},_)})):m(X,{placement:b,content:j,trigger:"hover",showArrow:!0,children:i?p.createElement(C,{size:v},i):p.createElement(C,{size:v},_)},"avatar-popup-key");return S.push(L),m(T,{size:v,children:m("div",{className:g,children:S})})}return m(T,{size:v,children:m("div",k(W({},y({className:g},E)),{children:h}))})};K.displayName="AvatarGroup";K.defaultProps=Ee;var we=["alt","hideOnLoadFailed","icon","image","shape","size","onError","children","style","className"];function re(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter(function(c){return Object.getOwnPropertyDescriptor(e,c).enumerable})),r.push.apply(r,a)}return r}function q(e){for(var t=1;t<arguments.length;t++){var r=arguments[t]!=null?arguments[t]:{};t%2?re(Object(r),!0).forEach(function(a){z(e,a,r[a])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):re(Object(r)).forEach(function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(r,a))})}return e}var M=be(function(e,t){var r,a=e.alt,c=e.hideOnLoadFailed,s=e.icon,u=e.image,l=e.shape,i=e.size,o=e.onError,b=e.children,O=e.style,v=e.className,P=te(e,we),E=n.exports.useContext(H),x=ae(),h=x.classPrefix,g=n.exports.useState(1),d=Q(g,2),S=d[0],j=d[1],_=n.exports.useState(!0),A=Q(_,2),L=A[0],R=A[1],w=n.exports.useRef(null),G=n.exports.useRef(null),f=i==="default"?E:i,B=4,Z=function(){if(!(!G.current||!w.current)){var $=G.current.offsetWidth,I=w.current.offsetWidth;$!==0&&I!==0&&B*2<I&&j(I-B*2<$?(I-B*2)/$:1)}},ce=ze({onResize:Z}),ie=ce.ref,se=function(){o&&o(),!c&&R(!1)};n.exports.useEffect(function(){R(!0),j(1)},[e.image]),n.exports.useEffect(function(){Z()},[]);var ue=Oe(),N=ue.SIZE,oe=f&&!N[f]?{width:f,height:f,fontSize:"".concat(Number.parseInt(f,10)/2,"px")}:{},le=f&&!N[f]?{width:f,height:f}:{},F="".concat(h,"-avatar"),fe=ne(F,v,(r={},z(r,N[f],!!N[f]),z(r,"".concat(F,"--").concat(l),!!l),z(r,"".concat(F,"-icon"),!!s),r)),D;if(u&&L)D=m("img",{src:u,alt:a,style:le,onError:se});else if(s)D=s;else{var ve={transform:"scale(".concat(S,")")};D=m("span",{ref:V(t,G,ie),style:ve,children:b})}return m("div",k(W({},q({ref:V(t,w),className:fe,style:q(q({},oe),O)},P)),{children:D}))},{Group:K});M.displayName="Avatar";M.defaultProps=Pe;var C=M;/**
 * tdesign v0.42.4
 * (c) 2022 tdesign
 * @license MIT
 */var je=C;export{je as A};
