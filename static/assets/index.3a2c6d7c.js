import{r as h,j as e,c as E,a as l,aY as b,aZ as r,d as B,f as F}from"./index.1cdf4813.js";import{C as A}from"./common.module.d7e709a7.js";import{U as y,F as D}from"./index.5e904e21.js";import{S as o}from"./index.62ae6118.js";import{R as m}from"./index.35dbae16.js";import{a as c}from"./index.84f3a1e1.js";import"./formModel.ad8b7348.js";import"./index.ef5945d7.js";import{T as g}from"./index.ed80cb8a.js";import{A as s}from"./index.6164e513.js";import{M as x}from"./index.e8866a69.js";import"./useDebounce.98b6b877.js";import"./error-circle-filled.3c40b142.js";import"./delete.94406282.js";import"./index.25a11f79.js";import"./DateRangePicker.416824bd.js";import"./dayjs.min.e36e4af8.js";import"./calendar.f212d2e1.js";import"./index.ba78343d.js";/**
 * tdesign v0.42.4
 * (c) 2022 tdesign
 * @license MIT
 */var N=y;const _="_formContainer_rhia5_1",T="_titleText_rhia5_10",q="_dateCol_rhia5_15";var i={formContainer:_,titleText:T,dateCol:q};const{FormItem:a}=D,{Option:t}=o,{Group:R}=s,u={name:"",type:"",payment:"",partyA:"",partyB:"",signDate:"",effectiveDate:"",endDate:"",remark:"",notary:"",file:[]};var K=h.exports.memo(()=>{const p=h.exports.useRef(),f=d=>{var n,C;d.validateResult===!0&&(console.log("form \u503C",(C=(n=p.current)==null?void 0:n.getFieldsValue)==null?void 0:C.call(n,!0)),x.info("\u63D0\u4EA4\u6210\u529F"))},v=({file:d})=>{console.error(`\u6587\u4EF6 ${d.name} \u4E0A\u4F20\u5931\u8D25`)};return e("div",{className:E(A.pageWithColor),children:e("div",{className:i.formContainer,children:l(D,{ref:p,onSubmit:f,labelWidth:100,labelAlign:"top",children:[e("div",{className:i.titleBox,children:e("div",{className:i.titleText,children:"\u5408\u540C\u4FE1\u606F"})}),l(b,{gutter:[32,24],children:[e(r,{span:6,children:e(a,{label:"\u5408\u540C\u540D\u79F0",name:"name",initialData:u.name,rules:[{required:!0,message:"\u5408\u540C\u540D\u79F0\u5FC5\u586B",type:"error"}],children:e(B,{placeholder:"\u8BF7\u8F93\u5165\u5185\u5BB9"})})}),e(r,{span:6,children:e(a,{label:"\u5408\u540C\u7C7B\u578B",name:"type",initialData:u.type,rules:[{required:!0,message:"\u5408\u540C\u7C7B\u578B\u5FC5\u586B",type:"error"}],children:l(o,{placeholder:"\u8BF7\u9009\u62E9\u7C7B\u578B",children:[e(t,{label:"\u7C7B\u578BA",value:"A"},"A"),e(t,{label:"\u7C7B\u578BB",value:"B"},"B"),e(t,{label:"\u7C7B\u578BC",value:"C"},"C")]})})}),e(r,{span:12,children:l(a,{label:"\u5408\u540C\u6536\u4ED8\u7C7B\u578B",name:"payment",initialData:u.payment,rules:[{required:!0}],children:[l(m.Group,{children:[e(m,{value:"0",children:"\u6536\u6B3E"}),e(m,{value:"1",children:"\u4ED8\u6B3E"})]}),e(B,{placeholder:"\u8BF7\u8F93\u5165\u91D1\u989D",style:{width:160}})]})}),e(r,{span:6,children:e(a,{label:"\u7532\u65B9",name:"partyA",initialData:u.partyA,rules:[{required:!0}],children:l(o,{placeholder:"\u8BF7\u9009\u62E9\u7C7B\u578B",children:[e(t,{label:"\u516C\u53F8A",value:"A"},"A"),e(t,{label:"\u516C\u53F8B",value:"B"},"B"),e(t,{label:"\u516C\u53F8C",value:"C"},"C")]})})}),e(r,{span:6,children:e(a,{label:"\u4E59\u65B9",name:"partyB",initialData:u.partyB,rules:[{required:!0}],children:l(o,{value:"A",placeholder:"\u8BF7\u9009\u62E9\u7C7B\u578B",children:[e(t,{label:"\u516C\u53F8A",value:"A"},"A"),e(t,{label:"\u516C\u53F8B",value:"B"},"B"),e(t,{label:"\u516C\u53F8C",value:"C"},"C")]})})}),e(r,{span:6,className:i.dateCol,rules:[{required:!0}],children:e(a,{label:"\u5408\u540C\u7B7E\u8BA2\u65E5\u671F",name:"signDate",initialData:u.signDate,children:e(c,{mode:"date"})})}),e(r,{span:6,className:i.dateCol,rules:[{required:!0}],children:e(a,{label:"\u5408\u540C\u751F\u6548\u65E5\u671F",name:"effectiveDate",initialData:u.effectiveDate,children:e(c,{mode:"date"})})}),e(r,{span:6,className:i.dateCol,rules:[{required:!0}],children:e(a,{label:"\u5408\u540C\u7ED3\u675F\u65E5\u671F",name:"endDate",initialData:u.endDate,children:e(c,{mode:"date"})})}),e(r,{span:6,children:e(a,{label:"\u5408\u540C\u6587\u4EF6",name:"file",initialData:u.file,children:e(N,{onFail:v,tips:"\u8BF7\u4E0A\u4F20pdf\u6587\u4EF6\uFF0C\u5927\u5C0F\u572860M\u4EE5\u5185",action:"//service-bv448zsw-1257786608.gz.apigw.tencentcs.com/api/upload-demo"})})})]}),e("div",{className:i.titleBox,children:e("div",{className:i.titleText,children:"\u5176\u4ED6\u4FE1\u606F"})}),e(a,{label:"\u5907\u6CE8",name:"remark",initialData:u.remark,children:e(g,{placeholder:"\u8BF7\u8F93\u5165\u5907\u6CE8"})}),e(a,{label:"\u516C\u8BC1\u4EBA",name:"notary",initialData:u.notary,children:l(R,{children:[e(s,{children:"D"}),e(s,{children:"S"}),e(s,{children:"+"})]})}),l(a,{children:[e(F,{type:"submit",theme:"primary",children:"\u63D0\u4EA4"}),e(F,{type:"reset",style:{marginLeft:12},children:"\u91CD\u7F6E"})]})]})})})});export{K as default};
