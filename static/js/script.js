// js/script.js
document.addEventListener('DOMContentLoaded', function() {
    // Existing functionality for 'Add to Cart'
    document.querySelector('#add-to-cart-btn').addEventListener('click', function() {
        alert('Added to cart!');
        // Implement the add-to-cart functionality here
    });

    // New functionality for dynamic order status updates
    // Assuming there's a way to identify orders on the page, e.g., data attributes
    const orderElements = document.querySelectorAll('[data-order-id]');
    orderElements.forEach(orderElement => {
        const orderId = orderElement.getAttribute('data-order-id');
        updateOrderStatus(orderId); // Call this on page load for each order
    });
});

// Function to fetch and update order status
function updateOrderStatus(orderId) {
    fetch(`/orders/status/${orderId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById(`status-${orderId}`).textContent = data.status;
        })
        .catch(error => console.log('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$.ajax({
    url: '/your-endpoint/',
    type: 'post',
    headers: {"X-CSRFToken": csrftoken},
    // Your AJAX data
});

// Optionally, set up a periodic update for order statuses
// setInterval(() => {
//     const orderElements = document.querySelectorAll('[data-order-id]');
//     orderElements.forEach(orderElement => {
//         const orderId = orderElement.getAttribute('data-order-id');
//         updateOrderStatus(orderId);
//     });
// }, 10000); // Update every 10 seconds, adjust as needed
