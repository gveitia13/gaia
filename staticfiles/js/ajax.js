const productModal = document.querySelector('#product_modal')
const productModal2 = new bootstrap.Modal(document.getElementById('product_modal'));

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
        })
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
  },
  fetchFunction = (data, token, url) => {
    // let data = JSON.stringify(data)
    console.log(data)
    let headers = {
      "X-CSRFToken": token,
      'Content-Type': 'application/json',
      // pk: '{{ object.pk }}'
    }
    fetch(url, {
      method: "POST",
      body: data,
      headers: headers
    }).then((res, reject) => {
      console.log(res);
      console.log(res.json());
    }).catch((err) => {

    })
  },
  Alerta = (text, icon = 'success') => {
    const Alerta = Swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 3000
    })
    Alerta.fire({
      icon: icon,
      title: text
    })
  },
  alert_action_yes_not = (title, content, callback, icon) => {
    $.confirm({
      theme: 'material',
      title: title,
      icon: icon,
      content: content,
      columnClass: 'small',
      typeAnimated: true,
      cancelButtonClass: 'btn-success rounded-pill',
      draggable: true,
      dragWindowBorder: false,
      buttons: {
        info: {
          text: 'Si',
          btnClass: 'btn-danger rounded-pill',
          action: function () {
            callback()
          }
        },
        danger: {
          text: 'No',
          btnClass: 'btn-success rounded-pill',
          action: () => {
          }
        }
      }
    })
  },
  llenarModal = data => {
    // document.querySelector('#img-modal').src = data.image
    document.querySelector('#img-modal').style = `background: url('${data.product.image}')`
    document.querySelector('#name-modal').innerHTML = data.product.name
    document.querySelector('#cat-modal').innerHTML = data.product.category.name
    document.querySelector('#price-modal').innerHTML = data.product.price + ' cup'
    document.querySelector('#delivery-modal').innerHTML = 'Tiempo de entrega máximo <b>'
      + data.product.delivery_time + ' días</b>'
    document.querySelector('#info-modal').innerHTML = data.product.info
    document.querySelector('#about-modal').innerHTML = data.product.about
    $("#input-touchspin").val(1).trigger("touchspin.updatesettings", {max: parseInt(data.product.stock) - parseInt(data.amount)});
    document.querySelector('#input-hidden-id-modal').value = data.product.id
    if (data.product.old_price)
      document.querySelector('#old-price-modal').innerHTML = data.product.old_price + ' cup'
  },
  limpiarModal = () => {
    document.querySelector('#img-modal').src = ''
    document.querySelector('#name-modal').innerHTML = ''
    document.querySelector('#cat-modal').innerHTML = ''
    document.querySelector('#price-modal').innerHTML = ''
    document.querySelector('#delivery-modal').innerHTML = ''
    document.querySelector('#info-modal').innerHTML = ''
    document.querySelector('#about-modal').innerHTML = ''
    document.querySelector('#old-price-modal').innerHTML = ''
  },
  updateCart = () => {
    let cant = 0
    const d = document
    d.querySelectorAll('.cards-horizontal .input-cantidad').forEach(e => cant++)
    let product = cant === 1 ? `producto` : 'productos',
      total = 0

    d.querySelectorAll('.cards-horizontal .card-s-cart div div > span.span-price b').forEach(e =>
      total += parseFloat(e.children[0].innerText.replace(',', '.')))
    console.log(total)

    d.querySelectorAll('#total-hidden').forEach(e => e.value = total)

    d.querySelectorAll('#total-price').forEach(e => e.innerHTML =
      `<b>Total</b>: (${cant} ${product}) <b>$${total.toFixed(2)}</b>`)

    d.querySelector('#botoncito-verde').innerHTML = `$ ${total.toFixed(2)} / ${cant} ${product}`
    total = 0
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

productModal.addEventListener('hidden.bs.modal', e => {
  document.querySelector('#my-loader').classList.remove('d-none')
  document.querySelector('#response').classList.remove('d-block')
  document.querySelector('#response').classList.add('d-none')
  console.log('se hizo el evento')
  limpiarModal()
})
