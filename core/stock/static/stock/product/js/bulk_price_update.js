var tableProducts;
var currentProducts = [];

function getFilters() {
    return {
        'action': 'search_products',
        'product': $('select[name="product"]').val() || '',
        'category': $('select[name="category"]').val() || '',
        'unit': $('select[name="unit"]').val() || '',
        'stock': $('select[name="stock"]').val() || '0',
        'update_type': $('select[name="update_type"]').val(),
        'update_value': $('input[name="update_value"]').val() || ''
    };
}

function searchProducts() {
    var params = getFilters();
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: params,
        dataType: 'json',
        success: function (data) {
            if (data.error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: data.error,
                    confirmButtonColor: '#007bff',
                    confirmButtonText: 'OK'
                });
                return;
            }
            currentProducts = data;
            renderTable(data);
            if (data.length > 0) {
                $('#apply_section').show();
            } else {
                $('#apply_section').hide();
            }
        },
        error: function (xhr) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Ocurrió un error al buscar productos.',
                confirmButtonColor: '#007bff',
                confirmButtonText: 'OK'
            });
        }
    });
}

function renderTable(data) {
    if (tableProducts) {
        tableProducts.destroy();
    }
    var tbody = $('#table_products tbody');
    tbody.empty();
    $.each(data, function (i, item) {
        var row = '<tr>' +
            '<td>' + item.id + '</td>' +
            '<td>' + item.name + '</td>' +
            '<td>' + parseFloat(item.final_price).toFixed(4) + '</td>' +
            '<td><strong>' + parseFloat(item.new_price || item.final_price).toFixed(4) + '</strong></td>' +
            '<td>' + (item.unit ? item.unit.name || item.unit.abbreviation || '-' : '-') + '</td>' +
            '</tr>';
        tbody.append(row);
    });
    tableProducts = $('#table_products').DataTable({
        responsive: true,
        autoWidth: false,
        "language": {
            "url": typeof DATATABLES_LANG_URL !== 'undefined' ? DATATABLES_LANG_URL : '',
            "sEmptyTable": "No hay productos con los filtros seleccionados."
        },
        "lengthMenu": [10, 25, 50, 100],
        "pageLength": 25,
        order: [[1, 'asc']]
    });
}

function applyUpdate() {
    var params = getFilters();
    var updateValue = $('input[name="update_value"]').val();
    if (!updateValue) {
        Swal.fire({
            icon: 'warning',
            title: 'Atención',
            text: 'Debe ingresar un valor de actualización.',
            confirmButtonColor: '#007bff',
            confirmButtonText: 'OK'
        });
        return;
    }
    if (currentProducts.length === 0) {
        Swal.fire({
            icon: 'warning',
            title: 'Atención',
            text: 'No hay productos para actualizar.',
            confirmButtonColor: '#007bff',
            confirmButtonText: 'OK'
        });
        return;
    }
    var productIds = currentProducts.map(function (p) { return p.id; });
    Swal.fire({
        title: 'Confirmar actualización',
        text: '¿Está seguro de actualizar el precio de ' + currentProducts.length + ' producto(s)? Esta acción no se puede deshacer.',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#007bff',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Aplicar',
        cancelButtonText: 'Cancelar'
    }).then(function (result) {
        if (result.value) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'apply_update',
                    'product_ids[]': productIds,
                    'update_type': params.update_type,
                    'update_value': params.update_value
                },
                dataType: 'json',
                success: function (data) {
                    if (data.error) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: data.error,
                            confirmButtonColor: '#007bff',
                            confirmButtonText: 'OK'
                        });
                    } else {
                        $('input[name="update_value"]').val('');
                        Swal.fire({
                            icon: 'success',
                            title: 'Éxito',
                            text: data.message,
                            confirmButtonColor: '#007bff',
                            confirmButtonText: 'OK'
                        }).then(function () {
                            searchProducts();
                        });
                    }
                },
                error: function () {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Ocurrió un error al aplicar los cambios.',
                        confirmButtonColor: '#007bff',
                        confirmButtonText: 'OK'
                    });
                }
            });
        }
    });
}

var searchDebounceTimer;

function scheduleSearch() {
    if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(searchProducts, 300);
}

$(function () {
    $('select[name="category"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true
    }).on('change', scheduleSearch);
    $('select[name="unit"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true
    }).on('change', scheduleSearch);
    $('select[name="stock"]').select2({
        theme: "bootstrap4",
        language: 'es'
    }).on('change', scheduleSearch);
    $('select[name="product"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_product'
                };
            },
            processResults: function (data) {
                if (data.error) {
                    return { results: [] };
                }
                return {
                    results: data.map(function (item) {
                        return { id: item.id, text: item.name + ' (' + item.id + ')' };
                    })
                };
            }
        },
        placeholder: 'Todos los productos',
        minimumInputLength: 2
    }).on('change', scheduleSearch);

    $('select[name="update_type"]').on('change', scheduleSearch);
    $('input[name="update_value"]').on('input', scheduleSearch);

    $('#btn_apply').on('click', applyUpdate);

    searchProducts();
});
