(window.webpackJsonp=window.webpackJsonp||[]).push([[3],{tePd:function(n,l,u){"use strict";u.r(l);var t=u("CcnG"),e=function(){return function(){}}(),o=u("pMnS"),i=u("ZYCi"),a=function(){function n(){}return n.prototype.ngOnInit=function(){},n}(),r=[[""]],c=t.gb({encapsulation:0,styles:r,data:{}});function s(n){return t.Ab(0,[(n()(),t.ib(0,0,null,null,1,"p",[],null,null,null,null,null)),(n()(),t.yb(-1,null,[" pages works!\n"])),(n()(),t.ib(2,16777216,null,null,1,"router-outlet",[],null,null,null,null,null)),t.hb(3,212992,null,0,i.p,[i.b,t.Ha,t.m,[8,null],t.j],null,null)],function(n,l){n(l,3,0)},null)}var p=t.eb("toco-pages",a,function(n){return t.Ab(0,[(n()(),t.ib(0,0,null,null,1,"toco-pages",[],null,null,null,s,c)),t.hb(1,114688,null,0,a,[],null,null)],function(n,l){n(l,1,0)},null)},{},{},[]),g=u("Ip0R"),b=u("CY5v"),f=function(){function n(n,l){this.route=n,this.metadata=l,this.loading=!0}return n.prototype.ngOnInit=function(){var n=this;this.route.data.subscribe(function(l){n.loading=!1,console.log(l),n.page=l.page,n.ngOnChanges()})},n.prototype.ngOnChanges=function(){console.log(this.page),this.metadata.setTitleMetadataDrupal(this.page)},n}(),h=[[""]],v=t.gb({encapsulation:0,styles:h,data:{}});function d(n){return t.Ab(0,[(n()(),t.ib(0,0,null,null,5,"div",[["class","container"]],null,null,null,null,null)),(n()(),t.ib(1,0,null,null,2,"div",[["class","page-title"]],null,null,null,null,null)),(n()(),t.ib(2,0,null,null,1,"h1",[["class","mat-h1"]],null,null,null,null,null)),(n()(),t.yb(3,null,["",""])),(n()(),t.ib(4,0,null,null,1,"div",[],null,null,null,null,null)),(n()(),t.ib(5,0,null,null,0,"div",[["class","e2e-inner-html-bound  text-align-justify"]],[[8,"innerHTML",1]],null,null,null,null))],null,function(n,l){var u=l.component;n(l,3,0,u.page.title[0].value),n(l,5,0,u.page.body[0].value)})}function m(n){return t.Ab(0,[(n()(),t.Za(16777216,null,null,1,null,d)),t.hb(1,16384,null,0,g.k,[t.Ha,t.Ca],{ngIf:[0,"ngIf"]},null)],function(n,l){n(l,1,0,l.component.page)},null)}var y=t.eb("toco-page-view",f,function(n){return t.Ab(0,[(n()(),t.ib(0,0,null,null,1,"toco-page-view",[],null,null,null,m,v)),t.hb(1,638976,null,0,f,[i.a,b.a],null,null)],function(n,l){n(l,1,0)},null)},{},{},[]),w=u("t/Na"),q=u("AytR"),k=function(){function n(n){this.http=n}return n.prototype.getPageBySlug=function(n){var l={params:(new w.g).set("_format","json")};return this.http.get(q.a.apisEndpoints.pages+"/"+n,l)},n}(),A=u("t9fZ"),C=u("67Y/"),O=function(){function n(n,l){this.service=n,this.router=l}return n.prototype.resolve=function(n,l){var u=this,t=n.paramMap.get("slug");return console.log(t),this.service.getPageBySlug(t).pipe(Object(A.a)(1),Object(C.a)(function(n){if(n)return console.log(n),n;u.router.navigate(["/"])}))},n}(),j=function(){return function(){}}();u.d(l,"PagesModuleNgFactory",function(){return I});var I=t.fb(e,[],function(n){return t.pb([t.qb(512,t.m,t.Ua,[[8,[o.a,p,y]],[3,t.m],t.J]),t.qb(4608,g.m,g.l,[t.F,[2,g.x]]),t.qb(4608,k,k,[w.c]),t.qb(4608,O,O,[k,i.k]),t.qb(1073742336,g.c,g.c,[]),t.qb(1073742336,i.o,i.o,[[2,i.u],[2,i.k]]),t.qb(1073742336,j,j,[]),t.qb(1073742336,e,e,[]),t.qb(1024,i.i,function(){return[[{path:"",component:a,children:[{path:":slug",component:f,resolve:{page:O}}]}]]},[])])})}}]);