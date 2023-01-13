let Alerta = (text, icon = 'success') => {
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
}


document.querySelector('#algo').addEventListener('click', () => {
  Alerta('{{ object.name }}' + 'se añadio al carro', 'success')
})