// Generated by CoffeeScript 1.6.3
(function() {
  Ext.define('devilry_examiner.controller.DashboardController', {
    extend: 'Ext.app.Controller',
    views: ['dashboard.Dashboard'],
    stores: [],
    init: function() {
      return this.control({
        'viewport dashboard': {
          render: this._onRender
        }
      });
    },
    _onRender: function() {
      return console.log('Render');
    }
    /*
    _onLoadSuccess: function(records) {
        this.getAllWhereIsAdminList().update({
            loadingtext: null,
            list: this._flattenListOfActive(records)
        })
    }
    */

  });

}).call(this);
