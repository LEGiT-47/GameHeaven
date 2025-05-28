// Toggle Navbar in Mobile View
const menuBtn = document.getElementById('menu-btn');
const navbar = document.querySelector('.nav-links');

menuBtn.addEventListener('click', () => {
    navbar.classList.toggle('active');
});

// Add to Cart
let cart = [];

function addToCart(productId) {
    const productElement = document.querySelector(`#product-${productId}`);
    const productName = productElement.querySelector('.product-name').textContent;
    const productPrice = parseFloat(productElement.querySelector('.price').textContent.replace('$', ''));
    const product = { id: productId, name: productName, price: productPrice, quantity: 1 };

    const existingProduct = cart.find(item => item.id === productId);
    if (existingProduct) {
        existingProduct.quantity++;
    } else {
        cart.push(product);
    }

    updateCartDisplay();
    alert('Product added to cart!');
}

function updateCartDisplay() {
    const cartCount = cart.reduce((total, item) => total + item.quantity, 0);

// Update cart display
    document.querySelector('.cart a').textContent = `Cart (${cartCount})`;
}

// Remove from cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCartDisplay();
    displayCartItems();
}

// Display cart items
function displayCartItems() {
    const cartItemsContainer = document.querySelector('.cart-items');
    cartItemsContainer.innerHTML = '';

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p>Your cart is empty.</p>';
        return;
    }

    cart.forEach(item => {
        cartItemsContainer.innerHTML += `
            <div class="cart-item">
                <img src="${item.image}" alt="${item.name}">
                <div class="item-details">
                    <h4>${item.name}</h4>
                    <p>Price: $${item.price}</p>
                    <p>Quantity: ${item.quantity}</p>
                    <button class="btn remove" onclick="removeFromCart(${item.id})">Remove</button>
                </div>
            </div>
        `;
    });
}

// Call displayCartItems() on page load if the cart page is rendered
window.onload = function() {
    if (document.querySelector('.cart-items')) {
        displayCartItems();
    }
}
