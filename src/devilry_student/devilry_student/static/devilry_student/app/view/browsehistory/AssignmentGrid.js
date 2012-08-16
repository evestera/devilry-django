// NOTE: This was ported from the old devilry.apps.student, so it does not follow the MVC architecture
Ext.define('devilry_student.view.browsehistory.AssignmentGrid', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.browsehistory_assignmentgrid',

    requires: [
        'devilry.apps.student.simplified.SimplifiedAssignmentGroup'
    ],

    /**
     * @cfg {Function} [urlCreateFn]
     * Function to call to genereate urls. Takes an AssignmentGroup record as parameter.
     */

    /**
     * @cfg {Object} [urlCreateFnScope]
     * Scope of ``urlCreateFn``.
     */
    
    constructor: function(config) {
        this.createStore();
        this.callParent([config]);
    },

    assignmentTpl: Ext.create('Ext.XTemplate',
        '<a href="{url}">{data.parentnode__long_name}</a>'
    ),

    pointsTpl: Ext.create('Ext.XTemplate', 
        '<span class="pointscolumn">',
        '    <tpl if="feedback">',
        '       {feedback__points}',
        '    </tpl>',
        '    <tpl if="!feedback">',
        '       <span class="nofeedback">&empty;</span>',
        '   </tpl>',
        '</span>'
    ),

    gradeTpl: Ext.create('Ext.XTemplate', 
        '<div class="gradecolumn">',
            '<tpl if="feedback">',
                '<span class="is_passing_grade">',
                    '<tpl if="feedback__is_passing_grade"><span class="passing_grade success">',
                        gettext('Passed'),
                    '</span></tpl>',
                    '<tpl if="!feedback__is_passing_grade"><span class="not_passing_grade danger">',
                        gettext('Failed'),
                    '</span></tpl>',
                    '<small>',
                        ' (<span class="grade">{feedback__grade}</span>)',
                    '</small>',
                '</span>',
                //' <small>(',
                    //'<tpl if="feedback__delivery__delivery_type == 0"><span class="electronic">Electronic</span></tpl>',
                    //'<tpl if="feedback__delivery__delivery_type == 1"><span class="non-electronic">Non-electronic</span></tpl>',
                    //'<tpl if="feedback__delivery__delivery_type == 2"><span class="neutralInlineItem">From previous period (semester)</span></tpl>',
                    //'<tpl if="feedback__delivery__delivery_type &gt; 2"><span class="warningInlineItem">Unknown delivery type</span></tpl>',
                //')</small>',
            '</tpl>',
            '<tpl if="!feedback">',
                '<small class="nofeedback">',
                    gettext('No feedback'),
                '</small>',
            '</tpl>',
        '</div>'
    ),

    createStore: function() {
        this.store = Ext.create('Ext.data.Store', {
            model: 'devilry.apps.student.simplified.SimplifiedAssignmentGroup',
            remoteFilter: true,
            remoteSort: false,
            autoSync: true
        });
        this.store.pageSize = 100000;
        //this.store.proxy.setDevilryOrderby(['parentnode__publishing_time', 'parentnode__short_name']);
    },

    loadGroupsInPeriod: function(periodRecord) {
        this.store.proxy.setDevilryFilters([{
            field: 'parentnode__parentnode',
            comp: 'exact',
            value: periodRecord.get('id')
        }])
        this.store.load({
            scope: this,
            callback: function(records, op) {
                this.getEl().unmask();
                if(records.length === 0) {
                    this.getEl().mask('You are not registered on any assignments within this period/semester. This may not be an issue if your subject/course do not have assignments, if no assignments have been published yet, or if the subject/course only use Devilry to register final results.', 'information-mask');
                }
            }
        });
    },
    
    initComponent: function() {
        var urlCreateFunction = Ext.bind(this.urlCreateFn, this.urlCreateFnScope);
        Ext.apply(this, {
            disableSelection: true,
            cls: 'bootstrap',
            columns: [{
                header: gettext('Assignment'),
                dataIndex: 'parentnode__long_name',
                flex: 4,
                sortable: false,
                menuDisabled: true,
                renderer: function(value, m, record) {
                    return this.assignmentTpl.apply({
                        data: record.data,
                        url: urlCreateFunction(record)
                    });
                }
            //}, {
                //header: 'Points', dataIndex: 'feedback__points', flex: 1,
                //renderer: function(value, m, record) {
                    //return this.pointsTpl.apply(record.data);
                //}
            }, {
                header: gettext('Grade'),
                dataIndex: 'feedback__grade',
                flex: 2,
                sortable: false,
                menuDisabled: true,
                renderer: function(value, m, record) {
                    return this.gradeTpl.apply(record.data);
                }
            }]
        });
        this.callParent(arguments);
    }
});
