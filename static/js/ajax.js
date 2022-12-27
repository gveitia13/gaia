//Auxiliary method: submit with ajax and jQuery
function ajaxFunction(url, parameters, type, callback, async = true) {
  $.ajax({
    url: url,
    type: type,
    data: parameters,
    dataType: 'json',
    processData: false,
    contentType: false,
    async: async
  })
    .done(function (data) {
      // callback(data)
      if (!data.hasOwnProperty('error')) {
        callback(data)
        return false
      } else {
        console.log(data)
        Swal.fire({
          title: 'Error',
          text: data['error'],
          icon: 'error'
        });
      }
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      alert(textStatus + ': ' + errorThrown)
    })
    .always(function (data) {
      console.log(data)
    })
}

//For Delete using jQuery confirm plugin and Jquery with ajax
let submit_with_ajax_alert = function (url, title, content, parameters, callback, icon) {
  $.confirm({
    theme: 'material',
    title: title,
    icon: icon,
    content: content,
    columnClass: 'small',
    typeAnimated: true,
    cancelButtonClass: 'bg-gradient-primary circular',
    draggable: true,
    dragWindowBorder: false,
    buttons: {
      info: {
        text: 'Si',
        btnClass: 'rounded-pill btn btn-secondary',
        action: function () {
          ajaxFunction(url, parameters, 'POST', callback, true)
        }
      },
      danger: {
        text: 'No',
        btnClass: 'rounded-pill btn btn-primary',
        action: () => {
        }
      }
    }
  })
}
let fetchFunction = (data, token, url) => {
  // let data = JSON.stringify(data)
  console.log(data)
  let headers = {
    "X-CSRFToken": token,
    'Content-Type': 'application/json',
    // pk: '{{ object.pk }}'
  }
  /*  $('#exampleModalCenter').modal({
      keyboard: false,
      backdrop: 'static',
    })*/
  fetch(url, {
    method: "POST",
    body: data,
    headers: headers
  }).then((res, reject) => {
    console.log(res);
    console.log(res.json());
  }).catch((err) => {

  })
}

class EasyHTTP {

  // Make an HTTP GET Request
  async get(url) {

    // Awaiting fetch response
    const response = await fetch(url);

    // Awaiting for response.json()
    const resData = await response.json();

    // Returning result data
    return resData;
  }

  // Make an HTTP POST Request
  async post(url, data, token) {

    // Awaiting fetch response and
    // defining method, headers and body
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
        "X-CSRFToken": token
      },
      body: JSON.stringify(data)
    });

    // Awaiting response.json()
    const resData = await response.json();

    // Returning result data
    return resData;
  }
}

