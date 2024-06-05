;(function() {
    const toastElement = document.getElementById('toast')
    const toastBody = document.getElementById('toast-body')
    const toast = new bootstrap.Toast(toastElement)

    htmx.on('showMessage', (e) => {
        levelColor = e.detail.level
        toastElement.classList.add('text-' + levelColor + '-emphasis')
        toastElement.classList.add('bg-' + levelColor + '-subtle')
        toastElement.classList.add('border-' + levelColor + '-subtle')
        toastBody.innerText = e.detail.message
        toast.show()
    })
})()