odoo.define('menu_customization.web_custom', function (require) {
'use strict';
    var ListView = require('web.ListView');
    var FormView = require('web.FormView');
    var calenderView = require('web_calendar.CalendarView');
    var Sidebar = require('web.Sidebar');
    var FilterMenu = require('web.FilterMenu');
    var core = require('web.core');
    var _t = core._t;
    var data_manager = require('web.data_manager');
    var SearchView = require('web.SearchView');
    var CrashManager = require('web.CrashManager');
    var Dialog = require('web.Dialog');
    var QWeb = core.qweb;
    var ActionManager = require('web.ActionManager');
    var ViewManager = require('web.ViewManager');
    var Model = require('web.Model');
    var data = require('web.data');

    ListView.include({
        // hide button import
        render_buttons: function () {
            var self = this;
            this._super.apply(this, arguments);
            self.$buttons.find('.o_button_import').hide();
            return this.$buttons;
        },

        // hide action export
        render_sidebar: function ($node) {
            if (!this.sidebar && this.options.sidebar) {
                this.sidebar = new Sidebar(this, {editable: this.is_action_enabled('edit')});
                if (this.fields_view.toolbar) {
                    this.sidebar.add_toolbar(this.fields_view.toolbar);
                }
                this.sidebar.add_items('other', _.compact([{},
                    this.is_action_enabled('delete') && {label: _t('Delete'), callback: this.do_delete_selected}
                ]));

                $node = $node || this.options.$sidebar;
                this.sidebar.appendTo($node);

                // Hide the sidebar by default (it will be shown as soon as a record is selected)
                this.sidebar.do_hide();
            }
        },

        compute_aggregates: function (records) {
            var columns = _(this.aggregate_columns).filter(function (column) {
                return column['function'];
            });
            if (_.isEmpty(columns)) {
                return;
            }

            if (_.isEmpty(records)) {
                records = this.groups.get_records();
            }
            records = _(records).compact();

            var count = 0, sums = {};
            _(columns).each(function (column) {
                switch (column['function']) {
                    case 'max':
                        sums[column.id] = -Infinity;
                        break;
                    case 'min':
                        sums[column.id] = Infinity;
                        break;
                    default:
                        sums[column.id] = 0;
                }
            });
            _(records).each(function (record) {
                count += record.count || 1;
                _(columns).each(function (column) {
                    var field = column.id,
                        value = record.values[field];
                    switch (column['function']) {
                        case 'sum':
                            sums[field] += value;
                            break;
                        case 'avg':
                            sums[field] += record.count * value;
                            break;
                        case 'min':
                            if (sums[field] > value) {
                                sums[field] = value;
                            }
                            break;
                        case 'max':
                            if (sums[field] < value) {
                                sums[field] = value;
                            }
                            break;
                    }
                });
            });

            var aggregates = {};
            _(columns).each(function (column) {
                var field = column.id;
                switch (column['function']) {
                    case 'avg':
                        aggregates[field] = {value: sums[field] / count};
                        break;
                    default:
                        aggregates[field] = {value: sums[field]};
                }
            });

            this.display_aggregates(aggregates);

            // hien thi gia tri cot len listview
            var self = this;
            records = _(records).compact();
            var model = ['new.stock.history'];
            if (model.includes(this.model)) {
                var x = 1;
                var ton_dau = 0;
                var ton_cuoi = 0;
                var cell = self.$('thead');
                var cell_tfoot = self.$('tfoot');

                _(records).each(function (record1) {
                    _(self.columns).each(function (column1) {
                        if (x === 1) {
                            if (column1.id === 'ton_dau') {
                                ton_dau = record1.values[column1.id];
                            }
                            if (column1.id === 'ton_cuoi') {
                                ton_cuoi = record1.values[column1.id];
                            }
                        }
                    });
                    x += 1;
                });
                $('<tr class="text-right"><td colspan="9"><b>Tồn đầu kỳ: ' + ton_dau + '</b></td></tr>').prependTo(cell);
                $('<tr class="text-right"><td colspan="9"><b>Tồn cuối kỳ: ' + ton_cuoi + '</b></td></tr>').appendTo(cell_tfoot);
            }
        },

        // khong tinh toan lai tong gia tri khi click checkbox listview(need fix)
        do_select: function (ids, records, deselected) {
            // uncheck header hook if at least one row has been deselected
            if (deselected) {
                this.$('thead .o_list_record_selector input').prop('checked', false);
            }

            if (!ids.length) {
                this.dataset.index = 0;
                if (this.sidebar) {
                    this.sidebar.do_hide();
                }
                // this.compute_aggregates();
                return;
            }

            this.dataset.index = _(this.dataset.ids).indexOf(ids[0]);
            if (this.sidebar) {
                this.sidebar.do_show();
            }

            // this.compute_aggregates(_(records).map(function (record) {
            //     return {count: 1, values: record};
            // }));
        }
    });

    ListView.List.include({
        // disable open popup field one2many
        row_clicked: function (event) {
            if( this.view.is_action_enabled('open') ) {
                if (!this.view.editable() || !this.view.is_action_enabled('edit')) {
                    return this._super.apply(this, arguments);
                }
                if (this.__is_starting_edition) {
                    return;
                }
                this.__is_starting_edition = true;

                var self = this;
                var args = arguments;
                var _super = self._super;

                var record_id = $(event.currentTarget).data('id');
                return this.view.start_edition(
                    ((record_id) ? this.records.get(record_id) : null), {
                        focus_field: $(event.target).not(".o_readonly").data('field')
                    }).fail(function () {
                    return _super.apply(self, args); // The record can't be edited so open it in a modal (use-case: readonly mode)
                }).always(function () {
                    self.__is_starting_edition = false;
                });
            }
        }
    });

    FormView.include({
        // hide button update translate
        display_translation_alert: function() {
        }
    });

    calenderView.include({
        // disable quick create in calender view
        open_quick_create: function(){
            var calendar_models = ['equipment.plan'];
            if (!(calendar_models.includes(this.model))) {
                this._super();
            }
        }
    });

    SearchView.include({
        // add attrs disable menu to hide button Filters or Groupby
        willStart: function () {
            var self = this;
            var disable_menu = this.fields_view.arch.attrs.disable_menu;
            disable_menu = disable_menu ? disable_menu.split(',') : [];
            _.each(disable_menu, function (menu) {
                self.options['disable_' + menu] = true;
            });
            return $.when(this._super());
        }
    });

    // remove string Odoo in error dialog
    CrashManager.include({
        show_warning: function(error) {
            if (!this.active) {
                return;
            }
            new Dialog(this, {
                size: 'medium',
                title: (_.str.capitalize(error.type) || _t("Warning")),
                $content: $('<div>').html(QWeb.render('CrashManager.warning', {error: error}))
            }).open();
        },
        show_error: function(error) {
            if (!this.active) {
                return;
            }
            new Dialog(this, {
                title: _.str.capitalize(error.type),
                $content: QWeb.render('CrashManager.error', {error: error})
            }).open();
        }
    });
});
