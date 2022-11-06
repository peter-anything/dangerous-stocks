import{r,j as e,a,aY as b,aZ as i,d as C,f as d,b as R,h as N,bu as T,bv as c,bw as k,F,c as y,ad as P}from"./index.1cdf4813.js";import{F as D}from"./index.5e904e21.js";import{n as j}from"./DateRangePicker.416824bd.js";import{M as x}from"./index.e8866a69.js";import{C as E}from"./common.module.d7e709a7.js";import{T as I}from"./index.1c2739e7.js";import{D as L}from"./index.ef5945d7.js";import{T as W}from"./index.676cd174.js";import"./formModel.ad8b7348.js";import"./index.62ae6118.js";import"./index.25a11f79.js";import"./useDebounce.98b6b877.js";import"./error-circle-filled.3c40b142.js";import"./delete.94406282.js";import"./index.ba78343d.js";import"./dayjs.min.e36e4af8.js";import"./calendar.f212d2e1.js";import"./index.35dbae16.js";const{FormItem:h}=D,V=l=>{const u=r.exports.useRef();return e("div",{className:"list-common-table-query",children:e(D,{ref:u,onSubmit:p=>{var n,s;p.validateResult===!0&&x.info("\u63D0\u4EA4\u6210\u529F");const o=(s=(n=u==null?void 0:u.current)==null?void 0:n.getFieldsValue)==null?void 0:s.call(n,!0);l.onSubmit(o)},onReset:()=>{l.onCancel(),x.info("\u91CD\u7F6E\u6210\u529F")},labelWidth:80,colon:!0,children:a(b,{children:[e(i,{flex:"1",children:a(b,{gutter:[16,16],children:[e(i,{span:3,xs:12,sm:6,xl:3,children:e(h,{label:"\u80A1\u7968\u4EE3\u7801",name:"code",children:e(C,{placeholder:"\u8BF7\u8F93\u5165\u80A1\u7968\u4EE3\u7801"})})}),e(i,{span:3,xs:12,sm:6,xl:3,children:e(h,{label:"\u80A1\u7968\u540D\u79F0",name:"name",children:e(C,{placeholder:"\u8BF7\u8F93\u5165\u80A1\u7968\u540D\u79F0"})})}),e(i,{span:3,xs:12,sm:6,xl:3,children:e(h,{label:"\u6362\u624B\u7387",name:"turnoverRate",children:e(j,{placeholder:"\u8BF7\u8F93\u5165\u6362\u624B\u7387"})})})]})}),a(i,{flex:"160px",children:[e(d,{theme:"primary",type:"submit",style:{margin:"0px 20px"},children:"\u67E5\u8BE2"}),e(d,{type:"reset",variant:"base",theme:"default",children:"\u91CD\u7F6E"})]})]})})})};var M=r.exports.memo(V);const S=()=>{const l=R(),u=N(T),[g,f]=r.exports.useState([0,1]),[p,o]=r.exports.useState(!1),{loading:n,stockList:s,current:A,pageSize:B,total:_}=u;r.exports.useEffect(()=>(l(c({pageSize:u.pageSize,current:u.current})),()=>{l(k())}),[]);function w(t){f(t)}function K(t){console.log(t)}function z(t){console.log(t),o(!0)}function q(){o(!1)}return a(F,{children:[e(b,{justify:"start",style:{marginBottom:"20px"},children:e(M,{onSubmit:async t=>{console.log("real"),l(c({pageSize:u.pageSize,current:1,code:t.code,name:t.name}))},onCancel:()=>{}})}),e(I,{loading:n,data:s,columns:[{colKey:"row-select",fixed:"left",type:"multiple"},{align:"left",width:200,ellipsis:!0,colKey:"code",title:"\u80A1\u7968\u4EE3\u7801"},{align:"left",width:200,ellipsis:!0,colKey:"name",title:"\u80A1\u7968\u540D\u79F0"},{align:"left",width:200,ellipsis:!0,colKey:"market",title:"\u5E02\u573A"},{align:"left",width:200,ellipsis:!0,colKey:"category",title:"\u5206\u7C7B"},{align:"left",width:200,ellipsis:!0,colKey:"type",title:"\u7C7B\u578B"},{align:"left",fixed:"right",width:200,colKey:"op",title:"\u64CD\u4F5C",cell(t){return a(F,{children:[e(d,{theme:"primary",variant:"text",onClick:()=>{K(t)},children:"\u7BA1\u7406"}),e(d,{theme:"primary",variant:"text",onClick:()=>{z(t)},children:"\u5220\u9664"})]})}}],rowKey:"index",selectedRowKeys:g,hover:!0,onSelectChange:w,pagination:{pageSize:B,total:_,current:A,showJumper:!0,onCurrentChange(t,v){l(c({pageSize:v.pageSize,current:v.current}))},onPageSizeChange(t){l(c({pageSize:t,current:1}))}}}),e(L,{header:"\u786E\u8BA4\u5220\u9664\u5F53\u524D\u6240\u9009\u5408\u540C\uFF1F",visible:p,onClose:q,children:e("p",{children:"\u5220\u9664\u540E\u7684\u6240\u6709\u5408\u540C\u4FE1\u606F\u5C06\u88AB\u6E05\u7A7A,\u4E14\u65E0\u6CD5\u6062\u590D"})})]})},J=()=>e("div",{className:y(E.pageWithPadding,E.pageWithColor),children:e(S,{})});r.exports.memo(J);const O=[{label:"\u6DF1\u5733\u603B\u90E8",value:0,children:[{label:"\u603B\u529E",value:"0-0"},{label:"\u5E02\u573A\u90E8",value:"0-1",children:[{label:"\u91C7\u8D2D1\u7EC4",value:"0-1-0"},{label:"\u91C7\u8D2D2\u7EC4",value:"0-1-1"}]},{label:"\u6280\u672F\u90E8",value:"0-2"}]},{label:"\u5317\u4EAC\u603B\u90E8",value:1,children:[{label:"\u603B\u529E",value:"1-0"},{label:"\u5E02\u573A\u90E8",value:"1-1",children:[{label:"\u91C7\u8D2D1\u7EC4",value:"1-1-0"},{label:"\u91C7\u8D2D2\u7EC4",value:"1-1-1"}]}]},{label:"\u4E0A\u6D77\u603B\u90E8",value:2,children:[{label:"\u5E02\u573A\u90E8",value:"2-0"},{label:"\u8D22\u52A1\u90E8",value:"2-1",children:[{label:"\u8D22\u52A11\u7EC4",value:"2-1-0"},{label:"\u8D22\u52A12\u7EC4",value:"2-1-1"}]}]},{label:"\u6E56\u5357",value:3},{label:"\u6E56\u5317",value:4}],Y="_content_120qd_1",Z="_treeContent_120qd_4",$="_search_120qd_9",G="_tableContent_120qd_12";var m={content:Y,treeContent:Z,search:$,tableContent:G};const he=()=>a("div",{className:y(E.pageWithColor,m.content),children:[a("div",{className:m.treeContent,children:[e(C,{className:m.search,suffixIcon:e(P,{}),placeholder:"\u8BF7\u8F93\u5165\u5173\u952E\u8BCD"}),e(W,{data:O,activable:!0,hover:!0,transition:!0})]}),e("div",{className:m.tableContent,children:e(S,{})})]});export{he as default};
