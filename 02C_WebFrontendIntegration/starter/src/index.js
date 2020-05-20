
import ThumbnailServiceApi from '../image-api/dist'

const client = new ThumbnailServiceApi.ImageApi()

function getUploadLink(filename, type) {
	client.appGetImageUploadUrl(filename, type, (err, data, response) => {
    console.log(data)
  })
}

window.onload = (event) => {
  const uploadButton = document.getElementById('#upload_button')
  if (uploadButton) {
    uploadButton.addEventListener('click', (e) => {
      const uploadInput = document.getElementById('#upload_input')
      for (let file of uploadInput.files) {
        client.appGetImageUploadUrl(file.name, file.type, (err, imageUrl, response) => {
          const request = new Request(imageUrl.upload_url, {
            method: 'PUT',
            mode: 'cors',
            body: file,
            contentType: file.type,
          })

          fetch(request)
            .then(response => {
              console.log(response)
            })
        })
      }
    })
  }
};
