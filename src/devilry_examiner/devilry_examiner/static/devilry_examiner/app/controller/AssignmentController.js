// Generated by CoffeeScript 1.6.3
(function() {
  Ext.define('devilry_examiner.controller.AssignmentController', {
    extend: 'Ext.app.Controller',
    views: ['assignment.AssignmentWorkspace'],
    stores: [],
    refs: [
      {
        ref: 'workspace',
        selector: 'viewport assignmentworkspace'
      }
    ],
    init: function() {
      return this.control({
        'viewport assignmentworkspace': {
          render: this._onRenderWorkspace
        }
      });
    },
    _onRenderWorkspace: function() {
      this.assignmentId = this.getWorkspace().assignmentId;
      return console.log('Render assignment', this.assignmentId);
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
