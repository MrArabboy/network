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
  loader.style.display = 'block'
  const result = document.getElementById('result')
  result.style.display = 'none'
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

    console.log(res)

    const time = res.time.toFixed(3)
    loader.style.display = 'none'
    result.style.display = 'block'
    result.innerText = 'Time = ' + time + ' s'
  } catch (e) {
    console.log(e)
  }
}
