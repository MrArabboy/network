function sleep(milliseconds) {
  const date = Date.now()
  let currentDate = null
  do {
    currentDate = Date.now()
  } while (currentDate - date < milliseconds)
}

function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}
const csrftoken = getCookie('csrftoken')

const onSubmit = async () => {
  const loader = document.getElementById('calculating_loader')
  loader.style.display = 'flex'
  const result = document.getElementById('result')
  result.style.display = 'none'
  const graph = document.getElementById('myBtn')
  const calculation_form = document.getElementById('form_inline')
  calculation_form.style.display = 'block'
  calculation_form.style.float = 'left'
  calculation_form.style.marginLeft = '20px'

  // sleep(3000)
  const input1 = document.getElementById('rangeInput1')
  const input2 = document.getElementById('amount2')

  try {
    const loadingValue = input1.value
    const packetLossRate = input2.value
    let res = await fetch('/calculate/', {
      method: 'POST',
      body: JSON.stringify({
        loading_value: loadingValue,
        packet_loss_rate: packetLossRate,
      }),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
        mode: 'same-origin',
      },
    })
    res = await res.json()
    var result_graph_image = document.getElementById('result-graph')
    result_graph_image.src = '/static/app/' + res.img + '.png'

    console.log(res)

    const time = res.time.toFixed(5)
    loader.style.display = 'none'
    graph.style.display = 'block'
    result.style.display = 'inline-block'
    result.style.float = 'right'
    document.getElementById('update_timer').innerText =
      'Update Timer = ' + Number(time).toFixed(4) + ' s'
    document.getElementById('invalid_timer').innerText =
      'Invalid Timer = ' + 6 * Number(time).toFixed(4) + ' s'
    document.getElementById('hold_down').innerText =
      'Hold Down = ' + 6 * Number(time).toFixed(4) + ' s'
    document.getElementById('flush_timer').innerText =
      'Flush Timer = ' + 8 * Number(time).toFixed(4) + ' s'
  } catch (e) {
    console.log(e)
  }
}

// Get the modal
var modal = document.getElementById('myModal')

// Get the button that opens the modal
var btn = document.getElementById('myBtn')
console.log(btn)
// Get the <span> element that closes the modal
var span = document.getElementsByClassName('close')[0]

// When the user clicks the button, open the modal
btn.onclick = function () {
  modal.style.display = 'block'
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = 'none'
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none'
  }
}
