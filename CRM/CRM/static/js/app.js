// notification timer
var message = document.getElementById('message');

if (message) { // Check if the element exists
    setTimeout(function () {
        message.style.display = 'none';
    }, 3000);
}
