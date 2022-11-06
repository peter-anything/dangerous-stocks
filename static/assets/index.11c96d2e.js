import{R as F,j as t,aY as d,aZ as p,r as y,a as s,bh as m,f as C,bi as D}from"./index.21cb48c3.js";import{E as c,B as S,L as E}from"./index.cb11d379.js";import{C as B}from"./index.d0bd16d7.js";import{u as b,E as f}from"./useDynamicChart.02a00cab.js";import{a as e,O as _,b as L,g as N}from"./chart.ab068e89.js";import{T}from"./index.d6260645.js";import"./dayjs.min.645d5d5a.js";import"./index.fbb5b830.js";import"./index.d9038502.js";import"./DateRangePicker.7dd76537.js";import"./useDebounce.7b0fd4f3.js";import"./calendar.033a4b69.js";const P=[{title:"\u603B\u7533\u8BF7\u6570\uFF08\u6B21\uFF09",count:"1126",trendNum:"10%",trend:c.up},{title:"\u4F9B\u5E94\u5546\u6570\u91CF\uFF08\u4E2A\uFF09",count:"13",trendNum:"13%",trend:c.down},{title:"\u91C7\u8D2D\u5546\u54C1\u54C1\u7C7B\uFF08\u7C7B\uFF09",count:"4",trendNum:"10%",trend:c.up},{title:"\u7533\u8BF7\u4EBA\u6570\u91CF\uFF08\u4EBA\uFF09",count:"90",trendNum:"44%",trend:c.down},{title:"\u7533\u8BF7\u5B8C\u6210\u7387\uFF08%\uFF09",count:"80.5",trendNum:"70%",trend:c.up},{title:"\u5230\u8D27\u53CA\u65F6\u7387\uFF08%\uFF09",count:"78",trendNum:"16%",trend:c.up}],v=[{description:"SSL\u8BC1\u4E66\u53C8\u53EB\u670D\u52A1\u5668\u8BC1\u4E66\uFF0C\u817E\u8BAF\u4E91\u4E3A\u60A8\u63D0\u4F9B\u8BC1\u4E66\u7684\u4E00\u7AD9\u5F0F\u670D\u52A1\uFF0C\u5305\u62EC\u514D\u8D39\u3001\u4ED8\u8D39\u8BC1\u4E66\u7684\u7533\u8BF7\u3001\u7BA1\u7406\u53CA\u90E8",index:1,isSetup:!0,name:"SSL\u8BC1\u4E66",type:"D",icon:"user"},{description:"SSL\u8BC1\u4E66\u53C8\u53EB\u670D\u52A1\u5668\u8BC1\u4E66\uFF0C\u817E\u8BAF\u4E91\u4E3A\u60A8\u63D0\u4F9B\u8BC1\u4E66\u7684\u4E00\u7AD9\u5F0F\u670D\u52A1\uFF0C\u5305\u62EC\u514D\u8D39\u3001\u4ED8\u8D39\u8BC1\u4E66\u7684\u7533\u8BF7\u3001\u7BA1\u7406\u53CA\u90E8",index:1,isSetup:!0,name:"SSL\u8BC1\u4E66",type:"C",icon:"calendar"}],w=()=>t(B,{title:"\u672C\u6708\u91C7\u8D2D\u7533\u8BF7\u60C5\u51B5",header:!0,children:t(d,{gutter:[16,16],children:P.map(u=>t(p,{xs:6,xl:3,span:12,children:t(S,{title:u.title,trend:u.trend,trendNum:u.trendNum,count:u.count,desc:"\u73AF\u6BD4",border:!0})},u.title))})});var j=F.memo(w);const g=(u=[])=>{let o=_;return u.length>0&&(o=L(u,7,"YYYY-MM-DD")),{grid:{top:"5%",right:"10px",left:"30px",bottom:"60px"},legend:{left:"center",bottom:"0",orient:"horizontal",data:["\u676F\u5B50","\u8336\u53F6","\u8702\u871C","\u9762\u7C89"]},xAxis:{type:"category",data:o,boundaryGap:!1,axisLabel:{color:"rgba(0, 0, 0, 0.4)"},axisLine:{lineStyle:{color:"#E3E6EB",width:1}}},yAxis:{type:"value",axisLabel:{color:"rgba(0, 0, 0, 0.4)"}},tooltip:{trigger:"item"},series:[{showSymbol:!0,symbol:"circle",symbolSize:8,name:"\u676F\u5B50",stack:"\u603B\u91CF",data:[e(),e(),e(),e(),e(),e(),e()],type:"line",itemStyle:{borderColor:"#ffffff",borderWidth:1}},{showSymbol:!0,symbol:"circle",symbolSize:8,name:"\u8336\u53F6",stack:"\u603B\u91CF",data:[e(),e(),e(),e(),e(),e(),e()],type:"line",itemStyle:{borderColor:"#ffffff",borderWidth:1}},{showSymbol:!0,symbol:"circle",symbolSize:8,name:"\u8702\u871C",stack:"\u603B\u91CF",data:[e(),e(),e(),e(),e(),e(),e()],type:"line",itemStyle:{borderColor:"#ffffff",borderWidth:1}},{showSymbol:!0,symbol:"circle",symbolSize:8,name:"\u9762\u7C89",stack:"\u603B\u91CF",data:[e(),e(),e(),e(),e(),e(),e()],type:"line",itemStyle:{borderColor:"#ffffff",borderWidth:1}}]}},x=(u=[])=>{const[o,a,n]=N(u);return{xAxis:{data:o,axisLabel:{color:"rgba(0, 0, 0, 0.4)"},splitLine:{show:!1},axisLine:{lineStyle:{color:"#E3E6EB",width:1}}},yAxis:{type:"value",axisLabel:{color:"rgba(0, 0, 0, 0.4)"},nameTextStyle:{padding:[0,0,0,60]},axisTick:{show:!1},axisLine:{show:!1}},tooltip:{trigger:"item"},grid:{top:"5px",left:"25px",right:"5px",bottom:"60px"},legend:{left:"center",bottom:"0",orient:"horizontal",data:["\u6309\u6469\u4EEA","\u5496\u5561\u673A"],itemHeight:8,itemWidth:8},series:[{name:"\u6309\u6469\u4EEA",symbolSize:10,data:n,type:"scatter"},{name:"\u5496\u5561\u673A",symbolSize:10,data:a,type:"scatter"}]}},O="_purchaseTrendPanel_r5e4j_1",W="_productTrendPanel_r5e4j_4",z="_productLogo_r5e4j_14",k="_productName_r5e4j_25",M="_productDesc_r5e4j_31",R="_iconWrap_r5e4j_42",I="_lightBtn_r5e4j_45";var i={purchaseTrendPanel:O,productTrendPanel:W,productLogo:z,productName:k,productDesc:M,iconWrap:R,lightBtn:I};const Y=({type:u,isSetup:o,description:a,name:n,icon:r})=>s("div",{className:i.productTrendPanel,children:[s(d,{justify:"space-between",children:[t("div",{className:i.productLogo,children:t(m,{name:r})}),t(T,{theme:"success",children:o?"\u5DF2\u542F\u7528":"\u5DF2\u505C\u7528"})]}),t("p",{className:i.productName,children:n}),t("p",{className:i.productDesc,children:a}),s(d,{justify:"space-between",align:"middle",children:[s("div",{className:i.iconWrap,children:[t(C,{shape:"circle",disabled:!o,children:u}),t(C,{shape:"circle",disabled:!o,className:i.lightBtn,children:t(m,{name:"add"})})]}),t(D,{disabled:!o,options:[{content:"\u7BA1\u7406",value:"manage",onClick:()=>{}},{content:"\u5220\u9664",value:"delete",onClick:()=>{}}],children:t(m,{name:"more"})})]})]}),U=g(),$=()=>{const[u,o]=y.exports.useState(U),a=r=>{const l=g(r);o(l)},n=b(u,{placeholderColor:["legend.textStyle.color","xAxis.axisLabel.color","yAxis.axisLabel.color"]});return s(d,{className:i.purchaseTrendPanel,gutter:[16,16],children:[t(p,{xs:12,xl:9,children:t(B,{title:"\u91C7\u8D2D\u5546\u54C1\u7533\u8BF7\u8D8B\u52BF",subtitle:"(\u4EF6)",actions:E(a),header:!0,children:t(f,{option:n,notMerge:!0,lazyUpdate:!0,style:{height:453}})})}),t(p,{xs:12,xl:3,children:t(d,{gutter:[16,16],children:v.map((r,l)=>t(p,{xs:12,children:t(Y,{type:r.type,isSetup:r.isSetup,description:r.description,name:r.name,icon:r.icon})},l))})})]})};var G=F.memo($);const H="_satisfactionPanel_aca4b_1",K="_operation_aca4b_4",Z="_exportBtn_aca4b_7";var h={satisfactionPanel:H,operation:K,exportBtn:Z};const q=()=>{const u=x(),[o,a]=y.exports.useState(u),n=l=>{const A=x(l);a(A)},r=b(o,{placeholderColor:["legend.textStyle.color","xAxis.axisLabel.color","yAxis.axisLabel.color"]});return t("div",{className:h.satisfactionPanel,children:t(B,{title:"\u91C7\u8D2D\u5546\u54C1\u6EE1\u610F\u5EA6\u5206\u5E03",header:!0,actions:s("div",{className:h.operation,children:[E(n),t(C,{className:h.exportBtn,children:"\u5BFC\u51FA\u6570\u636E"})]}),children:t(f,{option:r,notMerge:!0,lazyUpdate:!0,style:{height:374}})})})};var J=F.memo(q),ce=y.exports.memo(()=>s("div",{children:[t(j,{}),t(G,{}),t(J,{})]}));export{ce as default};
