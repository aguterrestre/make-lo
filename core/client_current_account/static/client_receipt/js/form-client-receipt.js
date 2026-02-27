// Ver https://es.stackoverflow.com/questions/314935/datatables-jquery-obtener-fila-seleccionada-por-un-checkbox

let tableReceipt;
var receipt = {
    items: {
        client: 1,
        date_joined: '',
        total: 0.0000,
        balance: 0.0000,
        tickets: [],
        letter: 'c',  // Letra C
        center: 1,  // Puesto comun
        number: 1  // Numero 1
    },
    calculateTotal: function () {
        let total = 0.0000
        $.each(this.items.tickets, function (pos, dict) {
            total += dict.balance
        })
        this.items.total = total

        $('input[name="total"]').val(this.items.total.toFixed(4));
    },
    add: function (item) {
        // agregamos a la estructura el/los ticket elegido
        this.items.tickets.push(item);
    },
    list: function (clientId) {
        // this.calculate_ticket()
        tableReceipt = $('#table_client_receipt').DataTable({
            responsive: true,
            autoWidth: false,
            "language": {
              "sEmptyTable": "Ningún dato disponible en esta tabla",
              "sLoadingRecords": "Cargando...",
              "sZeroRecords":    "No se encontraron resultados",
            }, // agregamos el idioma aquí ya que se recarga el DataTable en este codigo y pierde el idioma cargado en el template
            destroy: true,
            // data: this.items.products,
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            ajax: {
                url: window.location.pathname,
                // headers: {'X-CSRFToken': '{{ csrf_token }}'},
                type: 'POST',
                data: {
                    'action': 'search_ticket_current_account',
                    'client_id': clientId,
                },
                dataSrc: ""
            },
            columns: [
                {"data": "ticket.id"},
                {"data": "ticket.id"},
                {"data": "ticket.ticket_number"},
                {"data": "ticket.date_joined"},
                {"data": "balance"},
                {"data": "ticket.total"},
            ],
            columnDefs: [
              {
                  targets: [0], // columna checkbox
                  class: 'text-center',
                  orderable: false,
                  render: function (data, type, row) {
                      return '<input type="checkbox" value="'+ data +'" id="selected_ticket">';
                  }
              },
              {
                  targets: [1], // columna código
                  class: 'text-center',
                  orderable: false,
              },
              {
                  targets: [2], // columna comprobante
                  class: 'text-center',
                  orderable: false,
              },
              {
                  targets: [3], // columna fecha
                  class: 'text-center',
                  orderable: false,
              },
              {
                  targets: [4], // columna balance
                  class: 'text-center',
                  orderable: false,
                  render: function (data, type, row) {
                      return '<input type="text" name="balance" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.balance + '">';
                  }
              },
              {
                  targets: [5], // columna total
                  class: 'text-center',
                  orderable: false,
                  render: function (data, type, row) {
                      return '$' + parseFloat(data).toFixed(4);
                  }
              }
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="balance"]').TouchSpin({
                    min: 0.000,
                    max: 1000000,
                    step: 1,
                    forcestepdivisibility: 'none',
                    decimals: 4,
                    prefix: '$'
                });
            },
        });
    }
};

$(function () {

    // fecha de registro del recibo
    $('#date_joined').datetimepicker({
      format: 'YYYY-MM-DD',
      date: moment().format("YYYY-MM-DD"),
      locale: 'es',
      minDate: moment().format("YYYY-MM-DD")
    });

    // eventos de la tabla que contiene los comprobantes adeudados
    $('#table_client_receipt tbody')
    .on('change', 'input[name="balance"]', function () {
        // Actualizamos el balance del ticket en la estructura de datos
        let balance = parseFloat($(this).val());
        var tr = tableReceipt.cell($(this).closest('td, li')).index();
        receipt.items.tickets[tr.row].balance = balance;
        receipt.calculateTotal();
    })
    .on('change', 'input[type=checkbox]', function () {
        // Actualizamos el balance del ticket en la estructura de datos
    });

    // evento submit del boton guardar
    $('form').on('submit', function (e) {
        // Cancela evento por defecto
        e.preventDefault();

        // mostramos mjs informando que debe ingresar un total
        if ($('input[name="total"]').val() <= 0) {
            const text_mjs = "Debe ingresar un total para continuar."
            Swal.fire({
              title: 'Oops...!',
              text: text_mjs,
              icon: 'warning',
              confirmButtonColor: '#28a745',
              confirmButtonText: 'Aceptar'
            })
            return false;
        };

        // mostramos mjs informando al usuario que registrará un recibo a cuenta
        // **** Falta controlar cuando queda un monto del recibo sin afectar, sería una parte a cuenta ****
        if (receipt.items.tickets.length === 0) {
            const text_mjs = "No ha seleccionado ningún comprobante a pagar. El recibo será registrado en la cuenta del cliente."
            Swal.fire({
              title: 'Información',
              text: text_mjs,
              icon: 'info',
              confirmButtonColor: '#28a745',
              confirmButtonText: 'Continuar'
            })
        };

        // Completamos estructura de datos para enviar a la vista
        receipt.items.client = $('select[name="client"]').val();
        receipt.items.total = $('input[name="total"]').val();
        receipt.items.letter = $('input[name="letter"]').val();
        receipt.items.center = $('input[name="center"]').val();
        receipt.items.number = $('input[name="number"]').val();
        receipt.items.date_joined = $('input[name="date_joined"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('receipt', JSON.stringify(receipt.items));
        submit_with_ajax(window.location.pathname, 'Registrar Recibo', '¿Estas seguro de registrar el recibo de venta?',
         parameters, function (response) {
           alert_action_ticket('Visualizar PDF', '¿Desea ver el recibo en formato PDF?', function () {
              window.open('/client_current_account/receipt/pdf/' + response.id + '/', '_blank');
              location.href = '/client_current_account/receipt/list/';
            }, function () {
                location.href = '/client_current_account/receipt/list/';
          });
        });
    });

    // buscador de clientes
    $('select[name="client"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            // headers: "{'X-CSRFToken': '{{ csrf_token }}'}",
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_clients'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese un nombre de cliente...',
        minimumInputLength: 3,
    }).on('select2:select', function (e) {
        // obtenemos el id del cliente seleccionado
        let client = e.params.data.id
        // listamos los comprobantes adeudados
        receipt.list(client);
    });

    // total del recibo al iniciar
    $('input[name="total"]').TouchSpin({
        min: 0.0000,
        max: 1000000,
        step: 1,
        forcestepdivisibility: 'none',
        decimals: 4,
        prefix: '$'
    }).val('0.0000');

    // boton de seleccion para toda la columna de la tabla
    selected = true; // Creamos una variable bandera
    $('#selected_all').click(function() {
      if (selected) {
        $('#table_client_receipt input[type=checkbox]').prop("checked", true);
      } else {
        $('#table_client_receipt input[type=checkbox]').prop("checked", false);
      }
      selected = !selected;
      addTicket()
    });

    // agrega los tickets seleccionados a estructura de procesamiento
    function addTicket() {
    };

    // hacemos foco en el buscador de clientes
    document.getElementById("client").focus();

});
