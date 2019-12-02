function ajax (method, url, data, header) {
  var request = new XMLHttpRequest()

  return new Promise((resolve, reject) => {
    request.onload = () => {
      if (request.status === 200) {
        resolve(request)
      } else {
        reject(new Error({ status: request.status, statusText: request.statusText }))
      }
    }

    request.open(method, url, true)
    if (header) {
      for (const item of Object.entries(header)) { request.setRequestHeader(...item) }
    }
    request.send(data)
  })
}

function appendParams (base, params) {
  return `${base}?${Object.entries(params).map(i => i.join('=')).join('&')}`
}

function animationEnd (element) {
  return new Promise(resolve => element.addEventListener('animationend', resolve, { once: true }))
}
