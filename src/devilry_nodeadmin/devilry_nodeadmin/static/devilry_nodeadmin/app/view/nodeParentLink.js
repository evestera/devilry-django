Ext.define('devilry_nodeadmin.view.nodeParentLink', {
    extend: 'Ext.view.View',
    alias: 'widget.nodeparentlink',
    cls: 'node-parent-link',
    tpl: [
        '<tpl for=".">',
        '<div class="navigator">',
            '<span>{ short_name }</span>',
            '<tpl if="predecessor">',
                '<a href="/devilry_nodeadmin/#/node/"><i class="icon-home"></i> til rotnoden</a>',
                '<a href="/devilry_nodeadmin/#/node/{ predecessor.id }"><i class="icon-chevron-up"></i> ett nivå opp</a>',
            '<tpl else>',
                '<a href="/devilry_nodeadmin/#/node/"><i class="icon-home"></i> til rotnoden</a>',
            '</tpl>',
        '</div>',
        '</tpl>',
        '<hr />'
    ],

    itemSelector: '',

    initComponent: function() {
        this.store = Ext.create( 'devilry_nodeadmin.store.NodeDetails' );
        this.store.proxy.url = Ext.String.format('/devilry_nodeadmin/rest/node/{0}/details', this.node_pk );
        this.callParent(arguments);
    }

});