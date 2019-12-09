
function generateImage () {
  var xhr = new XMLHttpRequest()
  return new Promise((resolve, reject) => {
    xhr.open('get', '/generate', true)

    xhr.setRequestHeader('cache-control', 'no-cache, must-revalidate, post-check=0, pre-check=0')
    xhr.setRequestHeader('cache-control', 'max-age=0')
    xhr.setRequestHeader('expires', '0')
    xhr.setRequestHeader('expires', 'Tue, 01 Jan 1980 1:00:00 GMT')
    xhr.setRequestHeader('pragma', 'no-cache')

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
    const url = document.querySelector('#randomImage').src
    if (url) { URL.revokeObjectURL(url) }
    document.querySelector('#randomImage').src = img
}

document.addEventListener('DOMContentLoaded', () => {
  refreshImage()
  setInterval(refreshImage, imageRefreshInterval)
})