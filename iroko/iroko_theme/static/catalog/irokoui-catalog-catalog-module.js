(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["irokoui-catalog-catalog-module"],{

/***/ "./src/irokoui/catalog/catalog-filters/catalog-filters.component.html":
/*!****************************************************************************!*\
  !*** ./src/irokoui/catalog/catalog-filters/catalog-filters.component.html ***!
  \****************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<!-- <div fxLayout=\"row wrap\" fxLayoutAlign=\"start center\" fxLayoutAlign.xs=\"center center\" fxLayoutGap=\"1em\" fxLayoutGap.xs=\"0\"> -->\n\n  <ng-template toco-Filter></ng-template>\n\n<!-- </div> -->\n\n<button mat-icon-button [matMenuTriggerFor]=\"menu\">\n    <mat-icon>add</mat-icon>\n</button>\n  <mat-menu #menu=\"matMenu\" >\n    <ng-container *ngFor=\"let item of filters_data,let i=index\">\n        <ng-container *ngIf=\"item.is_enabled\">\n          <button mat-menu-item (click)=\"addFilter(i)\">\n            {{item.name}}\n          </button>\n        </ng-container>\n    </ng-container>\n    \n\n    \n  </mat-menu>"

/***/ }),

/***/ "./src/irokoui/catalog/catalog-filters/catalog-filters.component.scss":
/*!****************************************************************************!*\
  !*** ./src/irokoui/catalog/catalog-filters/catalog-filters.component.scss ***!
  \****************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".width-100 {\n  width: 100%; }\n\n.mat-menu-item {\n  height: 37px; }\n"

/***/ }),

/***/ "./src/irokoui/catalog/catalog-filters/catalog-filters.component.ts":
/*!**************************************************************************!*\
  !*** ./src/irokoui/catalog/catalog-filters/catalog-filters.component.ts ***!
  \**************************************************************************/
/*! exports provided: CatalogFiltersComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CatalogFiltersComponent", function() { return CatalogFiltersComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _filters_filter_item__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../filters/filter-item */ "./src/irokoui/filters/filter-item.ts");
/* harmony import */ var _filters_boolean_filter_boolean_filter_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../filters/boolean-filter/boolean-filter.component */ "./src/irokoui/filters/boolean-filter/boolean-filter.component.ts");
/* harmony import */ var _catalog_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../catalog.service */ "./src/irokoui/catalog/catalog.service.ts");
/* harmony import */ var _filters_filter_container_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../filters/filter-container.service */ "./src/irokoui/filters/filter-container.service.ts");
/* harmony import */ var _filters_filter_container_filter_container_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../filters/filter-container/filter-container.component */ "./src/irokoui/filters/filter-container/filter-container.component.ts");
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
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};






var CatalogFiltersComponent = /** @class */ (function (_super) {
    __extends(CatalogFiltersComponent, _super);
    function CatalogFiltersComponent(componentFactoryResolver, childrenService, service) {
        var _this = _super.call(this, componentFactoryResolver, childrenService) || this;
        _this.componentFactoryResolver = componentFactoryResolver;
        _this.childrenService = childrenService;
        _this.service = service;
        return _this;
    }
    CatalogFiltersComponent.prototype.ngOnInit = function () {
        var _this = this;
        _super.prototype.ngOnInit.call(this);
        this.addOperator();
        default_filters.forEach(function (filter) {
            _this.filters_data.push(filter);
        });
        this.service.getJournalsVocab().subscribe(function (response) {
            response.data.vocabularies.forEach(function (vocab) {
                _this.service.getTerminosByVocab(vocab.name).subscribe(function (termsResponse) {
                    _this.filters_data.push({
                        index: _this.filters_data.length,
                        field: 'terms',
                        type: 'select-autocomplete',
                        placeholder: vocab.name,
                        name: vocab.name,
                        idVocab: vocab.id,
                        selectOptions: termsResponse.data.terms,
                        is_enabled: true
                    });
                });
            });
        });
    };
    CatalogFiltersComponent.prototype.addOperator = function () {
        var f = new _filters_filter_item__WEBPACK_IMPORTED_MODULE_1__["FilterItem"](_filters_boolean_filter_boolean_filter_component__WEBPACK_IMPORTED_MODULE_2__["BooleanFilterComponent"], { field: 'op', value: true, name: ['AND', 'OR'], is_enabled: false, index: -1 });
        // this.current_filters.push(f);
        var componentFactory = this.componentFactoryResolver.resolveComponentFactory(f.component);
        var viewContainerRef = this.adHost.viewContainerRef;
        // viewContainerRef.clear();
        var componentRef = viewContainerRef.createComponent(componentFactory);
        componentRef.instance.data = f.data;
    };
    CatalogFiltersComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-catalog-filters-container',
            template: __webpack_require__(/*! ./catalog-filters.component.html */ "./src/irokoui/catalog/catalog-filters/catalog-filters.component.html"),
            styles: [__webpack_require__(/*! ./catalog-filters.component.scss */ "./src/irokoui/catalog/catalog-filters/catalog-filters.component.scss")]
        }),
        __metadata("design:paramtypes", [_angular_core__WEBPACK_IMPORTED_MODULE_0__["ComponentFactoryResolver"],
            _filters_filter_container_service__WEBPACK_IMPORTED_MODULE_4__["FilterContainerService"],
            _catalog_service__WEBPACK_IMPORTED_MODULE_3__["CatalogService"]])
    ], CatalogFiltersComponent);
    return CatalogFiltersComponent;
}(_filters_filter_container_filter_container_component__WEBPACK_IMPORTED_MODULE_5__["FilterContainerComponent"]));

var default_filters = [
    {
        index: 0,
        field: 'title',
        type: 'search',
        placeholder: 'Título',
        name: 'Título',
        is_enabled: true
    },
    {
        index: 1,
        field: 'issn',
        type: 'text',
        placeholder: 'ISSN',
        name: 'ISSN',
        is_enabled: true
    } /*,
    {
      index: 2,
      field: 'e_issn',
      type: 'text',
      placeholder: 'eISSN',
      name: 'eISSN',
      is_enabled: true
    },
    {
      index: 3,
      field: 'i_issn',
      type: 'text',
      placeholder: 'iISSN',
      name: 'iISSN',
      is_enabled: true
    }*/,
    {
        index: 2,
        field: 'rnps',
        type: 'number',
        placeholder: 'RNPS',
        name: 'RNPS',
        is_enabled: true
    } /*,
    {
      index: 5,
      field: 'term',
      type: 'select',
      placeholder: 'Términos',
      name: 'Términos',
      is_enabled: true
    } */
];


/***/ }),

/***/ "./src/irokoui/catalog/catalog-routing.module.ts":
/*!*******************************************************!*\
  !*** ./src/irokoui/catalog/catalog-routing.module.ts ***!
  \*******************************************************/
/*! exports provided: CatalogRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CatalogRoutingModule", function() { return CatalogRoutingModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _catalog_catalog_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./catalog/catalog.component */ "./src/irokoui/catalog/catalog/catalog.component.ts");
/* harmony import */ var _journals_journals_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./journals/journals.component */ "./src/irokoui/catalog/journals/journals.component.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};




var routes = [{
        path: '',
        component: _catalog_catalog_component__WEBPACK_IMPORTED_MODULE_2__["CatalogComponent"],
        children: [
            {
                path: '',
                component: _journals_journals_component__WEBPACK_IMPORTED_MODULE_3__["JournalsComponent"],
                data: {
                    title: 'Revistas'
                }
            }
        ]
    }];
var CatalogRoutingModule = /** @class */ (function () {
    function CatalogRoutingModule() {
    }
    CatalogRoutingModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_1__["RouterModule"]]
        })
    ], CatalogRoutingModule);
    return CatalogRoutingModule;
}());



/***/ }),

/***/ "./src/irokoui/catalog/catalog.module.ts":
/*!***********************************************!*\
  !*** ./src/irokoui/catalog/catalog.module.ts ***!
  \***********************************************/
/*! exports provided: CatalogModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CatalogModule", function() { return CatalogModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _catalog_routing_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./catalog-routing.module */ "./src/irokoui/catalog/catalog-routing.module.ts");
/* harmony import */ var _journals_journals_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./journals/journals.component */ "./src/irokoui/catalog/journals/journals.component.ts");
/* harmony import */ var _catalog_catalog_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./catalog/catalog.component */ "./src/irokoui/catalog/catalog/catalog.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../shared/shared.module */ "./src/irokoui/shared/shared.module.ts");
/* harmony import */ var _catalog_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./catalog.service */ "./src/irokoui/catalog/catalog.service.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _filters_filters_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../filters/filters.module */ "./src/irokoui/filters/filters.module.ts");
/* harmony import */ var _catalog_filters_catalog_filters_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./catalog-filters/catalog-filters.component */ "./src/irokoui/catalog/catalog-filters/catalog-filters.component.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};










var CatalogModule = /** @class */ (function () {
    function CatalogModule() {
    }
    CatalogModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
                _catalog_routing_module__WEBPACK_IMPORTED_MODULE_2__["CatalogRoutingModule"],
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_5__["SharedModule"],
                // InfiniteScrollModule,
                _angular_forms__WEBPACK_IMPORTED_MODULE_7__["ReactiveFormsModule"],
                _filters_filters_module__WEBPACK_IMPORTED_MODULE_8__["FiltersModule"]
            ],
            declarations: [
                _journals_journals_component__WEBPACK_IMPORTED_MODULE_3__["JournalsComponent"],
                _catalog_catalog_component__WEBPACK_IMPORTED_MODULE_4__["CatalogComponent"],
                _catalog_filters_catalog_filters_component__WEBPACK_IMPORTED_MODULE_9__["CatalogFiltersComponent"]
            ],
            providers: [
                _catalog_service__WEBPACK_IMPORTED_MODULE_6__["CatalogService"],
            ]
        })
    ], CatalogModule);
    return CatalogModule;
}());



/***/ }),

/***/ "./src/irokoui/catalog/catalog/catalog.component.html":
/*!************************************************************!*\
  !*** ./src/irokoui/catalog/catalog/catalog.component.html ***!
  \************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<router-outlet></router-outlet>"

/***/ }),

/***/ "./src/irokoui/catalog/catalog/catalog.component.scss":
/*!************************************************************!*\
  !*** ./src/irokoui/catalog/catalog/catalog.component.scss ***!
  \************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/irokoui/catalog/catalog/catalog.component.ts":
/*!**********************************************************!*\
  !*** ./src/irokoui/catalog/catalog/catalog.component.ts ***!
  \**********************************************************/
/*! exports provided: CatalogComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CatalogComponent", function() { return CatalogComponent; });
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

var CatalogComponent = /** @class */ (function () {
    function CatalogComponent() {
    }
    CatalogComponent.prototype.ngOnInit = function () {
    };
    CatalogComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-catalog',
            template: __webpack_require__(/*! ./catalog.component.html */ "./src/irokoui/catalog/catalog/catalog.component.html"),
            styles: [__webpack_require__(/*! ./catalog.component.scss */ "./src/irokoui/catalog/catalog/catalog.component.scss")]
        }),
        __metadata("design:paramtypes", [])
    ], CatalogComponent);
    return CatalogComponent;
}());



/***/ }),

/***/ "./src/irokoui/catalog/journals/journals.component.html":
/*!**************************************************************!*\
  !*** ./src/irokoui/catalog/journals/journals.component.html ***!
  \**************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<!-- <div infiniteScroll [infiniteScrollDistance]=\"0\" [infiniteScrollUpDistance]=\"0.5\" [infiniteScrollThrottle]=\"10\" (scrolled)=\"onScrollDown()\"\n  (scrolledUp)=\"onScrollUp()\"> -->\n\n\n    <!-- <toco-page-header [info]=\"['Catálogo de Revistas Científicas Cubanas']\">\n    </toco-page-header> --> \n\n\n    <div fxLayoutAlign=\"end center\" fxLayout=\"row\">\n      <button mat-icon-button [matMenuTriggerFor]=\"menu\">\n        <mat-icon>dashboard</mat-icon>\n      </button>\n      <mat-menu #menu=\"matMenu\">\n        <button mat-menu-item (click)=\"changeLayoutPosition(0)\">\n          <mat-icon>arrow_forward</mat-icon>\n          <span>{{layoutPosition[0].name}}</span>\n        </button>\n        <button mat-menu-item (click)=\"changeLayoutPosition(1)\">\n          <mat-icon>arrow_back</mat-icon>\n          <span>{{layoutPosition[1].name}}</span>\n        </button>\n        <button mat-menu-item (click)=\"changeLayoutPosition(2)\">\n          <mat-icon>arrow_upward</mat-icon>\n          <span>{{layoutPosition[2].name}}</span>\n        </button>\n        <button mat-menu-item (click)=\"changeLayoutPosition(3)\">\n          <mat-icon>arrow_downward</mat-icon>\n          <span>{{layoutPosition[3].name}}</span>\n        </button>\n      </mat-menu>\n    </div>\n\n    \n    <div fxLayout=\"{{currentlayout.layout}}\" fxLayout.xs=\"column nowrap\" fxLayoutAlign=\"{{currentlayout.aling}}\">\n      \n      <toco-catalog-filters-container fxLayout=\"row wrap\" fxLayout.xs=\"column wrap\" fxFlex=\"{{currentlayout.width}}\" fxLayoutAlign=\"start center\" fxLayoutAlign.xs=\"center center\"\n        fxLayoutGap=\"1em\" class=\"width-90 back-grey mat-elevation-z8\">\n      </toco-catalog-filters-container>\n      \n      \n\n      <div class=\"mat-elevation-z8 width-90 margin1em\">\n        <table mat-table [dataSource]=\"dataSource\" multiTemplateDataRows>\n          <ng-container matColumnDef=\"title\">\n            <th mat-header-cell *matHeaderCellDef>Titulo</th>\n            <td mat-cell *matCellDef=\"let element\"> {{element.jinformation.title}} </td>\n          </ng-container>\n          <ng-container matColumnDef=\"rnps\">\n            <th mat-header-cell *matHeaderCellDef>RNPS</th>\n            <td mat-cell *matCellDef=\"let element\"> {{element.jinformation.rnps}} </td>\n          </ng-container>\n          <ng-container matColumnDef=\"p-issn\">\n            <th mat-header-cell *matHeaderCellDef>P-ISSN</th>\n            <td mat-cell *matCellDef=\"let element\"> {{element.jinformation.issn.p}} </td>\n          </ng-container>\n          <ng-container matColumnDef=\"url\">\n            <th mat-header-cell *matHeaderCellDef>URL</th>\n            <td mat-cell *matCellDef=\"let element\"> {{element.jinformation.url}} </td>\n          </ng-container>\n          \n          <!-- Expanded Content Column - The detail row is made up of this one column that spans across all columns -->\n          <ng-container matColumnDef=\"expandedDetail\">\n            <td mat-cell *matCellDef=\"let element\" [attr.colspan]=\"columnsToDisplay.length\">\n              <div class=\"example-element-detail\" [@detailExpand]=\"element == expandedElement ? 'expanded' : 'collapsed'\">\n                <div class=\"example-element-description e2e-inner-html-bound\" [innerHTML]=\"element.jinformation.description\"></div>\n                <div class=\"example-element-description\" fxLayout=\"row\" fxLayoutAlign=\"center end\">\n                  <a mat-flat-button color=\"primary\" href=\"{{irokoHost}}/{{element.tocoID}}\" >\n                    Ver\n                  </a>\n                </div>\n                \n              </div>\n            </td>\n          </ng-container>\n\n          <tr mat-header-row *matHeaderRowDef=\"columnsToDisplay\"></tr>\n          <tr mat-row *matRowDef=\"let element; columns: columnsToDisplay;\" class=\"example-element-row\" [class.example-expanded-row]=\"expandedElement === element\"\n            (click)=\"expandedElement = element\">\n          </tr>\n          <tr mat-row *matRowDef=\"let row; columns: ['expandedDetail']\" class=\"example-detail-row\"></tr>\n        </table>\n        <mat-paginator [length]=\"length\"\n              [pageSize]=\"pageSize\"\n              [pageSizeOptions]=\"pageSizeOptions\"\n              (page)=\"fetchJournalData()\">\n        </mat-paginator>\n      </div>\n      \n      <mat-card *ngIf=\"!isEmpty()\" class=\"center-spinner\" fxLayout=\"row\" fxLayoutAlign=\"center center\" fxLayoutGap=\"gappx\">\n        <mat-spinner></mat-spinner>\n        <!--<mat-progress-bar mode=\"indeterminate\"></mat-progress-bar>-->\n      </mat-card>\n\n      <!-- <mat-card *ngIf=\"isEmpty()\" class=\"center-spinner\" fxLayout=\"row\" fxLayoutAlign=\"center center\" fxLayoutGap=\"gappx\">\n        <h1>No hay Información para Mostrar</h1>\n      </mat-card> -->\n    </div>\n\n    <!-- \n      </mat-drawer-content>\n\n\n\n    </mat-drawer-container> -->\n\n<!-- </div> -->"

/***/ }),

/***/ "./src/irokoui/catalog/journals/journals.component.scss":
/*!**************************************************************!*\
  !*** ./src/irokoui/catalog/journals/journals.component.scss ***!
  \**************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".width-card {\n  width: 30%;\n  min-width: 240px;\n  margin-left: 24px;\n  margin-top: 24px; }\n\n.card-float-left {\n  float: left; }\n\n.center-spinner {\n  width: 90.5%;\n  min-width: 240px;\n  margin-left: 24px;\n  margin-right: 24px;\n  margin-top: 24px; }\n\n.back-grey {\n  background: rgba(0, 0, 0, 0.01);\n  margin: 1.5em 1em;\n  padding: 1em;\n  min-width: 18em; }\n\n.width-90 {\n  width: 90%; }\n\n.width-93 {\n  width: 93.5%; }\n\ntable {\n  width: 90%; }\n\n.margin1em {\n  margin: 1em; }\n\n.menu-pull-right {\n  flex: 1 1 auto; }\n\ntable.mat-table {\n  width: 100%; }\n\ntr.example-detail-row {\n  height: 0; }\n\ntr.example-element-row:not(.example-expanded-row):hover {\n  background: #f5f5f5; }\n\ntr.example-element-row:not(.example-expanded-row):active {\n  background: #efefef; }\n\n.example-element-row td {\n  border-bottom-width: 0; }\n\n.example-element-detail {\n  overflow: hidden;\n  display: flex; }\n\n.example-element-diagram {\n  min-width: 80px;\n  border: 2px solid black;\n  padding: 8px;\n  font-weight: lighter;\n  margin: 8px 0;\n  height: 104px; }\n\n.example-element-symbol {\n  font-weight: bold;\n  font-size: 40px;\n  line-height: normal; }\n\n.example-element-description {\n  padding: 16px; }\n\n.example-element-description-attribution {\n  opacity: 0.5; }\n"

/***/ }),

/***/ "./src/irokoui/catalog/journals/journals.component.ts":
/*!************************************************************!*\
  !*** ./src/irokoui/catalog/journals/journals.component.ts ***!
  \************************************************************/
/*! exports provided: JournalsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "JournalsComponent", function() { return JournalsComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _entities_journal_entity__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../entities/journal.entity */ "./src/irokoui/entities/journal.entity.ts");
/* harmony import */ var _catalog_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../catalog.service */ "./src/irokoui/catalog/catalog.service.ts");
/* harmony import */ var _core_metadata_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../core/metadata.service */ "./src/irokoui/core/metadata.service.ts");
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/animations */ "./node_modules/@angular/animations/fesm5/animations.js");
/* harmony import */ var _angular_material__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material */ "./node_modules/@angular/material/esm5/material.es5.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _catalog_filters_catalog_filters_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../catalog-filters/catalog-filters.component */ "./src/irokoui/catalog/catalog-filters/catalog-filters.component.ts");
/* harmony import */ var _filters_filters_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../filters/filters.service */ "./src/irokoui/filters/filters.service.ts");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../environments/environment */ "./src/environments/environment.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};











var JournalsComponent = /** @class */ (function () {
    function JournalsComponent(service, metadata, filterService) {
        this.service = service;
        this.metadata = metadata;
        this.filterService = filterService;
        this.journalList = [];
        this.loading = true;
        this.dataSource = new _angular_material__WEBPACK_IMPORTED_MODULE_5__["MatTableDataSource"]();
        this.columnsToDisplay = ['title', 'rnps', 'p-issn', 'url'];
        this.length = 0;
        this.pageSize = 5;
        this.pageSizeOptions = [5, 10, 15, 20];
        this.irokoHost = _environments_environment__WEBPACK_IMPORTED_MODULE_10__["environment"].irokoHost + "/catalog";
        this.layoutPosition = [
            {
                name: 'Derecha',
                layout: 'row-reverse',
                aling: 'center baseline',
                width: '22'
            },
            {
                name: 'Izquierda',
                layout: 'row',
                aling: 'center baseline',
                width: '22'
            },
            {
                name: 'Arriba',
                layout: 'column',
                aling: 'center center',
                width: '90'
            },
            {
                name: 'Abajo',
                layout: 'column-reverse',
                aling: 'center center',
                width: '90'
            }
        ];
        this.currentlayout = this.layoutPosition[1];
    }
    JournalsComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.metadata.setTitleDescription("Catálogo de Revistas Científicas", "");
        this.paginator.firstPage();
        this.paginator.pageSize = 5;
        this.service.getJournalsCount().subscribe(function (response) {
            _this.length = response.data.count;
        });
        this.fetchJournalData();
        this.filterService.paramsChanged.subscribe(function (params) {
            _this.params = params;
            _this.fetchJournalData();
        });
    };
    // onPaginatorChanged(){
    //   this.filterService.changeFilter('count',this.paginator.pageSize, false);
    //   this.filterService.changeFilter('page',this.paginator.pageIndex);
    // }
    JournalsComponent.prototype.fetchJournalData = function () {
        var _this = this;
        this.loading = true;
        //this.dataSource.data = this.service.getJournalsPage(this.count, this.page);
        var arr = new Array();
        Object(rxjs__WEBPACK_IMPORTED_MODULE_6__["merge"])().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["startWith"])({}), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["switchMap"])(function () {
            _this.loading = true;
            return _this.service.getJournalsPage(_this.paginator.pageSize, _this.paginator.pageIndex, _this.params);
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["map"])(function (response) {
            // Flip flag to show that loading has finished.
            _this.loading = false;
            // this.isRateLimitReached = false;
            // this.resultsLength = response.total_count;
            _this.length = response.data.sources.count;
            response.data.sources.data.forEach(function (item) {
                var j = new _entities_journal_entity__WEBPACK_IMPORTED_MODULE_1__["Journal"](0, 0);
                j.id = item.id;
                j.tocoID = item.uuid;
                var info = new _entities_journal_entity__WEBPACK_IMPORTED_MODULE_1__["JournalInformation"]();
                info.url = item.data != null ? item.data.url : "";
                info.title = item.name;
                info.subtitle = item.subtitle;
                info.shortname = item.shortname;
                var issn = new _entities_journal_entity__WEBPACK_IMPORTED_MODULE_1__["ISSN"]();
                issn.e = item.data != null ? item.data.issn.e : "";
                issn.l = item.data != null ? item.data.issn.l : "";
                issn.p = item.data != null ? item.data.issn.p : "";
                info.issn = issn;
                info.rnps = item.data != null ? item.data.rnps : "";
                info.logo = item.data != null ? item.data.logo : "";
                info.purpose = item.purpose;
                info.description = item.data != null ? item.data.description : "";
                j.jinformation = info;
                arr.push(j);
            });
            return arr;
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["catchError"])(function (error) {
            _this.loading = false;
            console.log("ERRORRR  " + error);
            // Catch if the GitHub API has reached its rate limit. Return empty data.
            // this.isRateLimitReached = true;
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_6__["of"])([]);
        })).subscribe(function (data) { return _this.dataSource.data = data; });
    };
    JournalsComponent.prototype.onScrollUp = function () {
        // console.log("scrolled up!!");
    };
    JournalsComponent.prototype.isEmpty = function () {
        if (this.journalList.length == 0) {
            this.loading = false;
            return true;
        }
        return false;
    };
    JournalsComponent.prototype.isLoading = function () {
        return this.loading;
    };
    JournalsComponent.prototype.openme = function () {
        var a = navigator.userAgent.match(/Android/i);
        var b = navigator.userAgent.match(/BlackBerry/i);
        var apple = navigator.userAgent.match(/iPhone|iPad|iPod/i);
        var o = navigator.userAgent.match(/Opera Mini/i);
        var i = navigator.userAgent.match(/IEMobile/i);
        if (a != null || b != null || apple != null || o != null || i != null)
            return false;
        return true;
    };
    JournalsComponent.prototype.changeLayoutPosition = function (index) {
        this.currentlayout = this.layoutPosition[index];
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewChild"])(_angular_material__WEBPACK_IMPORTED_MODULE_5__["MatPaginator"]),
        __metadata("design:type", _angular_material__WEBPACK_IMPORTED_MODULE_5__["MatPaginator"])
    ], JournalsComponent.prototype, "paginator", void 0);
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewChild"])(_catalog_filters_catalog_filters_component__WEBPACK_IMPORTED_MODULE_8__["CatalogFiltersComponent"]),
        __metadata("design:type", _catalog_filters_catalog_filters_component__WEBPACK_IMPORTED_MODULE_8__["CatalogFiltersComponent"])
    ], JournalsComponent.prototype, "filter_component", void 0);
    JournalsComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-journals',
            template: __webpack_require__(/*! ./journals.component.html */ "./src/irokoui/catalog/journals/journals.component.html"),
            styles: [__webpack_require__(/*! ./journals.component.scss */ "./src/irokoui/catalog/journals/journals.component.scss")],
            animations: [
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_4__["trigger"])('detailExpand', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_4__["state"])('collapsed', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_4__["style"])({ height: '0px', minHeight: '0', display: 'none' })),
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_4__["state"])('expanded', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_4__["style"])({ height: '*' })),
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_4__["transition"])('expanded <=> collapsed', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_4__["animate"])('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
                ]),
            ],
        }),
        __metadata("design:paramtypes", [_catalog_service__WEBPACK_IMPORTED_MODULE_2__["CatalogService"],
            _core_metadata_service__WEBPACK_IMPORTED_MODULE_3__["MetadataService"],
            _filters_filters_service__WEBPACK_IMPORTED_MODULE_9__["FiltersService"]])
    ], JournalsComponent);
    return JournalsComponent;
}());



/***/ }),

/***/ "./src/irokoui/entities/journal.entity.ts":
/*!************************************************!*\
  !*** ./src/irokoui/entities/journal.entity.ts ***!
  \************************************************/
/*! exports provided: Journal, JournalInformation, ISSN */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Journal", function() { return Journal; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "JournalInformation", function() { return JournalInformation; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ISSN", function() { return ISSN; });
/* harmony import */ var _entity__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./entity */ "./src/irokoui/entities/entity.ts");
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

var Journal = /** @class */ (function (_super) {
    __extends(Journal, _super);
    /**
     * r: length of journal reference
     * t: length of Term
     */
    function Journal(r, t) {
        var _this = _super.call(this) || this;
        _this.jreference = new Array(r);
        _this.terms = new Array(t);
        return _this;
    }
    ;
    return Journal;
}(_entity__WEBPACK_IMPORTED_MODULE_0__["Entity"]));

var JournalInformation = /** @class */ (function () {
    function JournalInformation() {
    }
    JournalInformation.prototype.getISSN = function () {
        return this.issn.p;
    };
    return JournalInformation;
}());

var ISSN = /** @class */ (function () {
    function ISSN() {
    }
    return ISSN;
}());



/***/ }),

/***/ "./src/irokoui/filters/boolean-filter/boolean-filter.component.html":
/*!**************************************************************************!*\
  !*** ./src/irokoui/filters/boolean-filter/boolean-filter.component.html ***!
  \**************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<!-- <mat-slide-toggle [checked]=\"operator\" [(ngModel)]=\"operator\" (click)=\"change_operator_name()\">{{operator_name}}</mat-slide-toggle>\n\n<div class=\"interruptor-background\">\n    <div class=\"interruptor-selector-down\"></div>\n</div>\n<br> -->\n<div fxLayout=\"{{direction}}\" fxLayoutAlign=\"center center\" fxLayoutGap=\"5px\">\n    <label>{{data.name[0]}}</label>\n    <div class=\"mat-interruptor-background{{classDireccion}}\">\n        <div *ngIf=\"!operator;then content else other_content\"></div>\n        <ng-template #content>\n            <div class=\"mat-interruptor-selector-up{{classDireccion}}\" (click)=\"changeInterruptor()\"></div>\n        </ng-template>\n        <ng-template #other_content>\n            <div class=\"mat-interruptor-selector-down{{classDireccion}}\" (click)=\"changeInterruptor()\"></div>\n        </ng-template>\n    </div>\n    <label>{{data.name[1]}}</label>\n</div>"

/***/ }),

/***/ "./src/irokoui/filters/boolean-filter/boolean-filter.component.scss":
/*!**************************************************************************!*\
  !*** ./src/irokoui/filters/boolean-filter/boolean-filter.component.scss ***!
  \**************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".interruptor-background {\n  width: 1.01em;\n  height: 2.3em;\n  border: 0.1em solid black;\n  border-radius: 1em;\n  position: relative;\n  display: flex;\n  flex-direction: row;\n  justify-content: center;\n  background: transparent;\n  box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2), 0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 1px 3px 0 rgba(0, 0, 0, 0.12); }\n\n.interruptor-selector-down, .interruptor-selector-up {\n  width: .9em;\n  height: .9em;\n  border-radius: 50%;\n  position: absolute;\n  left: .07em;\n  box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2), 0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 1px 3px 0 rgba(0, 0, 0, 0.12); }\n\n.interruptor-selector-up {\n  top: .05em; }\n\n.interruptor-selector-down {\n  bottom: .05em; }\n\n.mat-interruptor-background, .mat-interruptor-background-horizontal {\n  width: .875em;\n  height: 2.3em;\n  background-color: rgba(248, 56, 33, 0.5);\n  background-color: rgba(100, 97, 96, 0.5);\n  border-radius: 1em;\n  position: relative;\n  display: flex;\n  flex-direction: row;\n  justify-content: center;\n  border: transparent; }\n\n.mat-interruptor-background-horizontal {\n  height: .875em;\n  width: 2.3em; }\n\n.mat-interruptor-selector-down, .mat-interruptor-selector-up, .mat-interruptor-selector-up-horizontal, .mat-interruptor-selector-down-horizontal {\n  width: 1.3em;\n  height: 1.3em;\n  border-radius: 50%;\n  position: absolute;\n  box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2), 0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 1px 3px 0 rgba(0, 0, 0, 0.12); }\n\n.mat-interruptor-selector-up {\n  top: -.1em; }\n\n.mat-interruptor-selector-down {\n  bottom: -.1em; }\n\n.mat-interruptor-selector-up-horizontal {\n  left: -.1em;\n  top: -.22em; }\n\n.mat-interruptor-selector-down-horizontal {\n  right: -.1em;\n  top: -.22em; }\n\n.mat-interruptor-selector-up:hover, .mat-interruptor-selector-down:hover, .mat-interruptor-selector-up-horizontal:hover, .mat-interruptor-selector-down-horizontal:hover {\n  cursor: pointer; }\n\n.mat-interruptor-selector-up:active, .mat-interruptor-selector-down:active, .mat-interruptor-selector-up-horizontal:active, .mat-interruptor-selector-down-horizontal:active {\n  cursor: -webkit-grabbing;\n  cursor: grabbing;\n  transition-duration: 1s;\n  box-shadow: 0 0 2px 8px rgba(248, 55, 33, 0.26); }\n\n.mat-interruptor-selector-up:active {\n  -webkit-transform: translate3d(0, 16px, 0);\n          transform: translate3d(0, 16px, 0); }\n\n.interruptor-selector-down:active {\n  -webkit-transform: translate3d(0, 0, 16px);\n          transform: translate3d(0, 0, 16px); }\n\n.mat-interruptor-selector-up-horizontal:active {\n  -webkit-transform: translate3d(16px, 0, 0);\n          transform: translate3d(16px, 0, 0); }\n\n.mat-interruptor-selector-down-horizontal:active {\n  -webkit-transform: translate3d(0, 0, 0);\n          transform: translate3d(0, 0, 0); }\n"

/***/ }),

/***/ "./src/irokoui/filters/boolean-filter/boolean-filter.component.ts":
/*!************************************************************************!*\
  !*** ./src/irokoui/filters/boolean-filter/boolean-filter.component.ts ***!
  \************************************************************************/
/*! exports provided: BooleanFilterComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BooleanFilterComponent", function() { return BooleanFilterComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _filters_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../filters.service */ "./src/irokoui/filters/filters.service.ts");
/* harmony import */ var _filter_container_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../filter-container.service */ "./src/irokoui/filters/filter-container.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var BooleanFilterComponent = /** @class */ (function () {
    function BooleanFilterComponent(filterService, filterContainerService) {
        this.filterService = filterService;
        this.filterContainerService = filterContainerService;
        this.operator = true;
        this.direction = 'column';
    }
    BooleanFilterComponent.prototype.ngOnInit = function () {
        this.operator = this.data.value;
        this.operator_name = this.data.name[0];
        if (this.data.direction) {
            this.direction = 'row';
            this.classDireccion = '-horizontal';
        }
    };
    BooleanFilterComponent.prototype.remove_component = function () {
        this.filterService.deleteParameter(this.data.field);
        this.filterContainerService.filterDeleted(this.data.index);
    };
    BooleanFilterComponent.prototype.change_operator_name = function () {
        this.operator ? this.operator_name = this.data.name[1] : this.operator_name = this.data.name[0];
        var value = this.operator ? 'OR' : 'AND';
        this.filterService.changeFilter(this.data.field, value);
    };
    BooleanFilterComponent.prototype.changeInterruptor = function () {
        this.operator = !this.operator;
        this.change_operator_name();
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", Object)
    ], BooleanFilterComponent.prototype, "data", void 0);
    BooleanFilterComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-boolean-filter',
            template: __webpack_require__(/*! ./boolean-filter.component.html */ "./src/irokoui/filters/boolean-filter/boolean-filter.component.html"),
            styles: [__webpack_require__(/*! ./boolean-filter.component.scss */ "./src/irokoui/filters/boolean-filter/boolean-filter.component.scss")]
        }),
        __metadata("design:paramtypes", [_filters_service__WEBPACK_IMPORTED_MODULE_1__["FiltersService"],
            _filter_container_service__WEBPACK_IMPORTED_MODULE_2__["FilterContainerService"]])
    ], BooleanFilterComponent);
    return BooleanFilterComponent;
}());



/***/ }),

/***/ "./src/irokoui/filters/filter-container.service.ts":
/*!*********************************************************!*\
  !*** ./src/irokoui/filters/filter-container.service.ts ***!
  \*********************************************************/
/*! exports provided: FilterContainerService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FilterContainerService", function() { return FilterContainerService; });
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

var FilterContainerService = /** @class */ (function () {
    function FilterContainerService() {
        this.emitter = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
    }
    FilterContainerService.prototype.filterDeleted = function (filterIndex) {
        this.emitter.emit(filterIndex);
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"])(),
        __metadata("design:type", _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"])
    ], FilterContainerService.prototype, "emitter", void 0);
    FilterContainerService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])(),
        __metadata("design:paramtypes", [])
    ], FilterContainerService);
    return FilterContainerService;
}());



/***/ }),

/***/ "./src/irokoui/filters/filter-container/filter-container.component.html":
/*!******************************************************************************!*\
  !*** ./src/irokoui/filters/filter-container/filter-container.component.html ***!
  \******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<!-- <div fxLayout=\"row wrap\" fxLayoutAlign=\"start center\" fxLayoutAlign.xs=\"center center\" fxLayoutGap=\"1em\" fxLayoutGap.xs=\"0\"> -->\n\n  <ng-template toco-Filter></ng-template>\n\n<!-- </div> -->\n\n<button mat-icon-button [matMenuTriggerFor]=\"menu\">\n    <mat-icon>add</mat-icon>\n</button>\n  <mat-menu #menu=\"matMenu\" >\n    <ng-container *ngFor=\"let item of filters_data,let i=index\">\n        <ng-container *ngIf=\"item.is_enabled\">\n          <button mat-menu-item (click)=\"addFilter(i)\">\n            {{item.name}}\n          </button>\n        </ng-container>\n    </ng-container>\n    \n\n    \n  </mat-menu>"

/***/ }),

/***/ "./src/irokoui/filters/filter-container/filter-container.component.scss":
/*!******************************************************************************!*\
  !*** ./src/irokoui/filters/filter-container/filter-container.component.scss ***!
  \******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".width-100 {\n  width: 100%; }\n\n.mat-menu-item {\n  height: 37px; }\n"

/***/ }),

/***/ "./src/irokoui/filters/filter-container/filter-container.component.ts":
/*!****************************************************************************!*\
  !*** ./src/irokoui/filters/filter-container/filter-container.component.ts ***!
  \****************************************************************************/
/*! exports provided: FilterContainerComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FilterContainerComponent", function() { return FilterContainerComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _filter_item__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../filter-item */ "./src/irokoui/filters/filter-item.ts");
/* harmony import */ var _filter_directive__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../filter.directive */ "./src/irokoui/filters/filter.directive.ts");
/* harmony import */ var _title_filter_title_filter_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../title-filter/title-filter.component */ "./src/irokoui/filters/title-filter/title-filter.component.ts");
/* harmony import */ var _boolean_filter_boolean_filter_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../boolean-filter/boolean-filter.component */ "./src/irokoui/filters/boolean-filter/boolean-filter.component.ts");
/* harmony import */ var _select_filter_select_filter_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../select-filter/select-filter.component */ "./src/irokoui/filters/select-filter/select-filter.component.ts");
/* harmony import */ var _select_autocomplete_filter_select_autocomplete_filter_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../select-autocomplete-filter/select-autocomplete-filter.component */ "./src/irokoui/filters/select-autocomplete-filter/select-autocomplete-filter.component.ts");
/* harmony import */ var _filter_container_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../filter-container.service */ "./src/irokoui/filters/filter-container.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};








var FilterContainerComponent = /** @class */ (function () {
    function FilterContainerComponent(componentFactoryResolver, childrenService) {
        this.componentFactoryResolver = componentFactoryResolver;
        this.childrenService = childrenService;
        this.filter_url = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
    }
    FilterContainerComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.filters_data = [];
        this.childrenService.emitter.subscribe(function (filterIndex) {
            _this.deleteFilter(filterIndex);
        });
    };
    FilterContainerComponent.prototype.addFilter = function (index) {
        var data = this.filters_data[index];
        var viewContainerRef = this.adHost.viewContainerRef;
        data.pos = viewContainerRef.length;
        var f = this.newFilter(data);
        // this.current_filters.push(f);
        var componentFactory = this.componentFactoryResolver.resolveComponentFactory(f.component);
        var componentRef = viewContainerRef.createComponent(componentFactory);
        componentRef.instance.data = f.data;
        //this.delete_item_of_filters(pos);
        this.filters_data[index].is_enabled = false;
    };
    FilterContainerComponent.prototype.newFilter = function (data_filter) {
        data_filter.viewContainerRef = this.adHost.viewContainerRef;
        var f = null;
        switch (data_filter.type) {
            case 'select': {
                f = new _filter_item__WEBPACK_IMPORTED_MODULE_1__["FilterItem"](_select_filter_select_filter_component__WEBPACK_IMPORTED_MODULE_5__["SelectFilterComponent"], data_filter);
                break;
            }
            case 'boolean': {
                f = new _filter_item__WEBPACK_IMPORTED_MODULE_1__["FilterItem"](_boolean_filter_boolean_filter_component__WEBPACK_IMPORTED_MODULE_4__["BooleanFilterComponent"], data_filter);
                break;
            }
            case 'select-autocomplete': {
                f = new _filter_item__WEBPACK_IMPORTED_MODULE_1__["FilterItem"](_select_autocomplete_filter_select_autocomplete_filter_component__WEBPACK_IMPORTED_MODULE_6__["SelectAutocompleteFilterComponent"], data_filter);
                break;
            }
            default: f = new _filter_item__WEBPACK_IMPORTED_MODULE_1__["FilterItem"](_title_filter_title_filter_component__WEBPACK_IMPORTED_MODULE_3__["TitleFilterComponent"], data_filter);
        }
        return f;
    };
    FilterContainerComponent.prototype.deleteFilter = function (index) {
        var last_pos = this.filters_data[index].pos;
        this.adHost.viewContainerRef.remove(this.filters_data[index].pos);
        this.filters_data[index].pos = -1;
        this.filters_data[index].is_enabled = true;
        for (var i = 0; i < this.filters_data.length; i++) {
            if (!this.filters_data[i].is_enabled && this.filters_data[i].pos > last_pos) {
                this.filters_data[i].pos = this.filters_data[i].pos - 1;
            }
        }
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"])(),
        __metadata("design:type", _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"])
    ], FilterContainerComponent.prototype, "filter_url", void 0);
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewChild"])(_filter_directive__WEBPACK_IMPORTED_MODULE_2__["FilterDirective"]),
        __metadata("design:type", _filter_directive__WEBPACK_IMPORTED_MODULE_2__["FilterDirective"])
    ], FilterContainerComponent.prototype, "adHost", void 0);
    FilterContainerComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-filter-container',
            template: __webpack_require__(/*! ./filter-container.component.html */ "./src/irokoui/filters/filter-container/filter-container.component.html"),
            styles: [__webpack_require__(/*! ./filter-container.component.scss */ "./src/irokoui/filters/filter-container/filter-container.component.scss")]
        }),
        __metadata("design:paramtypes", [_angular_core__WEBPACK_IMPORTED_MODULE_0__["ComponentFactoryResolver"],
            _filter_container_service__WEBPACK_IMPORTED_MODULE_7__["FilterContainerService"]])
    ], FilterContainerComponent);
    return FilterContainerComponent;
}());



/***/ }),

/***/ "./src/irokoui/filters/filter-item.ts":
/*!********************************************!*\
  !*** ./src/irokoui/filters/filter-item.ts ***!
  \********************************************/
/*! exports provided: FilterItem, FilterHttpMap */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FilterItem", function() { return FilterItem; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FilterHttpMap", function() { return FilterHttpMap; });
var FilterItem = /** @class */ (function () {
    function FilterItem(component, data) {
        this.component = component;
        this.data = data;
    }
    return FilterItem;
}());

var FilterHttpMap = /** @class */ (function () {
    function FilterHttpMap(field, value) {
        this.field = field;
        this.value = value;
    }
    return FilterHttpMap;
}());



/***/ }),

/***/ "./src/irokoui/filters/filter.directive.ts":
/*!*************************************************!*\
  !*** ./src/irokoui/filters/filter.directive.ts ***!
  \*************************************************/
/*! exports provided: FilterDirective */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FilterDirective", function() { return FilterDirective; });
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

var FilterDirective = /** @class */ (function () {
    function FilterDirective(viewContainerRef) {
        this.viewContainerRef = viewContainerRef;
    }
    FilterDirective = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Directive"])({
            selector: '[toco-Filter]'
        }),
        __metadata("design:paramtypes", [_angular_core__WEBPACK_IMPORTED_MODULE_0__["ViewContainerRef"]])
    ], FilterDirective);
    return FilterDirective;
}());



/***/ }),

/***/ "./src/irokoui/filters/filters.module.ts":
/*!***********************************************!*\
  !*** ./src/irokoui/filters/filters.module.ts ***!
  \***********************************************/
/*! exports provided: FiltersModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FiltersModule", function() { return FiltersModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../shared/shared.module */ "./src/irokoui/shared/shared.module.ts");
/* harmony import */ var _filters_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./filters.service */ "./src/irokoui/filters/filters.service.ts");
/* harmony import */ var _title_filter_title_filter_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./title-filter/title-filter.component */ "./src/irokoui/filters/title-filter/title-filter.component.ts");
/* harmony import */ var _filter_directive__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./filter.directive */ "./src/irokoui/filters/filter.directive.ts");
/* harmony import */ var _boolean_filter_boolean_filter_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./boolean-filter/boolean-filter.component */ "./src/irokoui/filters/boolean-filter/boolean-filter.component.ts");
/* harmony import */ var _select_filter_select_filter_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./select-filter/select-filter.component */ "./src/irokoui/filters/select-filter/select-filter.component.ts");
/* harmony import */ var _select_autocomplete_filter_select_autocomplete_filter_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./select-autocomplete-filter/select-autocomplete-filter.component */ "./src/irokoui/filters/select-autocomplete-filter/select-autocomplete-filter.component.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _filter_container_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./filter-container.service */ "./src/irokoui/filters/filter-container.service.ts");
/* harmony import */ var _filter_container_filter_container_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./filter-container/filter-container.component */ "./src/irokoui/filters/filter-container/filter-container.component.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};












var FiltersModule = /** @class */ (function () {
    function FiltersModule() {
    }
    FiltersModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_1__["CommonModule"],
                _shared_shared_module__WEBPACK_IMPORTED_MODULE_2__["SharedModule"],
                // InfiniteScrollModule,
                _angular_forms__WEBPACK_IMPORTED_MODULE_9__["ReactiveFormsModule"]
            ],
            declarations: [
                _title_filter_title_filter_component__WEBPACK_IMPORTED_MODULE_4__["TitleFilterComponent"],
                _filter_directive__WEBPACK_IMPORTED_MODULE_5__["FilterDirective"],
                _boolean_filter_boolean_filter_component__WEBPACK_IMPORTED_MODULE_6__["BooleanFilterComponent"],
                _select_filter_select_filter_component__WEBPACK_IMPORTED_MODULE_7__["SelectFilterComponent"],
                _select_autocomplete_filter_select_autocomplete_filter_component__WEBPACK_IMPORTED_MODULE_8__["SelectAutocompleteFilterComponent"],
                _filter_container_filter_container_component__WEBPACK_IMPORTED_MODULE_11__["FilterContainerComponent"]
            ],
            exports: [
                _filter_directive__WEBPACK_IMPORTED_MODULE_5__["FilterDirective"],
            ],
            entryComponents: [
                _title_filter_title_filter_component__WEBPACK_IMPORTED_MODULE_4__["TitleFilterComponent"],
                _boolean_filter_boolean_filter_component__WEBPACK_IMPORTED_MODULE_6__["BooleanFilterComponent"],
                _select_filter_select_filter_component__WEBPACK_IMPORTED_MODULE_7__["SelectFilterComponent"],
                _select_autocomplete_filter_select_autocomplete_filter_component__WEBPACK_IMPORTED_MODULE_8__["SelectAutocompleteFilterComponent"]
            ],
            providers: [
                _filters_service__WEBPACK_IMPORTED_MODULE_3__["FiltersService"],
                _filter_container_service__WEBPACK_IMPORTED_MODULE_10__["FilterContainerService"]
            ]
        })
    ], FiltersModule);
    return FiltersModule;
}());



/***/ }),

/***/ "./src/irokoui/filters/filters.service.ts":
/*!************************************************!*\
  !*** ./src/irokoui/filters/filters.service.ts ***!
  \************************************************/
/*! exports provided: FiltersService, AutocompleteFilter */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FiltersService", function() { return FiltersService; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AutocompleteFilter", function() { return AutocompleteFilter; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _filter_item__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./filter-item */ "./src/irokoui/filters/filter-item.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var FiltersService = /** @class */ (function () {
    function FiltersService() {
        this.params = new Array();
        // httpParams: HttpParams = new HttpParams();
        this.autocompleteFilter = new Array();
        this.paramsChanged = new _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"]();
    }
    /**
     *
     * @param field el nombre del campo que se esta filtrando (title, etc...)
     * @param value el valor del filtro
     * @param emitEvent si se emite o no el evento de cambio de parametros, para los que estan suscritos.
     */
    FiltersService.prototype.changeFilter = function (field, value, emitEvent) {
        if (emitEvent === void 0) { emitEvent = true; }
        if (this.params.find(function (x) { return x.field == field; })) {
            this.params.find(function (x) { return x.field == field; }).value = value;
        }
        else if (field && value) {
            this.params.push(new _filter_item__WEBPACK_IMPORTED_MODULE_1__["FilterHttpMap"](field, value));
        }
        /*
        crear el httpParams... a partir del params...
        */
        // this.httpParams.set(field, value);
        if (emitEvent)
            this.paramsChanged.emit(this.params);
    };
    FiltersService.prototype.deleteParameter = function (field) {
        var paramToDelete = this.params.find(function (x) { return x.field == field; });
        if (paramToDelete) {
            this.params.splice(this.params.indexOf(this.params.find(function (x) { return x.field == field; })), 1);
            this.paramsChanged.emit(this.params);
        }
    };
    /**
     * Especifico para el filtro de terminos.
     * @param termValue identificador del termino por el cual se esta filtrando
     * @param isdelete especifica si se va a eliminar o adicionar el @param termValue
     */
    FiltersService.prototype.changeAutocompleteFilter = function (name, value) {
        var isexist = false;
        this.autocompleteFilter.forEach(function (filter) {
            if (filter.name == name) {
                filter.value = value;
                isexist = true;
            }
        });
        if (!isexist) {
            this.autocompleteFilter.push(new AutocompleteFilter(name, value));
        }
        this.createAutocompleteFilterValue();
    };
    FiltersService.prototype.deleteAutocompleteFilter = function (name) {
        this.autocompleteFilter.splice(this.autocompleteFilter.indexOf(this.autocompleteFilter.find(function (x) { return x.name == name; })), 1);
        this.createAutocompleteFilterValue();
    };
    FiltersService.prototype.createAutocompleteFilterValue = function () {
        var emitValue = this.autocompleteFilter[0].value;
        for (var index = 1; index < this.autocompleteFilter.length; index++) {
            emitValue = emitValue + ',' + this.autocompleteFilter[index].value;
        }
        this.changeFilter('terms', emitValue, true);
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Output"])(),
        __metadata("design:type", _angular_core__WEBPACK_IMPORTED_MODULE_0__["EventEmitter"])
    ], FiltersService.prototype, "paramsChanged", void 0);
    FiltersService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])(),
        __metadata("design:paramtypes", [])
    ], FiltersService);
    return FiltersService;
}());

var AutocompleteFilter = /** @class */ (function () {
    function AutocompleteFilter(name, value) {
        this.name = name;
        this.value = value;
    }
    return AutocompleteFilter;
}());



/***/ }),

/***/ "./src/irokoui/filters/select-autocomplete-filter/select-autocomplete-filter.component.html":
/*!**************************************************************************************************!*\
  !*** ./src/irokoui/filters/select-autocomplete-filter/select-autocomplete-filter.component.html ***!
  \**************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"card-filter\" >\n  <mat-form-field style=\"width: 100%;\">\n    \n    <input type=\"text\" placeholder=\"{{placeholder}}\" aria-label=\"Number\" matInput [formControl]=\"myControl\" [matAutocomplete]=\"auto\" id=\"{{inputId}}\">\n    <mat-autocomplete #auto=\"matAutocomplete\" >\n      <mat-option *ngFor=\"let option of filteredOptions | async\" [value]=\"option.name\" (click)=\"addChips(option)\" title=\"{{option.value}}\">\n        {{option.name}}\n      </mat-option>\n    </mat-autocomplete>\n\n    <button mat-icon-button color=\"accent\" class=\"delete-filter\" (click)=\"remove_component()\">\n      <mat-icon>close</mat-icon>\n    </button>\n  </mat-form-field>\n  <mat-chip-list fxLayout=\"row\" fxLayoutAlign=\"start center\" style=\"margin-bottom: .5em\" id=\"chiplist\">\n    <mat-chip *ngFor=\"let item of chipsList; let i=index\" (click)=\"removeChip(i)\">{{item.name}}</mat-chip>\n  </mat-chip-list>\n</div>"

/***/ }),

/***/ "./src/irokoui/filters/select-autocomplete-filter/select-autocomplete-filter.component.scss":
/*!**************************************************************************************************!*\
  !*** ./src/irokoui/filters/select-autocomplete-filter/select-autocomplete-filter.component.scss ***!
  \**************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".card-filter {\n  border: 2px solid #e4e4e4;\n  border-radius: 5px;\n  padding: 0 .5em;\n  padding-top: 5px;\n  position: relative;\n  box-shadow: 2px 3px 10px RGB(0, 0, 0, 0.053);\n  width: 15em;\n  margin: .4em 0; }\n\n.delete-filter {\n  position: absolute;\n  top: -1.9em;\n  right: -1.4em;\n  width: 2em;\n  height: 2em; }\n\n.delete-filter mat-icon {\n    font-size: medium; }\n\n.mat-option {\n  line-height: 35px;\n  font-size: 20px;\n  height: 35px; }\n\n#mat-chip-list-0 > .mat-chip-list-wrapper {\n  max-height: 6em;\n  overflow: auto; }\n\nmat-chip {\n  cursor: pointer; }\n"

/***/ }),

/***/ "./src/irokoui/filters/select-autocomplete-filter/select-autocomplete-filter.component.ts":
/*!************************************************************************************************!*\
  !*** ./src/irokoui/filters/select-autocomplete-filter/select-autocomplete-filter.component.ts ***!
  \************************************************************************************************/
/*! exports provided: SelectAutocompleteFilterComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SelectAutocompleteFilterComponent", function() { return SelectAutocompleteFilterComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _filters_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../filters.service */ "./src/irokoui/filters/filters.service.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _filter_container_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../filter-container.service */ "./src/irokoui/filters/filter-container.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};





var SelectAutocompleteFilterComponent = /** @class */ (function () {
    function SelectAutocompleteFilterComponent(filterService, filterContainerService) {
        this.filterService = filterService;
        this.filterContainerService = filterContainerService;
        this.type = '';
        this.placeholder = '';
        this.text = '';
        this.multiple = false;
        this.selectOptions = [];
        this.myControl = new _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormControl"]();
        this.chipsList = [];
    }
    SelectAutocompleteFilterComponent.prototype.ngOnInit = function () {
        var _this = this;
        if (this.data.type)
            this.type = this.data.type;
        if (this.data.placeholder)
            this.placeholder = this.data.placeholder;
        if (this.multiple)
            this.multiple = true;
        if (this.data.selectOptions)
            this.selectOptions = this.data.selectOptions;
        this.data.value = '';
        this.filteredOptions = this.myControl.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["startWith"])(''), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(function (value) { return _this._filter(value); }));
        this.inputId = this.placeholder.trim().toLowerCase();
    };
    SelectAutocompleteFilterComponent.prototype._filter = function (value) {
        var filterValue = value.toLowerCase();
        return this.selectOptions.filter(function (option) { return option.name.toLowerCase().includes(filterValue); });
    };
    SelectAutocompleteFilterComponent.prototype.remove_component = function () {
        this.filterService.deleteParameter(this.data.field);
        this.filterContainerService.filterDeleted(this.data.index);
    };
    SelectAutocompleteFilterComponent.prototype.optionSelect = function () {
        var valueEmiter = 'OR';
        this.chipsList.forEach(function (chip) {
            valueEmiter = valueEmiter + ',' + chip.id;
        });
        this.filterService.changeAutocompleteFilter(this.data.idVocab, valueEmiter);
    };
    SelectAutocompleteFilterComponent.prototype.addChips = function (value) {
        var _this = this;
        this.chipsList.unshift(value);
        this.myControl.setValue('');
        this.filteredOptions = this.myControl.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["startWith"])(''), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(function (value) { return _this._filter(value); }));
        document.getElementById(this.inputId).blur();
        this.optionSelect();
    };
    SelectAutocompleteFilterComponent.prototype.removeChip = function (index) {
        this.chipsList.splice(index, 1);
        this.optionSelect();
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", Object)
    ], SelectAutocompleteFilterComponent.prototype, "data", void 0);
    SelectAutocompleteFilterComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-select-autocomplete-filter',
            template: __webpack_require__(/*! ./select-autocomplete-filter.component.html */ "./src/irokoui/filters/select-autocomplete-filter/select-autocomplete-filter.component.html"),
            styles: [__webpack_require__(/*! ./select-autocomplete-filter.component.scss */ "./src/irokoui/filters/select-autocomplete-filter/select-autocomplete-filter.component.scss")]
        }),
        __metadata("design:paramtypes", [_filters_service__WEBPACK_IMPORTED_MODULE_1__["FiltersService"],
            _filter_container_service__WEBPACK_IMPORTED_MODULE_4__["FilterContainerService"]])
    ], SelectAutocompleteFilterComponent);
    return SelectAutocompleteFilterComponent;
}());



/***/ }),

/***/ "./src/irokoui/filters/select-filter/select-filter.component.html":
/*!************************************************************************!*\
  !*** ./src/irokoui/filters/select-filter/select-filter.component.html ***!
  \************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<mat-form-field class=\"card-filter\">\n\n  <ng-container *ngIf=\"multiple; else elseTemplate\">\n    <mat-select placeholder=\"{{placeholder}}\" [(ngModel)]=\"selectValue\" multiple>\n        <mat-option *ngFor=\"let topping of toppingList\" [value]=\"topping\" (click)=\"optionSelect()\">{{topping}}</mat-option>\n      </mat-select>\n  </ng-container>\n  <ng-template #elseTemplate>\n    <mat-select placeholder=\"{{placeholder}}\" [(ngModel)]=\"selectValue\">\n        <mat-option *ngFor=\"let topping of toppingList\" [value]=\"topping\" (click)=\"optionSelect()\">{{topping}}</mat-option>\n      </mat-select>\n  </ng-template>\n\n  <button mat-icon-button color=\"accent\" class=\"delete-filter\" (click)=\"remove_component()\">\n    <mat-icon>close</mat-icon>\n  </button>\n</mat-form-field>"

/***/ }),

/***/ "./src/irokoui/filters/select-filter/select-filter.component.scss":
/*!************************************************************************!*\
  !*** ./src/irokoui/filters/select-filter/select-filter.component.scss ***!
  \************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".card-filter {\n  border: 2px solid #e4e4e4;\n  border-radius: 5px;\n  padding: 0 .5em;\n  padding-top: 5px;\n  position: relative;\n  box-shadow: 2px 3px 10px RGB(0, 0, 0, 0.053);\n  width: 15em;\n  margin: .4em 0; }\n\n.delete-filter {\n  position: absolute;\n  top: -1.9em;\n  right: -1.4em;\n  width: 2em;\n  height: 2em; }\n\n.delete-filter mat-icon {\n    font-size: medium; }\n"

/***/ }),

/***/ "./src/irokoui/filters/select-filter/select-filter.component.ts":
/*!**********************************************************************!*\
  !*** ./src/irokoui/filters/select-filter/select-filter.component.ts ***!
  \**********************************************************************/
/*! exports provided: SelectFilterComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SelectFilterComponent", function() { return SelectFilterComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _filters_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../filters.service */ "./src/irokoui/filters/filters.service.ts");
/* harmony import */ var _filter_container_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../filter-container.service */ "./src/irokoui/filters/filter-container.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var SelectFilterComponent = /** @class */ (function () {
    function SelectFilterComponent(filterService, filterContainerService) {
        this.filterService = filterService;
        this.filterContainerService = filterContainerService;
        this.type = '';
        this.placeholder = '';
        this.text = '';
        this.multiple = false;
        this.selectOptions = [''];
    }
    SelectFilterComponent.prototype.ngOnInit = function () {
        if (this.data.type)
            this.type = this.data.type;
        if (this.data.placeholder)
            this.placeholder = this.data.placeholder;
        if (this.multiple)
            this.multiple = true;
        if (this.data.selectOptions)
            this.selectOptions = this.data.selectOptions;
        this.data.value = '';
    };
    SelectFilterComponent.prototype.remove_component = function () {
        this.filterService.deleteParameter(this.data.field);
        this.filterContainerService.filterDeleted(this.data.index);
    };
    SelectFilterComponent.prototype.optionSelect = function () {
        if (this.multiple) {
            //adaptar el value
        }
        this.filterService.changeFilter(this.data.field, this.data.value);
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", Object)
    ], SelectFilterComponent.prototype, "data", void 0);
    SelectFilterComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-select-filter',
            template: __webpack_require__(/*! ./select-filter.component.html */ "./src/irokoui/filters/select-filter/select-filter.component.html"),
            styles: [__webpack_require__(/*! ./select-filter.component.scss */ "./src/irokoui/filters/select-filter/select-filter.component.scss")]
        }),
        __metadata("design:paramtypes", [_filters_service__WEBPACK_IMPORTED_MODULE_1__["FiltersService"],
            _filter_container_service__WEBPACK_IMPORTED_MODULE_2__["FilterContainerService"]])
    ], SelectFilterComponent);
    return SelectFilterComponent;
}());



/***/ }),

/***/ "./src/irokoui/filters/title-filter/title-filter.component.html":
/*!**********************************************************************!*\
  !*** ./src/irokoui/filters/title-filter/title-filter.component.html ***!
  \**********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<mat-form-field class=\"card-filter\">\n  <input matInput type=\"{{type}}\" placeholder=\"{{placeholder}}\" [(ngModel)]=\"data.value\" required (keyup)=\"onChange()\">\n  <button mat-icon-button color=\"accent\" class=\"delete-filter\" (click)=\"remove_component()\">\n    <mat-icon>close</mat-icon>\n  </button>\n</mat-form-field>\n"

/***/ }),

/***/ "./src/irokoui/filters/title-filter/title-filter.component.scss":
/*!**********************************************************************!*\
  !*** ./src/irokoui/filters/title-filter/title-filter.component.scss ***!
  \**********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".card-filter {\n  border: 2px solid #e4e4e4;\n  border-radius: 5px;\n  padding: 0 .5em;\n  padding-top: 5px;\n  position: relative;\n  box-shadow: 2px 3px 10px RGB(0, 0, 0, 0.053);\n  width: 15em;\n  margin: .4em 0; }\n\n.delete-filter {\n  position: absolute;\n  top: -1.9em;\n  right: -1.4em;\n  width: 2em;\n  height: 2em; }\n\n.delete-filter mat-icon {\n    font-size: medium; }\n"

/***/ }),

/***/ "./src/irokoui/filters/title-filter/title-filter.component.ts":
/*!********************************************************************!*\
  !*** ./src/irokoui/filters/title-filter/title-filter.component.ts ***!
  \********************************************************************/
/*! exports provided: TitleFilterComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TitleFilterComponent", function() { return TitleFilterComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _filters_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../filters.service */ "./src/irokoui/filters/filters.service.ts");
/* harmony import */ var _filter_container_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../filter-container.service */ "./src/irokoui/filters/filter-container.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var TitleFilterComponent = /** @class */ (function () {
    function TitleFilterComponent(filterService, filterContainerService) {
        this.filterService = filterService;
        this.filterContainerService = filterContainerService;
    }
    TitleFilterComponent.prototype.ngOnInit = function () {
        this.type = this.data.type;
        this.placeholder = this.data.placeholder;
        this.data.value = '';
    };
    TitleFilterComponent.prototype.remove_component = function () {
        this.filterService.deleteParameter(this.data.field);
        this.filterContainerService.filterDeleted(this.data.index);
    };
    TitleFilterComponent.prototype.onChange = function () {
        this.filterService.changeFilter(this.data.field, this.data.value);
    };
    __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Input"])(),
        __metadata("design:type", Object)
    ], TitleFilterComponent.prototype, "data", void 0);
    TitleFilterComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'toco-title-filter',
            template: __webpack_require__(/*! ./title-filter.component.html */ "./src/irokoui/filters/title-filter/title-filter.component.html"),
            styles: [__webpack_require__(/*! ./title-filter.component.scss */ "./src/irokoui/filters/title-filter/title-filter.component.scss")]
        }),
        __metadata("design:paramtypes", [_filters_service__WEBPACK_IMPORTED_MODULE_1__["FiltersService"],
            _filter_container_service__WEBPACK_IMPORTED_MODULE_2__["FilterContainerService"]])
    ], TitleFilterComponent);
    return TitleFilterComponent;
}());



/***/ })

}]);
//# sourceMappingURL=irokoui-catalog-catalog-module.js.map