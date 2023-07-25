var selected_genes = JSON.parse(localStorage.getItem("selected_genes")) || [];
function saveLocalChanges() {
    localStorage.setItem("selected_genes", JSON.stringify(selected_genes));
}
selected_genes.push = function() { Array.prototype.push.apply(this, arguments);  saveLocalChanges();};
selected_genes.pop = function() { Array.prototype.pop.apply(this, arguments);  saveLocalChanges();};
selected_genes.splice = function() { Array.prototype.splice.apply(this, arguments);  saveLocalChanges();};

$(document).ready(function() {
  const stateSave = true;
  lengthMenu = [
        [10, 50, 100, -1],
        [10, 50, 100, 'All']
    ]
  const genesTable = $('#genes').DataTable({
    'serverSide': true,
    'ajax':{
        'url': '/api/gene/?format=datatables',
        'data': function (d) {},
    },
    'initComplete': function(settings, json) {},
    'stateSave': stateSave,
    'dom': 'lfrtlip',
    'lengthMenu': lengthMenu,
    'order': [1],
    'columns': [
          {
            "data": null,
            "render": function( data, type, row, meta ) {
                let selected = $.inArray(row.def_name, selected_genes) !== -1;
                return '<input data-gene="'+row.def_name+'" type="checkbox" '+ (selected ? 'checked' : '') +'>';
            },
            "filtering": false,
            "width": "10%",
            "ordering": false,
            "searchable": false,
          },
          {
            "data": "icon",
            "name": "label, def_name",
            "searchable": true,
            "orderData": 1,
            "width": "15%",
            "render": function( data, type, row, meta ) {
              let klass = ''
              if (row.color) {
                klass = data.replaceAll('gene_icons/', '').replaceAll('.png', '') + ' ' + row.color
              }
              return '<img src="static/'+data+'" class="'+klass+'">' + row.label
            }
          },
          {"data": "label", "visible": false},
//          {"data": "def_name", "visible": false},
          {
            "data": "xenotype_set",
            "width": "50%",
            "searchable": true,
            "name": "xenotype_set__label",
            "orderData": 4,
            "render": function( data, type, row, meta ) {
                return $.map(row.xenotype_set, function(xeno){
                    return '<img data-xenotype="'+xeno.label+'" src="static/xenotype_icons/'+xeno.label+'.png" data-bs-toggle="tooltip" title="'+xeno.label+'">'
                }).join(" ")
            },
            "filter": function() {
            }
          },
          {"data": "xenotype_count", "name": "xenotype_count", "visible": false},
          {
            "data": "category",
            "name": "category",
            "visible": true,
            "searchable": true,
          },
          {
            "data": "is_cosmetic",
            "name": "is_cosmetic",
            "visible": false,
            "searchable": true,
            "orderable": false,
          },
          {
            "data": "trader_only",
            "name": "trader_only",
            "visible": false,
            "searchable": true,
            "orderable": false,
          },
          {
            "data": "def_name",
            "name": "def_name",
            "visible": false,
            "searchable": false,
            "orderable": false,
          },
      ],

  });
  const xenotypesTable = $('#xenotypes').DataTable({
    'serverSide': true,
    'ajax':'/api/xenotype/?format=datatables',
    'stateSave': stateSave,
    'order': [1],
    'dom': 'frt',
    'columns': [
        {
            "data": "gene_set",
            "searchable": true,
            "name": "gene_set__label",
            "className": 'inactive_genes',
            "orderData": 3,
            "width": "45%",
            "render": function( data, type, row, meta ) {
                return $.map(data, function(item) {
                    let selected = $.inArray(item.def_name, selected_genes) !== -1;
                    let klass = item.color ?  item.icon.replaceAll('gene_icons/', '').replaceAll('.png', '') + ' ' + item.color : ''
                    klass = item.category == 'COSMETIC' ? klass + ' cosmetic' : klass
                    klass = selected ? klass + ' active' : klass + ' inactive'
                    return '<img data-gene="'+item.def_name+'" src="static/'+item.icon+'" class="'+klass+'" data-bs-toggle="tooltip" title="'+item.label+'">'
                }).join(" ")
            },
        },
        {
            "data": "label",
            "width": "10%",
            "render": function( data, type, row, meta ) {
                return '<img data-xenotype="'+data+'" src="static/xenotype_icons/'+data+'.png" data-bs-toggle="tooltip" title="'+data+'">'
            },
        },
        {
            "data": "gene_set",
            "className": 'active_genes',
            "searchable": true,
            "name": "gene_set__label",
            "orderData": 4,
            "width": "45%",
            "render": function( data, type, row, meta ) {
                return $.map(data, function(item) {
                    let selected = $.inArray(item.def_name, selected_genes) !== -1;
                    let klass = item.color ?  item.icon.replaceAll('gene_icons/', '').replaceAll('.png', '') + ' ' + item.color : ''
                    klass = item.category == 'COSMETIC' ? klass + ' cosmetic' : klass
                    klass = selected ? klass + ' active' : klass + ' inactive'
                    return '<img data-gene="'+item.def_name+'" src="static/'+item.icon+'" class="'+klass+'" data-bs-toggle="tooltip" title="'+item.label+'">'
                }).join(" ")
            },
        },
        {"data": "gene_count", "name": "gene_count", "visible": false, "searchable": false},
      ],

  });

  console.log(genesTable)
  console.log(xenotypesTable)

  function refreshTableSpecificElements() {
    if ($('table#genes').is(':visible')) {
        $('.gene-table-only-element input').prop('disabled', false)
    } else {
        $('.gene-table-only-element input').prop('disabled', true)
    }
    if ($('table#xenotypes').is(':visible')) {
        $('.xenotype-table-only-element input').prop('disabled', false)
    } else {
        $('.xenotype-table-only-element input').prop('disabled', true)
    }
  }
  refreshTableSpecificElements();

  $(document).on('shown.bs.tab', function (e) {
    genesTable.columns.adjust();
    xenotypesTable.columns.adjust();
    refreshTableSpecificElements();
  });

  $(document).on('show.bs.tab', function (e) {
    genesTable.draw();
    xenotypesTable.draw();
  });

  $('body').tooltip({
    selector: 'img[data-bs-toggle]'
  });

  var show_cosmetic = $('#showCosmetic').is(':checked');
  $('table#xenotypes').toggleClass('hide-cosmetic', !show_cosmetic)
  genesTable.column(6).search(show_cosmetic ? '' : 0).draw()

  var show_trader_only = $('#showTraderOnlyGenes').is(':checked');
  genesTable.column(7).search(show_trader_only ? '' : 0).draw()

  $('#showCosmetic').on('change', function(e) {
    show_cosmetic = $('#showCosmetic').is(':checked');
    $('table#xenotypes').toggleClass('hide-cosmetic', !show_cosmetic)
    genesTable.column(6).search(show_cosmetic ? '' : 0)
    if ($('table#genes').is(':visible')) {
        genesTable.draw()
    }
  })

  $('#showTraderOnlyGenes').on('change', function(e) {
    show_trader_only = $('#showTraderOnlyGenes').is(':checked');
    genesTable.column(7).search(show_trader_only ? '' : 0)
    if ($('table#genes').is(':visible')) {genesTable.draw()}
  })

  $('table#genes').on('change', 'input[type="checkbox"]', function(e){
    let gene = $(this).data('gene');
    let checked = $(this).is(':checked');
    if (checked) {
        selected_genes.push(gene);
    } else {
        selected_genes.pop(gene);
    }
  })

  $('table#xenotypes').on('click', 'img[data-gene]', function(e){
    let gene = $(this).data('gene');
    let selected = $.inArray(gene, selected_genes) !== -1;
    if (selected) {
        selected_genes.splice(selected_genes.indexOf(gene), 1);
    } else {
        selected_genes.push(gene);
    }
    $(".tooltip").tooltip("hide");
    xenotypesTable.draw();
  });

  $('table#xenotypes').on('click', 'img[data-xenotype]', function(e){
    console.log(this)
    let xenotype_name = $(this).data('xenotype');
    let icon_url = $(this).attr('src');
    $('#xenotype_modal_genes_list').html('')
    $('#xenotype_modal_cosmetic_genes_list').html('')
    let $img_elements = $(this).closest('tr').find('td.active_genes img:not(.cosmetic)')
    let $cosmetic_img_elements = $(this).closest('tr').find('td.active_genes img.cosmetic')

    console.log('$img_elements', $img_elements);
    console.log('$cosmetic_img_elements', $cosmetic_img_elements);

    $img_elements.each(function(){
        $('#xenotype_modal_genes_list').append($.clone(this))
    })
    $cosmetic_img_elements.each(function(){
        $('#xenotype_modal_cosmetic_genes_list').append($.clone(this))
    })
    $('#xenotypeModal .xenotype_icon').attr('src', icon_url)
    $('#xenotypeModal .xenotype_name').text(xenotype_name)
    $('#xenotypeModal').data('xenotype', xenotype_name)  // used when clicking confirm buttons
    $('#xenotypeModal').modal('show');
  });

    $('#all_missing_button').on('click', function(e) {
        let xenotype = $('#xenotypeModal').data('xenotype');
        let $tr = $('table#xenotypes td img[data-xenotype="'+xenotype+'"]').closest('tr');
        let xenotype_genes = $.map($tr.find('td.active_genes img'), function(x){ return $(x).data('gene')})
        for (gene of xenotype_genes) {
            let selected = $.inArray(gene, selected_genes) !== -1;
            if (selected) {
                selected_genes.splice(selected_genes.indexOf(gene), 1);
            }
        }
        xenotypesTable.draw();
        $('#xenotypeModal').modal('hide');
    })

    $('#all_found_button').on('click', function(e) {
        let xenotype = $('#xenotypeModal').data('xenotype');
        let $tr = $('table#xenotypes td img[data-xenotype="'+xenotype+'"]').closest('tr');
        let xenotype_genes = $.map($tr.find('td.active_genes img'), function(x){ return $(x).data('gene')})
        for (gene of xenotype_genes) {
            let selected = $.inArray(gene, selected_genes) !== -1;
            if (!selected) {
                selected_genes.push(gene);
            }
        }
        xenotypesTable.draw();
        $('#xenotypeModal').modal('hide');
    })

});