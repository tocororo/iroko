(window.webpackJsonp=window.webpackJsonp||[]).push([[1],{KSnW:function(l,n,e){"use strict";e.r(n);var u=e("CcnG"),a=function(){},t=e("pMnS"),i=e("ZYCi"),o=function(){function l(){}return l.prototype.ngOnInit=function(){},l}(),r=u.Ua({encapsulation:0,styles:[[""]],data:{}});function c(l){return u.ob(0,[(l()(),u.Wa(0,16777216,null,null,1,"router-outlet",[],null,null,null,null,null)),u.Va(1,212992,null,0,i.m,[i.b,u.V,u.k,[8,null],u.i],null,null)],function(l,n){l(n,1,0)},null)}var b=u.Sa("toco-catalog",o,function(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,1,"toco-catalog",[],null,null,null,c,r)),u.Va(1,114688,null,0,o,[],null,null)],function(l,n){l(n,1,0)},null)},{},{},[]),d=e("BHnd"),m=e("y4qS"),s=e("21Lb"),g=e("OzfB"),p=e("bujt"),h=e("UodH"),f=e("dWZg"),y=e("lLAP"),w=e("wFw1"),x=e("pIm3"),k=e("lzlj"),V=e("FVSy"),_=e("Fzqc"),v=e("NvT6"),S=e("Blfk"),W=e("Ip0R"),j=e("mVsa"),C=e("eDkP"),O=e("Mr+X"),P=e("SMsm"),M=e("2Q+G"),D=e("76cv"),N=e("mrSG"),I=e("5Qyk"),L=e("+qD4"),R=e("+h9m"),A=e("Wakl"),T=function(l){function n(n,e,u){var a=l.call(this,n,e)||this;return a.componentFactoryResolver=n,a.childrenService=e,a.service=u,a}return Object(N.c)(n,l),n.prototype.ngOnInit=function(){var n=this;l.prototype.ngOnInit.call(this),this.addOperator(),E.forEach(function(l){n.filters_data.push(l)}),this.service.getJournalsVocab().subscribe(function(l){l.data.vocabularies.forEach(function(l){n.service.getTerminosByVocab(l.name).subscribe(function(e){n.filters_data.push({index:n.filters_data.length,field:"terms",type:"select-autocomplete",placeholder:l.name,name:l.name,idVocab:l.id,selectOptions:e.data.terms,is_enabled:!0})})})})},n.prototype.addOperator=function(){var l=new I.b(L.a,{field:"op",value:!0,name:["AND","OR"],is_enabled:!1,index:-1}),n=this.componentFactoryResolver.resolveComponentFactory(l.component);this.adHost.viewContainerRef.createComponent(n).instance.data=l.data},n}(e("Ilue").a),E=[{index:0,field:"title",type:"search",placeholder:"T\xedtulo",name:"T\xedtulo",is_enabled:!0},{index:1,field:"issn",type:"text",placeholder:"ISSN",name:"ISSN",is_enabled:!0},{index:2,field:"rnps",type:"number",placeholder:"RNPS",name:"RNPS",is_enabled:!0}],z=u.Ua({encapsulation:0,styles:[[".width-100[_ngcontent-%COMP%]{width:100%}.mat-menu-item[_ngcontent-%COMP%]{height:37px}"]],data:{}});function F(l){return u.ob(0,[(l()(),u.Na(0,null,null,0))],null,null)}function J(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,3,null,null,null,null,null,null,null)),(l()(),u.Wa(1,0,null,null,2,"button",[["class","mat-menu-item"],["mat-menu-item",""],["role","menuitem"]],[[2,"mat-menu-item-highlighted",null],[2,"mat-menu-item-submenu-trigger",null],[1,"tabindex",0],[1,"aria-disabled",0],[1,"disabled",0]],[[null,"click"],[null,"mouseenter"]],function(l,n,e){var a=!0,t=l.component;return"click"===n&&(a=!1!==u.gb(l,2)._checkDisabled(e)&&a),"mouseenter"===n&&(a=!1!==u.gb(l,2)._handleMouseEnter()&&a),"click"===n&&(a=!1!==t.addFilter(l.parent.context.index)&&a),a},M.c,M.b)),u.Va(2,180224,[[2,4]],0,j.d,[u.l,W.d,y.e,[2,j.h]],null,null),(l()(),u.mb(3,0,[" "," "]))],null,function(l,n){l(n,1,0,u.gb(n,2)._highlighted,u.gb(n,2)._triggersSubmenu,u.gb(n,2)._getTabIndex(),u.gb(n,2).disabled.toString(),u.gb(n,2).disabled||null),l(n,3,0,n.parent.context.$implicit.name)})}function Y(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,null,null,null,null,null,null,null)),(l()(),u.Na(16777216,null,null,1,null,J)),u.Va(2,16384,null,0,W.k,[u.V,u.S],{ngIf:[0,"ngIf"]},null),(l()(),u.Na(0,null,null,0))],function(l,n){l(n,2,0,n.context.$implicit.is_enabled)},null)}function H(l){return u.ob(0,[u.kb(402653184,1,{adHost:0}),(l()(),u.Na(16777216,null,null,1,null,F)),u.Va(2,16384,[[1,4]],0,D.a,[u.V],null,null),(l()(),u.Wa(3,16777216,null,null,5,"button",[["aria-haspopup","true"],["mat-icon-button",""]],[[8,"disabled",0],[2,"_mat-animation-noopable",null],[1,"aria-expanded",0]],[[null,"mousedown"],[null,"keydown"],[null,"click"]],function(l,n,e){var a=!0;return"mousedown"===n&&(a=!1!==u.gb(l,5)._handleMousedown(e)&&a),"keydown"===n&&(a=!1!==u.gb(l,5)._handleKeydown(e)&&a),"click"===n&&(a=!1!==u.gb(l,5)._handleClick(e)&&a),a},p.d,p.b)),u.Va(4,180224,null,0,h.b,[u.l,f.a,y.e,[2,w.a]],null,null),u.Va(5,1196032,null,0,j.f,[C.c,u.l,u.V,j.b,[2,j.c],[8,null],[2,_.b],y.e],{menu:[0,"menu"]},null),(l()(),u.Wa(6,0,null,0,2,"mat-icon",[["class","mat-icon"],["role","img"]],[[2,"mat-icon-inline",null]],null,null,O.b,O.a)),u.Va(7,638976,null,0,P.a,[u.l,P.c,[8,null]],null,null),(l()(),u.mb(-1,0,["add"])),(l()(),u.Wa(9,0,null,null,6,"mat-menu",[],null,null,null,M.d,M.a)),u.jb(6144,null,j.h,null,[j.c]),u.Va(11,1294336,[["menu",4]],2,j.c,[u.l,u.D,j.a],null,null),u.kb(603979776,2,{items:1}),u.kb(335544320,3,{lazyContent:0}),(l()(),u.Na(16777216,null,0,1,null,Y)),u.Va(15,278528,null,0,W.j,[u.V,u.S,u.w],{ngForOf:[0,"ngForOf"]},null)],function(l,n){var e=n.component;l(n,5,0,u.gb(n,11)),l(n,7,0),l(n,11,0),l(n,15,0,e.filters_data)},function(l,n){l(n,3,0,u.gb(n,4).disabled||null,"NoopAnimations"===u.gb(n,4)._animationMode,u.gb(n,5).menuOpen||null),l(n,6,0,u.gb(n,7).inline)})}var X=e("b1+6"),$=e("4epT"),U=e("KyXN"),q=e("nb4M"),B=e("F/XL"),G=e("p0ib"),K=e("p0Sj"),Z=e("15JJ"),Q=e("67Y/"),ll=e("9Z1F"),nl=e("cCwZ"),el=e("AytR"),ul=function(){function l(l,n,e){this.service=l,this.metadata=n,this.filterService=e,this.journalList=[],this.loading=!0,this.dataSource=new d.l,this.columnsToDisplay=["title","rnps","p-issn","url"],this.length=0,this.pageSize=5,this.pageSizeOptions=[5,10,15,20],this.irokoHost=el.a.irokoHost+"/catalog",this.layoutPosition=[{name:"Derecha",layout:"row-reverse",aling:"center baseline",width:"22"},{name:"Izquierda",layout:"row",aling:"center baseline",width:"22"},{name:"Arriba",layout:"column",aling:"center center",width:"90"},{name:"Abajo",layout:"column-reverse",aling:"center center",width:"90"}],this.currentlayout=this.layoutPosition[1]}return l.prototype.ngOnInit=function(){var l=this;this.metadata.setTitleDescription("Cat\xe1logo de Revistas Cient\xedficas",""),this.paginator.firstPage(),this.paginator.pageSize=5,this.service.getJournalsCount().subscribe(function(n){l.length=n.data.count}),this.fetchJournalData(),this.filterService.paramsChanged.subscribe(function(n){l.params=n,l.fetchJournalData()})},l.prototype.fetchJournalData=function(){var l=this;this.loading=!0;var n=new Array;Object(G.a)().pipe(Object(K.a)({}),Object(Z.a)(function(){return l.loading=!0,l.service.getJournalsPage(l.paginator.pageSize,l.paginator.pageIndex,l.params)}),Object(Q.a)(function(e){return l.loading=!1,l.length=e.data.sources.count,e.data.sources.data.forEach(function(l){var e=new U.b(0,0);e.id=l.id,e.tocoID=l.uuid;var u=new U.c;u.url=null!=l.data?l.data.url:"",u.title=l.name,u.subtitle=l.subtitle,u.shortname=l.shortname;var a=new U.a;a.e=null!=l.data?l.data.issn.e:"",a.l=null!=l.data?l.data.issn.l:"",a.p=null!=l.data?l.data.issn.p:"",u.issn=a,u.rnps=null!=l.data?l.data.rnps:"",u.logo=null!=l.data?l.data.logo:"",u.purpose=l.purpose,u.description=null!=l.data?l.data.description:"",e.jinformation=u,n.push(e)}),n}),Object(ll.a)(function(n){return l.loading=!1,console.log("ERRORRR  "+n),Object(B.a)([])})).subscribe(function(n){return l.dataSource.data=n})},l.prototype.onScrollUp=function(){},l.prototype.isEmpty=function(){return 0==this.journalList.length&&(this.loading=!1,!0)},l.prototype.isLoading=function(){return this.loading},l.prototype.openme=function(){var l=navigator.userAgent.match(/Android/i),n=navigator.userAgent.match(/BlackBerry/i),e=navigator.userAgent.match(/iPhone|iPad|iPod/i),u=navigator.userAgent.match(/Opera Mini/i),a=navigator.userAgent.match(/IEMobile/i);return null==l&&null==n&&null==e&&null==u&&null==a},l.prototype.changeLayoutPosition=function(l){this.currentlayout=this.layoutPosition[l]},l}(),al=u.Ua({encapsulation:0,styles:[[".width-card[_ngcontent-%COMP%]{width:30%;min-width:240px;margin-left:24px;margin-top:24px}.card-float-left[_ngcontent-%COMP%]{float:left}.center-spinner[_ngcontent-%COMP%]{width:90.5%;min-width:240px;margin-left:24px;margin-right:24px;margin-top:24px}.back-grey[_ngcontent-%COMP%]{background:rgba(0,0,0,.01);margin:1.5em 1em;padding:1em;min-width:18em}.width-90[_ngcontent-%COMP%]{width:90%}.width-93[_ngcontent-%COMP%]{width:93.5%}table[_ngcontent-%COMP%]{width:90%}.margin1em[_ngcontent-%COMP%]{margin:1em}.menu-pull-right[_ngcontent-%COMP%]{flex:1 1 auto}table.mat-table[_ngcontent-%COMP%]{width:100%}tr.example-detail-row[_ngcontent-%COMP%]{height:0}tr.example-element-row[_ngcontent-%COMP%]:not(.example-expanded-row):hover{background:#f5f5f5}tr.example-element-row[_ngcontent-%COMP%]:not(.example-expanded-row):active{background:#efefef}.example-element-row[_ngcontent-%COMP%]   td[_ngcontent-%COMP%]{border-bottom-width:0}.example-element-detail[_ngcontent-%COMP%]{overflow:hidden;display:flex}.example-element-diagram[_ngcontent-%COMP%]{min-width:80px;border:2px solid #000;padding:8px;font-weight:lighter;margin:8px 0;height:104px}.example-element-symbol[_ngcontent-%COMP%]{font-weight:700;font-size:40px;line-height:normal}.example-element-description[_ngcontent-%COMP%]{padding:16px}.example-element-description-attribution[_ngcontent-%COMP%]{opacity:.5}"]],data:{animation:[{type:7,name:"detailExpand",definitions:[{type:0,name:"collapsed",styles:{type:6,styles:{height:"0px",minHeight:"0",display:"none"},offset:null},options:void 0},{type:0,name:"expanded",styles:{type:6,styles:{height:"*"},offset:null},options:void 0},{type:1,expr:"expanded <=> collapsed",animation:{type:4,styles:null,timings:"225ms cubic-bezier(0.4, 0.0, 0.2, 1)"},options:null}],options:{}}]}});function tl(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"th",[["class","mat-header-cell"],["mat-header-cell",""],["role","columnheader"]],null,null,null,null,null)),u.Va(1,16384,null,0,d.e,[m.d,u.l],null,null),(l()(),u.mb(-1,null,["Titulo"]))],null,null)}function il(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"td",[["class","mat-cell"],["mat-cell",""],["role","gridcell"]],null,null,null,null,null)),u.Va(1,16384,null,0,d.a,[m.d,u.l],null,null),(l()(),u.mb(2,null,[" "," "]))],null,function(l,n){l(n,2,0,n.context.$implicit.jinformation.title)})}function ol(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"th",[["class","mat-header-cell"],["mat-header-cell",""],["role","columnheader"]],null,null,null,null,null)),u.Va(1,16384,null,0,d.e,[m.d,u.l],null,null),(l()(),u.mb(-1,null,["RNPS"]))],null,null)}function rl(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"td",[["class","mat-cell"],["mat-cell",""],["role","gridcell"]],null,null,null,null,null)),u.Va(1,16384,null,0,d.a,[m.d,u.l],null,null),(l()(),u.mb(2,null,[" "," "]))],null,function(l,n){l(n,2,0,n.context.$implicit.jinformation.rnps)})}function cl(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"th",[["class","mat-header-cell"],["mat-header-cell",""],["role","columnheader"]],null,null,null,null,null)),u.Va(1,16384,null,0,d.e,[m.d,u.l],null,null),(l()(),u.mb(-1,null,["P-ISSN"]))],null,null)}function bl(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"td",[["class","mat-cell"],["mat-cell",""],["role","gridcell"]],null,null,null,null,null)),u.Va(1,16384,null,0,d.a,[m.d,u.l],null,null),(l()(),u.mb(2,null,[" "," "]))],null,function(l,n){l(n,2,0,n.context.$implicit.jinformation.issn.p)})}function dl(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"th",[["class","mat-header-cell"],["mat-header-cell",""],["role","columnheader"]],null,null,null,null,null)),u.Va(1,16384,null,0,d.e,[m.d,u.l],null,null),(l()(),u.mb(-1,null,["URL"]))],null,null)}function ml(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"td",[["class","mat-cell"],["mat-cell",""],["role","gridcell"]],null,null,null,null,null)),u.Va(1,16384,null,0,d.a,[m.d,u.l],null,null),(l()(),u.mb(2,null,[" "," "]))],null,function(l,n){l(n,2,0,n.context.$implicit.jinformation.url)})}function sl(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,9,"td",[["class","mat-cell"],["mat-cell",""],["role","gridcell"]],[[1,"colspan",0]],null,null,null,null)),u.Va(1,16384,null,0,d.a,[m.d,u.l],null,null),(l()(),u.Wa(2,0,null,null,7,"div",[["class","example-element-detail"]],[[24,"@detailExpand",0]],null,null,null,null)),(l()(),u.Wa(3,0,null,null,0,"div",[["class","example-element-description e2e-inner-html-bound"]],[[8,"innerHTML",1]],null,null,null,null)),(l()(),u.Wa(4,0,null,null,5,"div",[["class","example-element-description"],["fxLayout","row"],["fxLayoutAlign","center end"]],null,null,null,null,null)),u.Va(5,737280,null,0,s.d,[g.h,u.l,g.l],{layout:[0,"layout"]},null),u.Va(6,737280,null,0,s.c,[g.h,u.l,[6,s.d],g.l],{align:[0,"align"]},null),(l()(),u.Wa(7,0,null,null,2,"a",[["color","primary"],["mat-flat-button",""]],[[8,"href",4],[1,"tabindex",0],[1,"disabled",0],[1,"aria-disabled",0],[2,"_mat-animation-noopable",null]],[[null,"click"]],function(l,n,e){var a=!0;return"click"===n&&(a=!1!==u.gb(l,8)._haltDisabledEvents(e)&&a),a},p.c,p.a)),u.Va(8,180224,null,0,h.a,[f.a,y.e,u.l,[2,w.a]],{color:[0,"color"]},null),(l()(),u.mb(-1,0,[" Ver "]))],function(l,n){l(n,5,0,"row"),l(n,6,0,"center end"),l(n,8,0,"primary")},function(l,n){var e=n.component;l(n,0,0,e.columnsToDisplay.length),l(n,2,0,n.context.$implicit==e.expandedElement?"expanded":"collapsed"),l(n,3,0,n.context.$implicit.jinformation.description),l(n,7,0,u.Ya(2,"",e.irokoHost,"/",n.context.$implicit.tocoID,""),u.gb(n,8).disabled?-1:u.gb(n,8).tabIndex||0,u.gb(n,8).disabled||null,u.gb(n,8).disabled.toString(),"NoopAnimations"===u.gb(n,8)._animationMode)})}function gl(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"tr",[["class","mat-header-row"],["mat-header-row",""],["role","row"]],null,null,null,x.d,x.a)),u.jb(6144,null,m.k,null,[d.g]),u.Va(2,49152,null,0,d.g,[],null,null)],null,null)}function pl(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"tr",[["class","example-element-row mat-row"],["mat-row",""],["role","row"]],[[2,"example-expanded-row",null]],[[null,"click"]],function(l,n,e){var u=!0;return"click"===n&&(u=!1!==(l.component.expandedElement=l.context.$implicit)&&u),u},x.e,x.b)),u.jb(6144,null,m.m,null,[d.i]),u.Va(2,49152,null,0,d.i,[],null,null)],null,function(l,n){l(n,0,0,n.component.expandedElement===n.context.$implicit)})}function hl(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,2,"tr",[["class","example-detail-row mat-row"],["mat-row",""],["role","row"]],null,null,null,x.e,x.b)),u.jb(6144,null,m.m,null,[d.i]),u.Va(2,49152,null,0,d.i,[],null,null)],null,null)}function fl(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,6,"mat-card",[["class","center-spinner mat-card"],["fxLayout","row"],["fxLayoutAlign","center center"],["fxLayoutGap","gappx"]],null,null,null,k.d,k.a)),u.Va(1,49152,null,0,V.a,[],null,null),u.Va(2,737280,null,0,s.d,[g.h,u.l,g.l],{layout:[0,"layout"]},null),u.Va(3,1785856,null,0,s.e,[g.h,u.l,[6,s.d],u.D,_.b,g.l],{gap:[0,"gap"]},null),u.Va(4,737280,null,0,s.c,[g.h,u.l,[6,s.d],g.l],{align:[0,"align"]},null),(l()(),u.Wa(5,0,null,0,1,"mat-spinner",[["class","mat-spinner mat-progress-spinner"],["mode","indeterminate"],["role","progressbar"]],[[2,"_mat-animation-noopable",null],[4,"width","px"],[4,"height","px"]],null,null,v.b,v.a)),u.Va(6,49152,null,0,S.d,[u.l,f.a,[2,W.d],[2,w.a],S.a],null,null)],function(l,n){l(n,2,0,"row"),l(n,3,0,"gappx"),l(n,4,0,"center center")},function(l,n){l(n,5,0,u.gb(n,6)._noopAnimations,u.gb(n,6).diameter,u.gb(n,6).diameter)})}function yl(l){return u.ob(0,[u.kb(402653184,1,{paginator:0}),u.kb(402653184,2,{filter_component:0}),(l()(),u.Wa(2,0,null,null,41,"div",[["fxLayout","row"],["fxLayoutAlign","end center"]],null,null,null,null,null)),u.Va(3,737280,null,0,s.d,[g.h,u.l,g.l],{layout:[0,"layout"]},null),u.Va(4,737280,null,0,s.c,[g.h,u.l,[6,s.d],g.l],{align:[0,"align"]},null),(l()(),u.Wa(5,16777216,null,null,5,"button",[["aria-haspopup","true"],["mat-icon-button",""]],[[8,"disabled",0],[2,"_mat-animation-noopable",null],[1,"aria-expanded",0]],[[null,"mousedown"],[null,"keydown"],[null,"click"]],function(l,n,e){var a=!0;return"mousedown"===n&&(a=!1!==u.gb(l,7)._handleMousedown(e)&&a),"keydown"===n&&(a=!1!==u.gb(l,7)._handleKeydown(e)&&a),"click"===n&&(a=!1!==u.gb(l,7)._handleClick(e)&&a),a},p.d,p.b)),u.Va(6,180224,null,0,h.b,[u.l,f.a,y.e,[2,w.a]],null,null),u.Va(7,1196032,null,0,j.f,[C.c,u.l,u.V,j.b,[2,j.c],[8,null],[2,_.b],y.e],{menu:[0,"menu"]},null),(l()(),u.Wa(8,0,null,0,2,"mat-icon",[["class","mat-icon"],["role","img"]],[[2,"mat-icon-inline",null]],null,null,O.b,O.a)),u.Va(9,638976,null,0,P.a,[u.l,P.c,[8,null]],null,null),(l()(),u.mb(-1,0,["dashboard"])),(l()(),u.Wa(11,0,null,null,32,"mat-menu",[],null,null,null,M.d,M.a)),u.Va(12,1294336,[["menu",4]],2,j.c,[u.l,u.D,j.a],null,null),u.kb(603979776,3,{items:1}),u.kb(335544320,4,{lazyContent:0}),u.jb(2048,null,j.h,null,[j.c]),(l()(),u.Wa(16,0,null,0,6,"button",[["class","mat-menu-item"],["mat-menu-item",""],["role","menuitem"]],[[2,"mat-menu-item-highlighted",null],[2,"mat-menu-item-submenu-trigger",null],[1,"tabindex",0],[1,"aria-disabled",0],[1,"disabled",0]],[[null,"click"],[null,"mouseenter"]],function(l,n,e){var a=!0,t=l.component;return"click"===n&&(a=!1!==u.gb(l,17)._checkDisabled(e)&&a),"mouseenter"===n&&(a=!1!==u.gb(l,17)._handleMouseEnter()&&a),"click"===n&&(a=!1!==t.changeLayoutPosition(0)&&a),a},M.c,M.b)),u.Va(17,180224,[[3,4]],0,j.d,[u.l,W.d,y.e,[2,j.h]],null,null),(l()(),u.Wa(18,0,null,0,2,"mat-icon",[["class","mat-icon"],["role","img"]],[[2,"mat-icon-inline",null]],null,null,O.b,O.a)),u.Va(19,638976,null,0,P.a,[u.l,P.c,[8,null]],null,null),(l()(),u.mb(-1,0,["arrow_forward"])),(l()(),u.Wa(21,0,null,0,1,"span",[],null,null,null,null,null)),(l()(),u.mb(22,null,["",""])),(l()(),u.Wa(23,0,null,0,6,"button",[["class","mat-menu-item"],["mat-menu-item",""],["role","menuitem"]],[[2,"mat-menu-item-highlighted",null],[2,"mat-menu-item-submenu-trigger",null],[1,"tabindex",0],[1,"aria-disabled",0],[1,"disabled",0]],[[null,"click"],[null,"mouseenter"]],function(l,n,e){var a=!0,t=l.component;return"click"===n&&(a=!1!==u.gb(l,24)._checkDisabled(e)&&a),"mouseenter"===n&&(a=!1!==u.gb(l,24)._handleMouseEnter()&&a),"click"===n&&(a=!1!==t.changeLayoutPosition(1)&&a),a},M.c,M.b)),u.Va(24,180224,[[3,4]],0,j.d,[u.l,W.d,y.e,[2,j.h]],null,null),(l()(),u.Wa(25,0,null,0,2,"mat-icon",[["class","mat-icon"],["role","img"]],[[2,"mat-icon-inline",null]],null,null,O.b,O.a)),u.Va(26,638976,null,0,P.a,[u.l,P.c,[8,null]],null,null),(l()(),u.mb(-1,0,["arrow_back"])),(l()(),u.Wa(28,0,null,0,1,"span",[],null,null,null,null,null)),(l()(),u.mb(29,null,["",""])),(l()(),u.Wa(30,0,null,0,6,"button",[["class","mat-menu-item"],["mat-menu-item",""],["role","menuitem"]],[[2,"mat-menu-item-highlighted",null],[2,"mat-menu-item-submenu-trigger",null],[1,"tabindex",0],[1,"aria-disabled",0],[1,"disabled",0]],[[null,"click"],[null,"mouseenter"]],function(l,n,e){var a=!0,t=l.component;return"click"===n&&(a=!1!==u.gb(l,31)._checkDisabled(e)&&a),"mouseenter"===n&&(a=!1!==u.gb(l,31)._handleMouseEnter()&&a),"click"===n&&(a=!1!==t.changeLayoutPosition(2)&&a),a},M.c,M.b)),u.Va(31,180224,[[3,4]],0,j.d,[u.l,W.d,y.e,[2,j.h]],null,null),(l()(),u.Wa(32,0,null,0,2,"mat-icon",[["class","mat-icon"],["role","img"]],[[2,"mat-icon-inline",null]],null,null,O.b,O.a)),u.Va(33,638976,null,0,P.a,[u.l,P.c,[8,null]],null,null),(l()(),u.mb(-1,0,["arrow_upward"])),(l()(),u.Wa(35,0,null,0,1,"span",[],null,null,null,null,null)),(l()(),u.mb(36,null,["",""])),(l()(),u.Wa(37,0,null,0,6,"button",[["class","mat-menu-item"],["mat-menu-item",""],["role","menuitem"]],[[2,"mat-menu-item-highlighted",null],[2,"mat-menu-item-submenu-trigger",null],[1,"tabindex",0],[1,"aria-disabled",0],[1,"disabled",0]],[[null,"click"],[null,"mouseenter"]],function(l,n,e){var a=!0,t=l.component;return"click"===n&&(a=!1!==u.gb(l,38)._checkDisabled(e)&&a),"mouseenter"===n&&(a=!1!==u.gb(l,38)._handleMouseEnter()&&a),"click"===n&&(a=!1!==t.changeLayoutPosition(3)&&a),a},M.c,M.b)),u.Va(38,180224,[[3,4]],0,j.d,[u.l,W.d,y.e,[2,j.h]],null,null),(l()(),u.Wa(39,0,null,0,2,"mat-icon",[["class","mat-icon"],["role","img"]],[[2,"mat-icon-inline",null]],null,null,O.b,O.a)),u.Va(40,638976,null,0,P.a,[u.l,P.c,[8,null]],null,null),(l()(),u.mb(-1,0,["arrow_downward"])),(l()(),u.Wa(42,0,null,0,1,"span",[],null,null,null,null,null)),(l()(),u.mb(43,null,["",""])),(l()(),u.Wa(44,0,null,null,87,"div",[["fxLayout.xs","column nowrap"]],null,null,null,null,null)),u.Va(45,737280,null,0,s.d,[g.h,u.l,g.l],{layout:[0,"layout"],layoutXs:[1,"layoutXs"]},null),u.Va(46,737280,null,0,s.c,[g.h,u.l,[6,s.d],g.l],{align:[0,"align"]},null),(l()(),u.Wa(47,0,null,null,5,"toco-catalog-filters-container",[["class","width-90 back-grey mat-elevation-z8"],["fxLayout","row wrap"],["fxLayout.xs","column wrap"],["fxLayoutAlign","start center"],["fxLayoutAlign.xs","center center"],["fxLayoutGap","1em"]],null,null,null,H,z)),u.Va(48,737280,null,0,s.d,[g.h,u.l,g.l],{layout:[0,"layout"],layoutXs:[1,"layoutXs"]},null),u.Va(49,1785856,null,0,s.e,[g.h,u.l,[6,s.d],u.D,_.b,g.l],{gap:[0,"gap"]},null),u.Va(50,737280,null,0,s.c,[g.h,u.l,[6,s.d],g.l],{align:[0,"align"],alignXs:[1,"alignXs"]},null),u.Va(51,737280,null,0,s.a,[g.h,u.l,[3,s.d],g.l,g.f],{flex:[0,"flex"]},null),u.Va(52,114688,[[2,4]],0,T,[u.k,A.a,R.a],null,null),(l()(),u.Wa(53,0,null,null,76,"div",[["class","mat-elevation-z8 width-90 margin1em"]],null,null,null,null,null)),(l()(),u.Wa(54,0,null,null,73,"table",[["class","mat-table"],["mat-table",""],["multiTemplateDataRows",""]],null,null,null,x.f,x.c)),u.Va(55,2342912,null,4,d.k,[u.w,u.i,u.l,[8,null],[2,_.b],W.d,f.a],{dataSource:[0,"dataSource"],multiTemplateDataRows:[1,"multiTemplateDataRows"]},null),u.kb(603979776,5,{_contentColumnDefs:1}),u.kb(603979776,6,{_contentRowDefs:1}),u.kb(603979776,7,{_contentHeaderRowDefs:1}),u.kb(603979776,8,{_contentFooterRowDefs:1}),(l()(),u.Wa(60,0,null,null,11,null,null,null,null,null,null,null)),u.Va(61,16384,null,3,d.c,[],{name:[0,"name"]},null),u.kb(335544320,9,{cell:0}),u.kb(335544320,10,{headerCell:0}),u.kb(335544320,11,{footerCell:0}),u.jb(2048,[[5,4]],m.d,null,[d.c]),(l()(),u.Na(0,null,null,2,null,tl)),u.Va(67,16384,null,0,d.f,[u.S],null,null),u.jb(2048,[[10,4]],m.j,null,[d.f]),(l()(),u.Na(0,null,null,2,null,il)),u.Va(70,16384,null,0,d.b,[u.S],null,null),u.jb(2048,[[9,4]],m.b,null,[d.b]),(l()(),u.Wa(72,0,null,null,11,null,null,null,null,null,null,null)),u.Va(73,16384,null,3,d.c,[],{name:[0,"name"]},null),u.kb(335544320,12,{cell:0}),u.kb(335544320,13,{headerCell:0}),u.kb(335544320,14,{footerCell:0}),u.jb(2048,[[5,4]],m.d,null,[d.c]),(l()(),u.Na(0,null,null,2,null,ol)),u.Va(79,16384,null,0,d.f,[u.S],null,null),u.jb(2048,[[13,4]],m.j,null,[d.f]),(l()(),u.Na(0,null,null,2,null,rl)),u.Va(82,16384,null,0,d.b,[u.S],null,null),u.jb(2048,[[12,4]],m.b,null,[d.b]),(l()(),u.Wa(84,0,null,null,11,null,null,null,null,null,null,null)),u.Va(85,16384,null,3,d.c,[],{name:[0,"name"]},null),u.kb(335544320,15,{cell:0}),u.kb(335544320,16,{headerCell:0}),u.kb(335544320,17,{footerCell:0}),u.jb(2048,[[5,4]],m.d,null,[d.c]),(l()(),u.Na(0,null,null,2,null,cl)),u.Va(91,16384,null,0,d.f,[u.S],null,null),u.jb(2048,[[16,4]],m.j,null,[d.f]),(l()(),u.Na(0,null,null,2,null,bl)),u.Va(94,16384,null,0,d.b,[u.S],null,null),u.jb(2048,[[15,4]],m.b,null,[d.b]),(l()(),u.Wa(96,0,null,null,11,null,null,null,null,null,null,null)),u.Va(97,16384,null,3,d.c,[],{name:[0,"name"]},null),u.kb(335544320,18,{cell:0}),u.kb(335544320,19,{headerCell:0}),u.kb(335544320,20,{footerCell:0}),u.jb(2048,[[5,4]],m.d,null,[d.c]),(l()(),u.Na(0,null,null,2,null,dl)),u.Va(103,16384,null,0,d.f,[u.S],null,null),u.jb(2048,[[19,4]],m.j,null,[d.f]),(l()(),u.Na(0,null,null,2,null,ml)),u.Va(106,16384,null,0,d.b,[u.S],null,null),u.jb(2048,[[18,4]],m.b,null,[d.b]),(l()(),u.Wa(108,0,null,null,8,null,null,null,null,null,null,null)),u.Va(109,16384,null,3,d.c,[],{name:[0,"name"]},null),u.kb(335544320,21,{cell:0}),u.kb(335544320,22,{headerCell:0}),u.kb(335544320,23,{footerCell:0}),u.jb(2048,[[5,4]],m.d,null,[d.c]),(l()(),u.Na(0,null,null,2,null,sl)),u.Va(115,16384,null,0,d.b,[u.S],null,null),u.jb(2048,[[21,4]],m.b,null,[d.b]),(l()(),u.Wa(117,0,null,null,10,"tbody",[],null,null,null,null,null)),(l()(),u.Na(0,null,null,2,null,gl)),u.Va(119,540672,null,0,d.h,[u.S,u.w],{columns:[0,"columns"]},null),u.jb(2048,[[7,4]],m.l,null,[d.h]),(l()(),u.Na(0,null,null,2,null,pl)),u.Va(122,540672,null,0,d.j,[u.S,u.w],{columns:[0,"columns"]},null),u.jb(2048,[[6,4]],m.n,null,[d.j]),(l()(),u.Na(0,null,null,3,null,hl)),u.Va(125,540672,null,0,d.j,[u.S,u.w],{columns:[0,"columns"]},null),u.hb(126,1),u.jb(2048,[[6,4]],m.n,null,[d.j]),(l()(),u.Wa(128,0,null,null,1,"mat-paginator",[["class","mat-paginator"]],null,[[null,"page"]],function(l,n,e){var u=!0;return"page"===n&&(u=!1!==l.component.fetchJournalData()&&u),u},X.b,X.a)),u.Va(129,245760,[[1,4]],0,$.b,[$.c,u.i],{length:[0,"length"],pageSize:[1,"pageSize"],pageSizeOptions:[2,"pageSizeOptions"]},{page:"page"}),(l()(),u.Na(16777216,null,null,1,null,fl)),u.Va(131,16384,null,0,W.k,[u.V,u.S],{ngIf:[0,"ngIf"]},null)],function(l,n){var e=n.component;l(n,3,0,"row"),l(n,4,0,"end center"),l(n,7,0,u.gb(n,12)),l(n,9,0),l(n,12,0),l(n,19,0),l(n,26,0),l(n,33,0),l(n,40,0),l(n,45,0,u.Ya(1,"",e.currentlayout.layout,""),"column nowrap"),l(n,46,0,u.Ya(1,"",e.currentlayout.aling,"")),l(n,48,0,"row wrap","column wrap"),l(n,49,0,"1em"),l(n,50,0,"start center","center center"),l(n,51,0,u.Ya(1,"",e.currentlayout.width,"")),l(n,52,0),l(n,55,0,e.dataSource,""),l(n,61,0,"title"),l(n,73,0,"rnps"),l(n,85,0,"p-issn"),l(n,97,0,"url"),l(n,109,0,"expandedDetail"),l(n,119,0,e.columnsToDisplay),l(n,122,0,e.columnsToDisplay),l(n,125,0,l(n,126,0,"expandedDetail")),l(n,129,0,e.length,e.pageSize,e.pageSizeOptions),l(n,131,0,!e.isEmpty())},function(l,n){var e=n.component;l(n,5,0,u.gb(n,6).disabled||null,"NoopAnimations"===u.gb(n,6)._animationMode,u.gb(n,7).menuOpen||null),l(n,8,0,u.gb(n,9).inline),l(n,16,0,u.gb(n,17)._highlighted,u.gb(n,17)._triggersSubmenu,u.gb(n,17)._getTabIndex(),u.gb(n,17).disabled.toString(),u.gb(n,17).disabled||null),l(n,18,0,u.gb(n,19).inline),l(n,22,0,e.layoutPosition[0].name),l(n,23,0,u.gb(n,24)._highlighted,u.gb(n,24)._triggersSubmenu,u.gb(n,24)._getTabIndex(),u.gb(n,24).disabled.toString(),u.gb(n,24).disabled||null),l(n,25,0,u.gb(n,26).inline),l(n,29,0,e.layoutPosition[1].name),l(n,30,0,u.gb(n,31)._highlighted,u.gb(n,31)._triggersSubmenu,u.gb(n,31)._getTabIndex(),u.gb(n,31).disabled.toString(),u.gb(n,31).disabled||null),l(n,32,0,u.gb(n,33).inline),l(n,36,0,e.layoutPosition[2].name),l(n,37,0,u.gb(n,38)._highlighted,u.gb(n,38)._triggersSubmenu,u.gb(n,38)._getTabIndex(),u.gb(n,38).disabled.toString(),u.gb(n,38).disabled||null),l(n,39,0,u.gb(n,40).inline),l(n,43,0,e.layoutPosition[3].name)})}var wl=u.Sa("toco-journals",ul,function(l){return u.ob(0,[(l()(),u.Wa(0,0,null,null,1,"toco-journals",[],null,null,null,yl,al)),u.Va(1,114688,null,0,ul,[R.a,q.a,nl.a],null,null)],function(l,n){l(n,1,0)},null)},{},{},[]),xl=e("NcP4"),kl=e("t68o"),Vl=e("xYTU"),_l=e("xfFk"),vl=e("E2lU"),Sl=e("okYH"),Wl=e("f9ck"),jl=e("M2Lx"),Cl=e("v9Dh"),Ol=e("Wf4p"),Pl=e("o3x0"),Ml=e("uGex"),Dl=e("ZYjt"),Nl=e("4tE/"),Il=e("gIcY"),Ll=e("t/Na"),Rl={title:"Revistas"},Al=function(){},Tl=e("u7R8"),El=e("4c35"),zl=e("qAlS"),Fl=e("8mMr"),Jl=e("/VYK"),Yl=e("seP3"),Hl=e("b716"),Xl=e("de3e"),$l=e("r43C"),Ul=e("vARd"),ql=e("Z+uX"),Bl=e("Nsh5"),Gl=e("La40"),Kl=e("/dO6"),Zl=e("kWGw"),Ql=e("XmIK"),ln=e("hUWP"),nn=e("3pJQ"),en=e("V9q+"),un=e("c7kW"),an=e("OeE5"),tn=e("YSh2");e.d(n,"CatalogModuleNgFactory",function(){return on});var on=u.Ta(a,[],function(l){return u.db([u.eb(512,u.k,u.Ia,[[8,[t.a,b,wl,xl.a,kl.a,Vl.a,Vl.b,_l.a,vl.a,Sl.a,Wl.a]],[3,u.k],u.B]),u.eb(4608,W.m,W.l,[u.y,[2,W.x]]),u.eb(4608,C.c,C.c,[C.i,C.e,u.k,C.h,C.f,u.u,u.D,W.d,_.b]),u.eb(5120,C.j,C.k,[C.c]),u.eb(5120,j.b,j.g,[C.c]),u.eb(4608,jl.c,jl.c,[]),u.eb(5120,Cl.b,Cl.c,[C.c]),u.eb(4608,Ol.d,Ol.d,[]),u.eb(5120,Pl.b,Pl.c,[C.c]),u.eb(4608,Pl.d,Pl.d,[C.c,u.u,[2,W.g],[2,Pl.a],Pl.b,[3,Pl.d],C.e]),u.eb(5120,Ml.a,Ml.b,[C.c]),u.eb(5120,$.c,$.a,[[3,$.c]]),u.eb(4608,Dl.f,Ol.e,[[2,Ol.i],[2,Ol.n]]),u.eb(5120,Nl.b,Nl.c,[C.c]),u.eb(4608,g.j,g.i,[g.d,g.g]),u.eb(5120,u.b,function(l,n){return[g.m(l,n)]},[W.d,u.F]),u.eb(4608,Il.r,Il.r,[]),u.eb(4608,Il.d,Il.d,[]),u.eb(4608,nl.a,nl.a,[]),u.eb(4608,A.a,A.a,[]),u.eb(4608,R.a,R.a,[Ll.c]),u.eb(1073742336,W.c,W.c,[]),u.eb(1073742336,i.l,i.l,[[2,i.r],[2,i.k]]),u.eb(1073742336,Al,Al,[]),u.eb(1073742336,_.a,_.a,[]),u.eb(1073742336,Ol.n,Ol.n,[[2,Ol.f]]),u.eb(1073742336,f.b,f.b,[]),u.eb(1073742336,Ol.y,Ol.y,[]),u.eb(1073742336,h.c,h.c,[]),u.eb(1073742336,Tl.a,Tl.a,[]),u.eb(1073742336,El.g,El.g,[]),u.eb(1073742336,zl.a,zl.a,[]),u.eb(1073742336,C.g,C.g,[]),u.eb(1073742336,j.e,j.e,[]),u.eb(1073742336,Fl.a,Fl.a,[]),u.eb(1073742336,jl.d,jl.d,[]),u.eb(1073742336,y.a,y.a,[]),u.eb(1073742336,Cl.e,Cl.e,[]),u.eb(1073742336,P.b,P.b,[]),u.eb(1073742336,V.e,V.e,[]),u.eb(1073742336,Jl.c,Jl.c,[]),u.eb(1073742336,Yl.d,Yl.d,[]),u.eb(1073742336,Hl.b,Hl.b,[]),u.eb(1073742336,Xl.a,Xl.a,[]),u.eb(1073742336,Pl.g,Pl.g,[]),u.eb(1073742336,Ol.o,Ol.o,[]),u.eb(1073742336,$l.a,$l.a,[]),u.eb(1073742336,Ul.d,Ul.d,[]),u.eb(1073742336,ql.a,ql.a,[]),u.eb(1073742336,S.c,S.c,[]),u.eb(1073742336,Bl.a,Bl.a,[]),u.eb(1073742336,Gl.a,Gl.a,[]),u.eb(1073742336,Kl.d,Kl.d,[]),u.eb(1073742336,m.p,m.p,[]),u.eb(1073742336,d.m,d.m,[]),u.eb(1073742336,Ol.w,Ol.w,[]),u.eb(1073742336,Ol.t,Ol.t,[]),u.eb(1073742336,Ml.d,Ml.d,[]),u.eb(1073742336,$.d,$.d,[]),u.eb(1073742336,Zl.a,Zl.a,[]),u.eb(1073742336,Nl.e,Nl.e,[]),u.eb(1073742336,Ql.a,Ql.a,[]),u.eb(1073742336,g.e,g.e,[]),u.eb(1073742336,s.b,s.b,[]),u.eb(1073742336,ln.a,ln.a,[]),u.eb(1073742336,nn.a,nn.a,[]),u.eb(1073742336,en.a,en.a,[[2,g.k],u.F]),u.eb(1073742336,Il.q,Il.q,[]),u.eb(1073742336,Il.h,Il.h,[]),u.eb(1073742336,un.a,un.a,[]),u.eb(1073742336,Il.o,Il.o,[]),u.eb(1073742336,an.a,an.a,[]),u.eb(1073742336,a,a,[]),u.eb(1024,i.i,function(){return[[{path:"",component:o,children:[{path:"",component:ul,data:Rl}]}]]},[]),u.eb(256,Kl.a,{separatorKeyCodes:[tn.f]},[])])})}}]);