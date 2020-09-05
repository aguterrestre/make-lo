var tableInvoiceForm;
var invoices = {
    items: {
        provider: 1,
        date_joined: '',
        subtotal: 0.0000,
        total_tax: 0.0000,
        total: 0.0000,
        products: []
    },
    calculate_invoice: function () {
        var subtotal = 0.0000;
        // var iva = $('input[name="iva"]').val();
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = dict.quantity * parseFloat(dict.final_price);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        // this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.subtotal; // + this.items.iva;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(4));
        // $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(4));
    },
    add: function (item) {
        this.items.products.push(item); // agregamos a la estructura el producto elegido
        this.list(); // llamamos al metodo list de esta estructura
    },
    list: function () {
        this.calculate_invoice();
        tableInvoiceForm = $('#table_invoice').DataTable({
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
            data: this.items.products,
            order: false, // para que respete el orden en que son elegidos desde el buscador
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "quantity"},
                {"data": "final_price"},
                {"data": "subtotal"},
                {"data": "options"},
            ], // las columnas que devuelve mi vista en forma de array
            columnDefs: [
              {
                  targets: [2], // columna cantidad
                  class: 'text-center',
                  orderable: false,
                  render: function (data, type, row) {
                      return '<input type="text" name="quantity" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.quantity + '">';
                  }
              },
              {
                  targets: [3, 4], // columnas precio y subtotal
                  class: 'text-center',
                  orderable: false,
                  render: function (data, type, row) {
                      return '$' + parseFloat(data).toFixed(4);
                  }
              },
              {
                    targets: [5], // columna eliminar
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
              }
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="quantity"]').TouchSpin({
                    min: 0.001,
                    max: 1000,
                    step: 1,
                    forcestepdivisibility: 'none',
                    decimals: 3
                });
            },
        });
    }
};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">' +
            '<div class="row">' +
                '<div class="col-lg-1">' +
                  '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
                '</div>' +
                '<div class="col-lg-11 text-left shadow-sm">' +
                    '<p style="margin-bottom: 0;">' +
                        '<b>Nombre:</b> ' + repo.name + '<br>' +
                        '<b>Categoría:</b> ' + repo.categ.name + '<br>' +
                        '<b>Unid. Medida:</b> ' + repo.unit.name + '<br>' +
                        '<b>Precio Final:</b> <span class="badge badge-warning">$' + repo.final_price + '</span>' +
                    '</p>' +
                '</div>' +
            '</div>' +
        '</div>');

    return option;
}

$(function () {

    // formato para plugin select2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // fecha de registro del invoice
    $('#date_joined').datetimepicker({
      format: 'YYYY-MM-DD',
      date: moment().format("YYYY-MM-DD"),
      locale: 'es',
      minDate: moment().format("YYYY-MM-DD")
    });

    // boton para eliminar todos los renglones del invoice
    $('button[name="buttonRemoveAll"]').on('click', function () {
        if (invoices.items.products.length === 0) return false;
          alert_action_remove_all('Advertencia...!', '¿Estas seguro de borrar todo el detalle de compra?',
            'El detalle de compra a sido borrado', function () {
              invoices.items.products = [];
              invoices.list();
          });
    });

    // eventos de la tabla que contiene los renglones del invoice
    $('#table_invoice tbody')
        // borrar renglon del invoice
        .on('click', 'a[rel="remove"]', function () {
            var tr = tableInvoiceForm.cell($(this).closest('td, li')).index();
              invoices.items.products.splice(tr.row, 1);
              invoices.list();
        })
        // campo cantidad de los renglones del invoice
        .on('change', 'input[name="quantity"]', function () {
            var cant = parseFloat($(this).val());
            var tr = tableInvoiceForm.cell($(this).closest('td, li')).index();
            invoices.items.products[tr.row].quantity = cant;
            invoices.calculate_invoice();
            $('td:eq(4)', tableInvoiceForm.row(tr.row).node()).html('$' + invoices.items.products[tr.row].subtotal.toFixed(4));
        });

    // evento submit del boton guardar
    $('form').on('submit', function (e) {
        e.preventDefault();

        if(invoices.items.products.length === 0){
            message_error('Debe tener al menos un item en su detalle de compra');
            return false;
        }

        invoices.items.provider = $('select[name="provider"]').val(); // obtenemos el valor ingresado en pantalla y lo guardamos en nuestra estructura
        invoices.items.date_joined = $('input[name="date_joined"]').val(); // obtenemos el valor ingresado en pantalla y lo guardamos en nuestra estructura
        var parameters = new FormData(); // creamos un objeto FormData para enviarlo a nuestra vista y guardar sus datos en el modelo
        parameters.append('action', $('input[name="action"]').val()); // le agregamos un parametro para definir la accion
        parameters.append('invoices', JSON.stringify(invoices.items)); // usamos metodo de JS para transformar un objeto js a un json string
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?',
         parameters, function (response) {
           alert_action_ticket('Notificación', '¿Desea imprimir la boleta de compra?', function () {
              window.open('/purchase/invoice/pdf/add/' + response.id + '/', '_blank');
              location.href = '/purchase/invoice/list/'; // donde va a retornar cuando termine la transacción
            }, function () {
                location.href = '/purchase/invoice/list/'; // donde va a retornar cuando termine la transacción
          });
        });
    });

    // buscador de productos
    $('select[name="search"]').select2({
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
                    action: 'search_products'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 3,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.quantity = 1;
        data.subtotal = 0.00;
        data.options = '';
        invoices.add(data);
        $(this).val('').trigger('change.select2');
    });

    // creamos la tabla vacía
    invoices.list();

});
