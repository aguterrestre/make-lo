function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Oops...!',
        html: html,
        icon: 'warning',
        confirmButtonColor: '#28a745',
        confirmButtonText: 'Aceptar'
    });
}

function submit_with_ajax(url, title, content, parameters, callback) {
    Swal.fire({
      title: title,
      text: content,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#28a745',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Si',
      cancelButtonText: 'No'
    }).then((result) => {
        if (result.value) {
          $.ajax({
              url: url, //window.location.pathname
              type: 'POST',
              data: parameters,
              dataType: 'json',
              processData: false,
              contentType: false,
          }).done(function (data) {
              console.log(data);
              if (!data.hasOwnProperty('error')) {
                  callback(data);
                  return false;
              }
              message_error(data.error);
          }).fail(function (jqXHR, textStatus, errorThrown) {
              alert(textStatus + ': ' + errorThrown);
          }).always(function (data) {
          });
        } else {

        }
      }
    )
    /*
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        console.log(data);
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
    */
}

function alert_action_ticket(title, content, callback, cancel) {
    Swal.fire({
      title: title,
      text: content,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#28a745',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Si',
      cancelButtonText: 'No'
    }).then((result) => {
        if (result.value) {
          callback();
        } else {
          cancel();
        }
      }
    )
    /*
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    cancel();
                }
            },
        }
    })
    */
}

function alert_action_remove_all(title, content, content_yes, callback) {
    Swal.fire({
      title: title,
      text: content,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#28a745',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Si, borrar todo!',
      cancelButtonText: 'Cancelar!'
    }).then((result) => {
      if (result.value) {
        callback();
        Swal.fire({
          title: 'Todo borrado!',
          text: content_yes,
          icon: 'success'
        })
      }
    })
    /*
    $.confirm({
      theme: 'material',
      title: title,
      icon: 'fa fa-info',
      content: content,
      columnClass: 'small',
      typeAnimated: true,
      cancelButtonClass: 'btn-primary',
      draggable: true,
      dragWindowBorder: false,
      buttons: {
          info: {
              text: "Si",
              btnClass: 'btn-primary',
              action: function () {
                  callback();
              }
          },
          danger: {
              text: "No",
              btnClass: 'btn-red',
              action: function () {
                  cancel();
              }
          },
      }
    })
    */
}

function submit_delete_with_ajax(url, parameters, callback) {
    $.ajax({
        url: url, //window.location.pathname
        type: 'POST',
        data: parameters,
        dataType: 'json',
        processData: false,
        contentType: false,
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            callback(data);
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {
    });
}
