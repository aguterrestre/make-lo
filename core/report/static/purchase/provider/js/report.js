var date_range = null;
var date_creation_range = null;
var date_now = new moment().format('YYYY-MM-DD');
var provider_filter = 0;

function generate_report() {
    var parameters = {
        'action': 'search_report',
        'start_date': '',
        'end_date': '',
        'provider': provider_filter,
        'start_creation_date': date_now,
        'end_creation_date': date_now,
    };

    if (date_range !== null) {
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
    }

    if (date_creation_range !== null) {
        parameters['start_creation_date'] = date_creation_range.startDate.format('YYYY-MM-DD');
        parameters['end_creation_date'] = date_creation_range.endDate.format('YYYY-MM-DD');
    }

    $('#table_report').DataTable({
        responsive: true,
        autoWidth: false,
        "language": {
          "sEmptyTable": "Ningún dato disponible en esta tabla",
          "sLoadingRecords": "Cargando..."
        },
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
        order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel  <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf  <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-success btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['5%', '30%', '15%', '10%', '10%', '10%'];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        columns: [
            {"data": "id"},
            {"data": "full_name"},
            {"data": "document_type"},
            {"data": "document"},
            {"data": "date_birthday"},
            {"data": "telephone"},
        ],
        columnDefs: [
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {

    // Filtro por fecha de nacimiento del proveedor
    $('input[name="date_birthday_range"]').daterangepicker({
        buttonClasses: 'btn btn-flat',
        applyButtonClasses: 'btn-success',
        cancelButtonClasses: 'btn-secondary',
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar rango',
            cancelLabel: '<i class="fas fa-times"></i> No aplicar rango',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        date_range = picker;
        generate_report();
    }).on('cancel.daterangepicker', function (ev, picker) {
        $(this).val('Todas las fechas');
        date_range = null;
        generate_report();
    });

    // Inicializo el filtro por cumpleaños sin contenido
    $('input[name="date_birthday_range"]').val('Todas las fechas');

    // Filtro por fecha de creación del proveedor
    $('input[name="date_creation_range"]').daterangepicker({
        buttonClasses: 'btn btn-flat',
        applyButtonClasses: 'btn-success',
        cancelButtonClasses: 'btn-secondary',
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar rango',
            cancelLabel: '<i class="fas fa-times"></i> No aplicar rango',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        date_creation_range = picker;
        generate_report();
    }).on('cancel.daterangepicker', function (ev, picker) {
        $(this).val('Todas las fechas');
        date_now = '';
        date_creation_range = null;
        generate_report();
    });

    // Filtro por proveedor del comprobate
    $('select[name="provider"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_provider'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Todos los proveedores',
        minimumInputLength: 3
    }).on('select2:select', function (e) {
        provider_filter = e.params.data.id;
        generate_report();
    }).on('select2:clear', function (e) {
        provider_filter = 0;
        generate_report();
    });

    // Genera el listado al inicio
    generate_report();
});
