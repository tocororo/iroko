(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["main"],{

/***/ "./src/$$_lazy_route_resource lazy recursive":
/*!**********************************************************!*\
  !*** ./src/$$_lazy_route_resource lazy namespace object ***!
  \**********************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var map = {
	"../irokoui/catalog/catalog.module": [
		"./src/irokoui/catalog/catalog.module.ts",
		"irokoui-catalog-catalog-module"
	]
};
function webpackAsyncContext(req) {
	var ids = map[req];
	if(!ids) {
		return Promise.resolve().then(function() {
			var e = new Error("Cannot find module '" + req + "'");
			e.code = 'MODULE_NOT_FOUND';
			throw e;
		});
	}
	return __webpack_require__.e(ids[1]).then(function() {
		var module = __webpack_require__(ids[0]);
		return module;
	});
}
webpackAsyncContext.keys = function webpackAsyncContextKeys() {
	return Object.keys(map);
};
webpackAsyncContext.id = "./src/$$_lazy_route_resource lazy recursive";
module.exports = webpackAsyncContext;

/***/ }),

/***/ "./src/app-catalog/app-catalog-routing.module.ts":
/*!*******************************************************!*\
  !*** ./src/app-catalog/app-catalog-routing.module.ts ***!
  \*******************************************************/
/*! exports provided: AppRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppRoutingModule", function() { return AppRoutingModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};


var appCatalogRoutes = [
    {
        path: '',
        loadChildren: '../irokoui/catalog/catalog.module#CatalogModule'
    }
];
var AppRoutingModule = /** @class */ (function () {
    function AppRoutingModule() {
    }
    AppRoutingModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forRoot(appCatalogRoutes)
            ],
            exports: [
                _angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]
            ],
            providers: []
        })
    ], AppRoutingModule);
    return AppRoutingModule;
}());



/***/ }),

/***/ "./src/app-catalog/app-catalog.component.html":
/*!****************************************************!*\
  !*** ./src/app-catalog/app-catalog.component.html ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<router-outlet *ngIf=\"isOnline;else isOffline\"></router-outlet>\n<ng-template #isOffline>\n    <div>\n        <p class=\"offline-error\">is offline</p>\n    </div>\n</ng-template>\n"

/***/ }),

/***/ "./src/app-catalog/app-catalog.component.ts":
/*!**************************************************!*\
  !*** ./src/app-catalog/app-catalog.component.ts ***!
  \**************************************************/
/*! exports provided: AppCatalogComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppCatalogComponent", function() { return AppCatalogComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var AppCatalogComponent = /** @class */ (function () {
    function AppCatalogComponent() {
        this.isOnline = true; //navigator.onLine;
    }
    AppCatalogComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-root',
            template: __webpack_require__(/*! ./app-catalog.component.html */ "./src/app-catalog/app-catalog.component.html"),
            styles: [__webpack_require__(/*! ../irokoui/app.component.scss */ "./src/irokoui/app.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], AppCatalogComponent);
    return AppCatalogComponent;
}());



/***/ }),

/***/ "./src/app-catalog/app-catalog.module.ts":
/*!***********************************************!*\
  !*** ./src/app-catalog/app-catalog.module.ts ***!
  \***********************************************/
/*! exports provided: AppModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppModule", function() { return AppModule; });
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm5/platform-browser.js");
/* harmony import */ var _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser/animations */ "./node_modules/@angular/platform-browser/fesm5/animations.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _app_catalog_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app-catalog-routing.module */ "./src/app-catalog/app-catalog-routing.module.ts");
/* harmony import */ var _app_catalog_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./app-catalog.component */ "./src/app-catalog/app-catalog.component.ts");
/* harmony import */ var _irokoui_core_core_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../irokoui/core/core.module */ "./src/irokoui/core/core.module.ts");
/* harmony import */ var _irokoui_shared_shared_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../irokoui/shared/shared.module */ "./src/irokoui/shared/shared.module.ts");
/* harmony import */ var _irokoui_catalog_catalog_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../irokoui/catalog/catalog.service */ "./src/irokoui/catalog/catalog.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};









var AppModule = /** @class */ (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
            declarations: [
                _app_catalog_component__WEBPACK_IMPORTED_MODULE_4__["AppCatalogComponent"],
            ],
            imports: [
                _angular_platform_browser__WEBPACK_IMPORTED_MODULE_0__["BrowserModule"],
                _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_1__["BrowserAnimationsModule"],
                _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpClientModule"],
                _irokoui_shared_shared_module__WEBPACK_IMPORTED_MODULE_6__["SharedModule"],
                _irokoui_core_core_module__WEBPACK_IMPORTED_MODULE_5__["CoreModule"],
                _app_catalog_routing_module__WEBPACK_IMPORTED_MODULE_3__["AppRoutingModule"]
            ],
            providers: [_irokoui_catalog_catalog_service__WEBPACK_IMPORTED_MODULE_7__["CatalogService"]],
            bootstrap: [_app_catalog_component__WEBPACK_IMPORTED_MODULE_4__["AppCatalogComponent"]]
        })
    ], AppModule);
    return AppModule;
}());



/***/ }),

/***/ "./src/environments/environment.ts":
/*!*****************************************!*\
  !*** ./src/environments/environment.ts ***!
  \*****************************************/
/*! exports provided: environment */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "environment", function() { return environment; });
// This file can be replaced during build by using the `fileReplacements` array.
// `ng build ---prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.
var environment = {
    production: false,
    appName: "Publicaciones Cientificas Cubanas",
    appHost: "http://tocororo.upr.edu.cu",
    irokoHost: "https://200.14.49.24/",
    apisEndpoints: {
        irokoCatalog: "https://200.14.49.24/api",
        pages: "http://10.2.24.246/pages"
    }
};
/*
 * In development mode, for easier debugging, you can ignore zone related error
 * stack frames such as `zone.run`/`zoneDelegate.invokeTask` by importing the
 * below file. Don't forget to comment it out in production mode
 * because it will have a performance impact when errors are thrown
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.


/***/ }),

/***/ "./src/irokoui/app.component.scss":
/*!****************************************!*\
  !*** ./src/irokoui/app.component.scss ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/irokoui/catalog/catalog.service.ts":
/*!************************************************!*\
  !*** ./src/irokoui/catalog/catalog.service.ts ***!
  \************************************************/
/*! exports provided: CatalogService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CatalogService", function() { return CatalogService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../environments/environment */ "./src/environments/environment.ts");
/* harmony import */ var _entities_http_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../entities/http.service */ "./src/irokoui/entities/http.service.ts");
var __extends = (undefined && undefined.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



'..//environments/environment';

var CatalogService = /** @class */ (function (_super) {
    __extends(CatalogService, _super);
    function CatalogService() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CatalogService.prototype.getJournalsPage = function (count, page, parameters) {
        try {
            var params = new _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpParams"]();
            if (parameters)
                for (var i = 0; i < parameters.length; i++) {
                    params = params.set(parameters[i].field, parameters[i].value);
                }
            var options = {
                params: params.set('count', count.toString()).set('page', (page).toString())
            };
            return this.http.get(_environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].apisEndpoints.irokoCatalog + '/sources', options);
        }
        catch (error) {
        }
    };
    CatalogService.prototype.getJournalsCount = function () {
        try {
            return this.http.get(_environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].apisEndpoints.irokoCatalog + '/sources/count');
        }
        catch (error) {
        }
    };
    CatalogService.prototype.getJournalsVocab = function () {
        try {
            return this.http.get(_environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].apisEndpoints.irokoCatalog + '/vocabularies');
        }
        catch (error) {
        }
    };
    CatalogService.prototype.getTerminosByVocab = function (vocabId) {
        try {
            return this.http.get(_environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].apisEndpoints.irokoCatalog + '/terms/' + vocabId);
            //return  this.http.get<any>(environment.apisEndpoints.irokoCatalog+'/terminos?search=id_vocabulario:'+vocabId+'&filter=id;value');
        }
        catch (error) {
        }
    };
    CatalogService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])()
    ], CatalogService);
    return CatalogService;
}(_entities_http_service__WEBPACK_IMPORTED_MODULE_3__["HttpService"]));



/***/ }),

/***/ "./src/irokoui/core/core-routing.module.ts":
/*!*************************************************!*\
  !*** ./src/irokoui/core/core-routing.module.ts ***!
  \*************************************************/
/*! exports provided: CoreRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CoreRoutingModule", function() { return CoreRoutingModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _home_home_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./home/home.component */ "./src/irokoui/core/home/home.component.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};



var routes = [{
        path: 'home',
        component: _home_home_component__WEBPACK_IMPORTED_MODULE_2__["HomeComponent"],
        data: {
            title: 'Inicio'
        }
    }
];
var CoreRoutingModule = /** @class */ (function () {
    function CoreRoutingModule() {
    }
    CoreRoutingModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]]
        })
    ], CoreRoutingModule);
    return CoreRoutingModule;
}());



/***/ }),

/***/ "./src/irokoui/core/core.module.ts":
/*!*****************************************!*\
  !*** ./src/irokoui/core/core.module.ts ***!
  \*****************************************/
/*! exports provided: CoreModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CoreModule", function() { return CoreModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _module_import_guard__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./module-import-guard */ "./src/irokoui/core/module-import-guard.ts");
/* harmony import */ var _nav_nav_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./nav/nav.component */ "./src/irokoui/core/nav/nav.component.ts");
/* harmony import */ var _footer_footer_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./footer/footer.component */ "./src/irokoui/core/footer/footer.component.ts");
/* harmony import */ var _error404_error404_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./error404/error404.component */ "./src/irokoui/core/error404/error404.component.ts");
/* harmony import */ var _home_home_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./home/home.component */ "./src/irokoui/core/home/home.component.ts");
/* harmony import */ var _core_routing_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./core-routing.module */ "./src/irokoui/core/core-routing.module.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../shared/shared.module */ "./src/irokoui/shared/shared.module.ts");
/* harmony import */ var _metadata_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./metadata.service */ "./src/irokoui/core/metadata.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (undefined && undefined.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};










var CoreModule = /** @class */ (function () {
    function CoreModule(parentModule) {
        Object(_module_import_guard__WEBPACK_IMPORTED_MODULE_2__["throwIfAlreadyLoaded"])(parentModule, 'CoreModule');
    }
    CoreModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
                _core_routing_module__WEBPACK_IMPORTED_MODULE_7__["CoreRoutingModule"],
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_8__["SharedModule"]
            ],
            exports: [
                _nav_nav_component__WEBPACK_IMPORTED_MODULE_3__["NavComponent"],
                _footer_footer_component__WEBPACK_IMPORTED_MODULE_4__["FooterComponent"]
            ],
            declarations: [
                _nav_nav_component__WEBPACK_IMPORTED_MODULE_3__["NavComponent"],
                _footer_footer_component__WEBPACK_IMPORTED_MODULE_4__["FooterComponent"],
                _error404_error404_component__WEBPACK_IMPORTED_MODULE_5__["Error404Component"],
                _home_home_component__WEBPACK_IMPORTED_MODULE_6__["HomeComponent"]
            ],
            providers: [
                _metadata_service__WEBPACK_IMPORTED_MODULE_9__["MetadataService"]
            ]
        }),
        __param(0, Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Optional"])()), __param(0, Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["SkipSelf"])()),
        __metadata("design:paramtypes", [CoreModule])
    ], CoreModule);
    return CoreModule;
}());



/***/ }),

/***/ "./src/irokoui/core/error404/error404.component.html":
/*!***********************************************************!*\
  !*** ./src/irokoui/core/error404/error404.component.html ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<p>\n  error404 works!\n</p>\n"

/***/ }),

/***/ "./src/irokoui/core/error404/error404.component.scss":
/*!***********************************************************!*\
  !*** ./src/irokoui/core/error404/error404.component.scss ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/irokoui/core/error404/error404.component.ts":
/*!*********************************************************!*\
  !*** ./src/irokoui/core/error404/error404.component.ts ***!
  \*********************************************************/
/*! exports provided: Error404Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Error404Component", function() { return Error404Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Error404Component = /** @class */ (function () {
    function Error404Component() {
    }
    Error404Component.prototype.ngOnInit = function () {
    };
    Error404Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-error404',
            template: __webpack_require__(/*! ./error404.component.html */ "./src/irokoui/core/error404/error404.component.html"),
            styles: [__webpack_require__(/*! ./error404.component.scss */ "./src/irokoui/core/error404/error404.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], Error404Component);
    return Error404Component;
}());



/***/ }),

/***/ "./src/irokoui/core/footer/footer.component.html":
/*!*******************************************************!*\
  !*** ./src/irokoui/core/footer/footer.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<p>\n  footer works!\n</p>\n"

/***/ }),

/***/ "./src/irokoui/core/footer/footer.component.scss":
/*!*******************************************************!*\
  !*** ./src/irokoui/core/footer/footer.component.scss ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/irokoui/core/footer/footer.component.ts":
/*!*****************************************************!*\
  !*** ./src/irokoui/core/footer/footer.component.ts ***!
  \*****************************************************/
/*! exports provided: FooterComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FooterComponent", function() { return FooterComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var FooterComponent = /** @class */ (function () {
    function FooterComponent() {
    }
    FooterComponent.prototype.ngOnInit = function () {
    };
    FooterComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-footer',
            template: __webpack_require__(/*! ./footer.component.html */ "./src/irokoui/core/footer/footer.component.html"),
            styles: [__webpack_require__(/*! ./footer.component.scss */ "./src/irokoui/core/footer/footer.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], FooterComponent);
    return FooterComponent;
}());



/***/ }),

/***/ "./src/irokoui/core/home/home.component.html":
/*!***************************************************!*\
  !*** ./src/irokoui/core/home/home.component.html ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<p>\n  home works!\n</p>\n"

/***/ }),

/***/ "./src/irokoui/core/home/home.component.scss":
/*!***************************************************!*\
  !*** ./src/irokoui/core/home/home.component.scss ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/irokoui/core/home/home.component.ts":
/*!*************************************************!*\
  !*** ./src/irokoui/core/home/home.component.ts ***!
  \*************************************************/
/*! exports provided: HomeComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HomeComponent", function() { return HomeComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _metadata_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../metadata.service */ "./src/irokoui/core/metadata.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var HomeComponent = /** @class */ (function () {
    function HomeComponent(metadata) {
        this.metadata = metadata;
    }
    HomeComponent.prototype.ngOnInit = function () {
        this.metadata.setTitleDescription("Inicio", "");
    };
    HomeComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-home',
            template: __webpack_require__(/*! ./home.component.html */ "./src/irokoui/core/home/home.component.html"),
            styles: [__webpack_require__(/*! ./home.component.scss */ "./src/irokoui/core/home/home.component.scss")]
        }),
        __metadata("design:paramtypes", [_metadata_service__WEBPACK_IMPORTED_MODULE_1__["MetadataService"]])
    ], HomeComponent);
    return HomeComponent;
}());



/***/ }),

/***/ "./src/irokoui/core/metadata.service.ts":
/*!**********************************************!*\
  !*** ./src/irokoui/core/metadata.service.ts ***!
  \**********************************************/
/*! exports provided: MetadataService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MetadataService", function() { return MetadataService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm5/platform-browser.js");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../environments/environment */ "./src/environments/environment.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




var MetadataService = /** @class */ (function () {
    function MetadataService(bodyTitle, meta, router) {
        this.bodyTitle = bodyTitle;
        this.meta = meta;
        this.router = router;
    }
    /**
     * TODO: en general esto hay que investigarlo ver la mejor variante
     * para poner los metadatos
     *  que metadatos poner...para que despues funcione twiter, facebook, etc..
     */
    MetadataService.prototype.setTitleDescription = function (title, description) {
        var url = _environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].appHost + this.router.url;
        var t = title + ' | ' + _environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].appName;
        this.bodyTitle.setTitle(t);
        this.meta.updateTag({ name: 'description', content: description });
        // <!-- Schema.org markup for Google+ --});
        // this.meta.updateTag({ itemprop:"name", title});
        // this.meta.updateTag({ itemprop:"description", content: description});
        this.meta.updateTag({ name: "twitter:site", content: _environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].appName });
        this.meta.updateTag({ name: "twitter:title", content: title });
        this.meta.updateTag({ name: "twitter:description", content: description });
        this.meta.updateTag({ name: "twitter:card", content: "some image..." });
        this.meta.updateTag({ name: "twitter:image:src", content: "some image.." });
        //<!-- Open Graph data --});
        this.meta.updateTag({ property: "og:title", content: title });
        this.meta.updateTag({ property: "og:type", content: "article" });
        this.meta.updateTag({ property: "og:url", content: url });
        this.meta.updateTag({ property: "og:description", content: description });
        this.meta.updateTag({ property: "og:site_name", content: _environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].appName });
    };
    MetadataService.prototype.setTitleMetadataDrupal = function (node) {
        if (node) {
            var url = _environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].appHost + this.router.url;
            var title = node.title[0].value + ' - ' + _environments_environment__WEBPACK_IMPORTED_MODULE_2__["environment"].appName;
            this.setTitleDescription(title, node.body[0].summary);
            /*
            this.bodyTitle.setTitle(title);
            this.meta.updateTag({ name: 'description', content: node.body[0].summary });
            
            if(node.field_main_image[0])
              //this.meta.updateTag({ name:"twitter:card", content:this.imageLinks(node.field_main_image[0], "medium")});
            this.meta.updateTag({ name:"twitter:site", content: env.appName});
            this.meta.updateTag({ name:"twitter:title", content: node.title[0].value});
            this.meta.updateTag({ name:"twitter:description", content:node.metatag.value.description});
            // this.meta.updateTag({ name:"twitter:creator", content:"@author_handle"});
            //<!-- Twitter summary card with large image must be at least 280x150px --});
            if(node.field_main_image[0])
              //this.meta.updateTag({ name:"twitter:image:src", content:this.imageLinks(node.field_main_image[0], "extra_large")});
      
            //<!-- Open Graph data --});
            this.meta.updateTag({ property:"og:title", content:node.title[0].value });
            this.meta.updateTag({ property:"og:type", content:"article" });
            this.meta.updateTag({ property:"og:url", content:url });
            if(node.field_main_image[0])
              //this.meta.updateTag({ property:"og:image", content:this.imageLinks(node.field_main_image[0], "extra_large")});
            this.meta.updateTag({ property:"og:description", content:node.metatag.value.description });
            this.meta.updateTag({ property:"og:site_name", content: env.appName });
            /* this.meta.updateTag({ property:"article:published_time", content:"2013-09-17T05:59:00+01:00" });
            this.meta.updateTag({ property:"article:modified_time", content:"2013-09-16T19:08:47+01:00" });
            this.meta.updateTag({ property:"article:section", content:"Article Section" });
            this.meta.updateTag({ property:"article:tag", content:"Article Tag" });
            this.meta.updateTag({ property:"fb:admins", content:"Facebook numberic ID" }); */
        }
    };
    MetadataService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__["Title"], _angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__["Meta"], _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"]])
    ], MetadataService);
    return MetadataService;
}());



/***/ }),

/***/ "./src/irokoui/core/module-import-guard.ts":
/*!*************************************************!*\
  !*** ./src/irokoui/core/module-import-guard.ts ***!
  \*************************************************/
/*! exports provided: throwIfAlreadyLoaded */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "throwIfAlreadyLoaded", function() { return throwIfAlreadyLoaded; });
function throwIfAlreadyLoaded(parentModule, moduleName) {
    if (parentModule) {
        throw new Error(moduleName + " has already been loaded. Import Core modules in the AppModule only.");
    }
}


/***/ }),

/***/ "./src/irokoui/core/nav/nav.component.html":
/*!*************************************************!*\
  !*** ./src/irokoui/core/nav/nav.component.html ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<header>\n\n  <nav>\n      \n    <div class=\"nav-heder shadows-for-head always-on-top nav-menu-items w-100\" fxLayout=\"row\" fxLayout.xs=\"column\" fxLayoutAlign=\"space-around\">\n\n      <!-- <div class=\"nav-menu-items\" > -->\n        <button mat-flat-button color=\"primary\" *ngFor=\"let item of menuItems\" [routerLink]=\"[item.link]\" routerLinkActive=\"active\">\n          {{item.label}}\n        </button>\n        \n      <!-- </div> -->\n\n\n      <!-- <div class=\"nav-tools\">\n          <div class=\"input-style-for-search\">\n             <mat-icon style=\"margin-left: -45px;z-index: 1;\">pageview</mat-icon> \n          </div>\n          <input type=\"search\" coloaria-label=\"Buscar\" placeholder=\"Buscar\" class=\"input-style\">\n\n        <span class=\"spacer\"></span>\n        <div>\n          <button mat-icon-button [matMenuTriggerFor]=\"menu\" matTooltip=\"Edel Abreu Hernández\" matTooltipPosition=\"left\">\n            <mat-icon matPrefix>person_pin</mat-icon>\n            pin\n          </button>\n          <mat-menu #menu=\"matMenu\">\n            <button mat-menu-item routerLink=\"/people/show\">\n              <mat-icon>person</mat-icon>\n              <span>Mi Perfil</span>\n            </button>\n            <button mat-menu-item>\n              <mat-icon>lock_open</mat-icon>\n              <span>Salir</span>\n            </button>\n          </mat-menu>\n        </div>\n\n      </div> -->\n\n    </div>\n  </nav>\n</header>"

/***/ }),

/***/ "./src/irokoui/core/nav/nav.component.scss":
/*!*************************************************!*\
  !*** ./src/irokoui/core/nav/nav.component.scss ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".menu-items {\n  display: flex;\n  /*float: left;*/\n  display: -webkit-box;\n  list-style: none;\n  flex-direction: row;\n  justify-content: flex-start; }\n"

/***/ }),

/***/ "./src/irokoui/core/nav/nav.component.ts":
/*!***********************************************!*\
  !*** ./src/irokoui/core/nav/nav.component.ts ***!
  \***********************************************/
/*! exports provided: NavComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NavComponent", function() { return NavComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var NavComponent = /** @class */ (function () {
    function NavComponent() {
    }
    NavComponent.prototype.ngOnInit = function () {
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", Array)
    ], NavComponent.prototype, "menuItems", void 0);
    NavComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-nav',
            template: __webpack_require__(/*! ./nav.component.html */ "./src/irokoui/core/nav/nav.component.html"),
            styles: [__webpack_require__(/*! ./nav.component.scss */ "./src/irokoui/core/nav/nav.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], NavComponent);
    return NavComponent;
}());



/***/ }),

/***/ "./src/irokoui/entities/entity.ts":
/*!****************************************!*\
  !*** ./src/irokoui/entities/entity.ts ***!
  \****************************************/
/*! exports provided: Entity */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Entity", function() { return Entity; });
/**
 * Created by Edel on 02/04/2018.
 */
var Entity = /** @class */ (function () {
    function Entity() {
    }
    return Entity;
}());



/***/ }),

/***/ "./src/irokoui/entities/http.service.ts":
/*!**********************************************!*\
  !*** ./src/irokoui/entities/http.service.ts ***!
  \**********************************************/
/*! exports provided: HttpService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HttpService", function() { return HttpService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var HttpService = /** @class */ (function () {
    function HttpService(http) {
        this.http = http;
    }
    HttpService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])(),
        __metadata("design:paramtypes", [_angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"]])
    ], HttpService);
    return HttpService;
}());



/***/ }),

/***/ "./src/irokoui/shared/body/body.component.html":
/*!*****************************************************!*\
  !*** ./src/irokoui/shared/body/body.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div class=\"container mat-body\">\n  <div class=\"e2e-inner-html-bound  text-align-justify\" [innerHTML]=\"body\"> </div>\n</div>\n"

/***/ }),

/***/ "./src/irokoui/shared/body/body.component.scss":
/*!*****************************************************!*\
  !*** ./src/irokoui/shared/body/body.component.scss ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/irokoui/shared/body/body.component.ts":
/*!***************************************************!*\
  !*** ./src/irokoui/shared/body/body.component.ts ***!
  \***************************************************/
/*! exports provided: BodyComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BodyComponent", function() { return BodyComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var BodyComponent = /** @class */ (function () {
    function BodyComponent() {
    }
    BodyComponent.prototype.ngOnChanges = function () {
        this.doReplace();
    };
    BodyComponent.prototype.ngOnInit = function () {
        if (this.body) {
            this.doReplace();
        }
    };
    BodyComponent.prototype.doReplace = function () {
        var find = "/public/inline-images/";
        var replace = "/public/inline-images/";
        var str = this.body.replace(find, replace);
        this.processed = str;
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", String)
    ], BodyComponent.prototype, "body", void 0);
    BodyComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-body',
            template: __webpack_require__(/*! ./body.component.html */ "./src/irokoui/shared/body/body.component.html"),
            styles: [__webpack_require__(/*! ./body.component.scss */ "./src/irokoui/shared/body/body.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], BodyComponent);
    return BodyComponent;
}());



/***/ }),

/***/ "./src/irokoui/shared/info-card/info-card.component.html":
/*!***************************************************************!*\
  !*** ./src/irokoui/shared/info-card/info-card.component.html ***!
  \***************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<mat-card>\n  <img mat-card-image src={{img_card}} *ngIf=\"is_img_card\">\n  <mat-card-header>\n\n      <img mat-card-avatar src={{avatar_card}} *ngIf=\"is_avatar_card\" >\n\n\n      <mat-card-title *ngIf=\"is_title_card\">\n        <strong>\n          {{title_card}}\n        </strong>\n      </mat-card-title>\n\n    <mat-card-subtitle *ngIf=\"is_subtitle_card\">\n      {{subtitle_card}}\n    </mat-card-subtitle>\n  </mat-card-header>\n\n\n\n  <mat-card-content *ngIf=\"is_content_card\">\n     <div class=\"e2e-inner-html-bound  text-align-justify\" [innerHTML]=\"content_card\"></div>\n    \n  </mat-card-content>\n\n  <mat-card-actions *ngIf=\"is_actions_card\">\n    <a mat-button color=\"primary\"   routerLink=\"{{router}}/{{entity.id}}\">VER MÁS</a>\n    <!--(click)=\"show_people()\"-->\n  </mat-card-actions>\n\n</mat-card>"

/***/ }),

/***/ "./src/irokoui/shared/info-card/info-card.component.scss":
/*!***************************************************************!*\
  !*** ./src/irokoui/shared/info-card/info-card.component.scss ***!
  \***************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/irokoui/shared/info-card/info-card.component.ts":
/*!*************************************************************!*\
  !*** ./src/irokoui/shared/info-card/info-card.component.ts ***!
  \*************************************************************/
/*! exports provided: InfoCardComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InfoCardComponent", function() { return InfoCardComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _entities_entity__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../entities/entity */ "./src/irokoui/entities/entity.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var InfoCardComponent = /** @class */ (function () {
    function InfoCardComponent() {
        this.is_avatar_card = false;
        this.is_title_card = false;
        this.is_subtitle_card = false;
        this.is_content_card = false;
        this.is_img_card = false;
        this.is_actions_card = false;
    }
    InfoCardComponent.prototype.ngOnInit = function () {
        if (typeof (this.avatar_card) != 'undefined')
            this.is_avatar_card = true;
        if (this.content_card != ' ')
            this.is_content_card = true;
        if (this.title_card != ' ')
            this.is_title_card = true;
        if (this.subtitle_card != ' ')
            this.is_subtitle_card = true;
        if (typeof (this.img_card) != 'undefined')
            this.is_img_card = true;
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", Object)
    ], InfoCardComponent.prototype, "avatar_card", void 0);
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", String)
    ], InfoCardComponent.prototype, "title_card", void 0);
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", String)
    ], InfoCardComponent.prototype, "subtitle_card", void 0);
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", String)
    ], InfoCardComponent.prototype, "content_card", void 0);
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", String)
    ], InfoCardComponent.prototype, "img_card", void 0);
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", String)
    ], InfoCardComponent.prototype, "router", void 0);
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", _entities_entity__WEBPACK_IMPORTED_MODULE_1__["Entity"])
    ], InfoCardComponent.prototype, "entity", void 0);
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", Boolean)
    ], InfoCardComponent.prototype, "is_actions_card", void 0);
    InfoCardComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-info-card',
            template: __webpack_require__(/*! ./info-card.component.html */ "./src/irokoui/shared/info-card/info-card.component.html"),
            styles: [__webpack_require__(/*! ./info-card.component.scss */ "./src/irokoui/shared/info-card/info-card.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], InfoCardComponent);
    return InfoCardComponent;
}());



/***/ }),

/***/ "./src/irokoui/shared/journal-card/journal-card.component.html":
/*!*********************************************************************!*\
  !*** ./src/irokoui/shared/journal-card/journal-card.component.html ***!
  \*********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<p>\n  journal-card works!\n</p>\n"

/***/ }),

/***/ "./src/irokoui/shared/journal-card/journal-card.component.scss":
/*!*********************************************************************!*\
  !*** ./src/irokoui/shared/journal-card/journal-card.component.scss ***!
  \*********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/irokoui/shared/journal-card/journal-card.component.ts":
/*!*******************************************************************!*\
  !*** ./src/irokoui/shared/journal-card/journal-card.component.ts ***!
  \*******************************************************************/
/*! exports provided: JournalCardComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "JournalCardComponent", function() { return JournalCardComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var JournalCardComponent = /** @class */ (function () {
    function JournalCardComponent() {
    }
    JournalCardComponent.prototype.ngOnInit = function () {
    };
    JournalCardComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-journal-card',
            template: __webpack_require__(/*! ./journal-card.component.html */ "./src/irokoui/shared/journal-card/journal-card.component.html"),
            styles: [__webpack_require__(/*! ./journal-card.component.scss */ "./src/irokoui/shared/journal-card/journal-card.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], JournalCardComponent);
    return JournalCardComponent;
}());



/***/ }),

/***/ "./src/irokoui/shared/material.module.ts":
/*!***********************************************!*\
  !*** ./src/irokoui/shared/material.module.ts ***!
  \***********************************************/
/*! exports provided: MaterialModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MaterialModule", function() { return MaterialModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/material */ "./node_modules/@angular/material/esm5/material.es5.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};


var MaterialModule = /** @class */ (function () {
    function MaterialModule() {
    }
    MaterialModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatButtonModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatButtonToggleModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatMenuModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatToolbarModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatTooltipModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatIconModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatCardModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatInputModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatCheckboxModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatFormFieldModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatDialogModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatGridListModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatSnackBarModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatProgressBarModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatProgressSpinnerModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatSidenavModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatTabsModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatChipsModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatTableModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatPaginatorModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatSlideToggleModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatSelectModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatOptionModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatAutocompleteModule"]
            ],
            exports: [
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatButtonModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatButtonToggleModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatMenuModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatToolbarModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatTooltipModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatIconModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatCardModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatInputModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatCheckboxModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatFormFieldModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatDialogModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatGridListModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatSnackBarModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatProgressSpinnerModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatProgressBarModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatSidenavModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatTabsModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatChipsModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatTableModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatPaginatorModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatSlideToggleModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatSelectModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatOptionModule"],
                _angular_material__WEBPACK_IMPORTED_MODULE_1__["MatAutocompleteModule"]
            ]
        })
    ], MaterialModule);
    return MaterialModule;
}());



/***/ }),

/***/ "./src/irokoui/shared/page-header/page-header.component.html":
/*!*******************************************************************!*\
  !*** ./src/irokoui/shared/page-header/page-header.component.html ***!
  \*******************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<mat-toolbar color=\"primary\">\n\n  <mat-toolbar-row *ngFor=\"let item of info; index as i\" >\n    <!--\n      la condicion especifica q-> si quiero mostrar el icono y es la primera iteracion entonces se muestra\n      esto evita que se repita el icono por cada row del componente\n    -->\n    <div *ngIf=\"is_show_icon && i ==0; then block\"></div>\n    <!--\n      en la sintaxis del \"if\" donde dice \"then block\" quiere decir q cuando se pumpla la condicion ira a ese blocque\n       q esta en otra etiqueta y q se tiene q llamar \"<ng-template #block >\"\n    -->\n    <ng-template #block >\n      <mat-icon class=\"icon-position change-cursor\" (click)=\"function()\">menu</mat-icon>\n    </ng-template>\n\n    <h1><strong>{{item}}</strong></h1>\n\n  </mat-toolbar-row>\n\n\n\n</mat-toolbar>"

/***/ }),

/***/ "./src/irokoui/shared/page-header/page-header.component.scss":
/*!*******************************************************************!*\
  !*** ./src/irokoui/shared/page-header/page-header.component.scss ***!
  \*******************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/irokoui/shared/page-header/page-header.component.ts":
/*!*****************************************************************!*\
  !*** ./src/irokoui/shared/page-header/page-header.component.ts ***!
  \*****************************************************************/
/*! exports provided: PageHeaderComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PageHeaderComponent", function() { return PageHeaderComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var PageHeaderComponent = /** @class */ (function () {
    function PageHeaderComponent() {
        this.info = [];
        this.is_show_icon = false;
    }
    PageHeaderComponent.prototype.ngOnInit = function () {
        //this.info = ['Listado de Personas','estas estan en el sitio','esta es otra fila'];
    };
    PageHeaderComponent.prototype.function = function () {
        this.drawer.toggle();
    };
    PageHeaderComponent.prototype.change_icon_show = function () {
        this.is_show_icon = false;
        console.log(this.is_show_icon);
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", Object)
    ], PageHeaderComponent.prototype, "drawer", void 0);
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", Array)
    ], PageHeaderComponent.prototype, "info", void 0);
    PageHeaderComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-page-header',
            template: __webpack_require__(/*! ./page-header.component.html */ "./src/irokoui/shared/page-header/page-header.component.html"),
            styles: [__webpack_require__(/*! ./page-header.component.scss */ "./src/irokoui/shared/page-header/page-header.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], PageHeaderComponent);
    return PageHeaderComponent;
}());



/***/ }),

/***/ "./src/irokoui/shared/shared.module.ts":
/*!*********************************************!*\
  !*** ./src/irokoui/shared/shared.module.ts ***!
  \*********************************************/
/*! exports provided: SharedModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SharedModule", function() { return SharedModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _material_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./material.module */ "./src/irokoui/shared/material.module.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var _page_header_page_header_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./page-header/page-header.component */ "./src/irokoui/shared/page-header/page-header.component.ts");
/* harmony import */ var _info_card_info_card_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./info-card/info-card.component */ "./src/irokoui/shared/info-card/info-card.component.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _journal_card_journal_card_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./journal-card/journal-card.component */ "./src/irokoui/shared/journal-card/journal-card.component.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _body_body_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./body/body.component */ "./src/irokoui/shared/body/body.component.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};










var SharedModule = /** @class */ (function () {
    function SharedModule() {
    }
    SharedModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
                _material_module__WEBPACK_IMPORTED_MODULE_2__["MaterialModule"],
                _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_6__["RouterModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_8__["FormsModule"]
            ],
            exports: [
                _material_module__WEBPACK_IMPORTED_MODULE_2__["MaterialModule"],
                _angular_flex_layout__WEBPACK_IMPORTED_MODULE_3__["FlexLayoutModule"],
                _page_header_page_header_component__WEBPACK_IMPORTED_MODULE_4__["PageHeaderComponent"],
                _info_card_info_card_component__WEBPACK_IMPORTED_MODULE_5__["InfoCardComponent"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_8__["FormsModule"],
                _body_body_component__WEBPACK_IMPORTED_MODULE_9__["BodyComponent"]
            ],
            declarations: [
                _page_header_page_header_component__WEBPACK_IMPORTED_MODULE_4__["PageHeaderComponent"],
                _info_card_info_card_component__WEBPACK_IMPORTED_MODULE_5__["InfoCardComponent"],
                _journal_card_journal_card_component__WEBPACK_IMPORTED_MODULE_7__["JournalCardComponent"],
                _body_body_component__WEBPACK_IMPORTED_MODULE_9__["BodyComponent"]
            ]
        })
    ], SharedModule);
    return SharedModule;
}());



/***/ }),

/***/ "./src/main.ts":
/*!*********************!*\
  !*** ./src/main.ts ***!
  \*********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser-dynamic */ "./node_modules/@angular/platform-browser-dynamic/fesm5/platform-browser-dynamic.js");
/* harmony import */ var _app_catalog_app_catalog_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./app-catalog/app-catalog.module */ "./src/app-catalog/app-catalog.module.ts");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./environments/environment */ "./src/environments/environment.ts");
/* harmony import */ var hammerjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! hammerjs */ "./node_modules/hammerjs/hammer.js");
/* harmony import */ var hammerjs__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(hammerjs__WEBPACK_IMPORTED_MODULE_4__);



//import { AppModule } from './app-harvester/app-harvester.module';


if (_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].production) {
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["enableProdMode"])();
}
Object(_angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_1__["platformBrowserDynamic"])().bootstrapModule(_app_catalog_app_catalog_module__WEBPACK_IMPORTED_MODULE_2__["AppModule"])
    .catch(function (err) { return console.log(err); });


/***/ }),

/***/ 0:
/*!***************************!*\
  !*** multi ./src/main.ts ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/malayo/www/tocororo/portal/src/main.ts */"./src/main.ts");


/***/ })

},[[0,"runtime","vendor"]]]);
//# sourceMappingURL=main.js.map