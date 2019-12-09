
function generateImage () {
  var xhr = new XMLHttpRequest()
  return new Promise((resolve, reject) => {
    xhr.open('get', '/generate', true)
    xhr.responseType = 'blob'
    xhr.onload = () => {
      if (xhr.status === 200) {
        resolve(xhr)
      } else {
        reject(new Error({ status: xhr.status, statusText: xhr.statusText }))
      }
    }
    xhr.send()
  })
}

async function refreshImage () {
    const img = await generateImage().then(r => URL.createObjectURL(r.response))
    document.querySelector('#randomImage').src = img
}

document.addEventListener('DOMContentLoaded', () => {
  refreshImage()
  setInterval(refreshImage, 1000 * 60 * 2)
})