var tableTicketList;

$(function () {

    tableTicketList = $('#table_id').DataTable({
        responsive: true,
        autoWidth: false,
        "language": {
          "sProcessing":     "Procesando...",
                        "sLengthMenu":     "Mostrar _MENU_ registros",
                        "sZeroRecords":    "No se encontraron resultados",
                        "sEmptyTable":     "Ningún dato disponible en esta tabla",
                        "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                        "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
                        "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
                        "sInfoPostFix":    "",
                        "sSearch":         "Buscar:",
                        "sUrl":            "",
                        "sInfoThousands":  ",",
                        "sLoadingRecords": "Cargando...",
                        "oPaginate": {
                            "sFirst":    "Primero",
                            "sLast":     "Último",
                            "sNext":     "Siguiente",
                            "sPrevious": "Anterior"
                        },
                        "oAria": {
                            "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
                            "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                        },
                        "buttons": {
                            "copy": "Copiar",
                            "colvis": "Visibilidad"
                        }
        }, // agregamos el idioma aquí ya que se recarga el DataTable en este codigo y pierde el idioma cargado en el template
        "lengthMenu": [ 5, 10, 15, 20 ], // lo mismo que el lenguaje
        destroy: true,
        deferRender: true,
        order: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "client.full_name"},
            {"data": "ticket_number"},
            {"data": "date_joined"},
            {"data": "validated"},
            {"data": "total"},
            {"data": "options"},
        ],
        columnDefs: [
            {
                targets: [4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let validate = ''
                    if (data == 'A') {
                        validate = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
                    } else if (data == 'R') {
                        validate = '<img src="/static/admin/img/icon-no.svg" alt="True">'
                    }
                    return validate;
                }
            },
            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(4);
                }
            },
            {
                targets: [6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="ticket_detail" class="btn btn-success btn-xs btn-flat" style="color: white;"><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/sale/ticket/pdf/add/'+row.id+'/" target="_blank" class="btn btn-success btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    if (row.validated == 'R') {
                        buttons += '<a rel="ticket_validated_afip" class="btn btn-success btn-xs btn-flat" style="color: white;"><i class="fas fa-sync-alt"></i></a> ';
                    }
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#table_id tbody')
        .on('click', 'a[rel="ticket_detail"]', function () {
            var tr = tableTicketList.cell($(this).closest('td, li')).index();
            var data = tableTicketList.row(tr.row).data();
            $('#table_ticket_detail').DataTable({
                responsive: true,
                autoWidth: false,
                "language": {
                  "sProcessing":     "Procesando...",
                                "sLengthMenu":     "Mostrar _MENU_ registros",
                                "sZeroRecords":    "No se encontraron resultados",
                                "sEmptyTable":     "Ningún dato disponible en esta tabla",
                                "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                                "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
                                "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
                                "sInfoPostFix":    "",
                                "sSearch":         "Buscar:",
                                "sUrl":            "",
                                "sInfoThousands":  ",",
                                "sLoadingRecords": "Cargando...",
                                "oPaginate": {
                                    "sFirst":    "Primero",
                                    "sLast":     "Último",
                                    "sNext":     "Siguiente",
                                    "sPrevious": "Anterior"
                                },
                                "oAria": {
                                    "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
                                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                                },
                                "buttons": {
                                    "copy": "Copiar",
                                    "colvis": "Visibilidad"
                                }
                }, // agregamos el idioma aquí ya que se recarga el DataTable en este codigo y pierde el idioma cargado en el template
                "lengthMenu": [ 5, 10, 15, 20 ], // lo mismo que el lenguaje
                destroy: true,
                deferRender: true,
                order: false, // para que respete el orden en que son elegidos desde el buscador
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "product.name"},
                    {"data": "quantity"},
                    {"data": "product.unit.name"},
                    {"data": "final_price"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [3, 4], // columna final_price, subtotal
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(4);
                        }
                    },
                    {
                        targets: [1], // columna quantity
                        class: 'text-center',
                        render: function (data, type, row) {
                            return parseFloat(data).toFixed(3);
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#modal_ticket_detail').modal('show');
        })
        .on('click', 'a[rel="ticket_validated_afip"]', function () {
            alert('Validando en AFIP')
        })
});
