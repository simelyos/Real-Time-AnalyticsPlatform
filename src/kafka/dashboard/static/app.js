const socket = new WebSocket(
    `ws://${window.location.host}/ws`
);


socket.onopen = function() {
    console.log("WebSocket connected");
};


socket.onmessage = function(event) {

    const data = JSON.parse(event.data);

    updateDashboard(data);
};


socket.onclose = function() {
    console.log("WebSocket disconnected");
};


socket.onerror = function(error) {
    console.error(
        "WebSocket error:",
        error
    );
};


function updateDashboard(data) {

    document.getElementById("total-orders").textContent =
        data.total_orders;

    document.getElementById("total-items").textContent =
        data.total_items;

    document.getElementById("total-revenue").textContent =
        `$${data.total_revenue.toFixed(2)}`;

    updateProducts(data.top_products);

    updateCustomers(data.top_customers);

    updateRecent(data.recent_events);
}


function updateProducts(products) {

    const table =
        document.getElementById("products-table");

    table.innerHTML = "";

    for (const product of products) {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${product.product_id}</td>
            <td>${product.quantity}</td>
            <td>$${product.revenue.toFixed(2)}</td>
        `;

        table.appendChild(row);
    }
}


function updateCustomers(customers) {

    const table =
        document.getElementById("customers-table");

    table.innerHTML = "";

    for (const customer of customers) {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${customer.customer_id}</td>
            <td>${customer.quantity}</td>
            <td>$${customer.revenue.toFixed(2)}</td>
        `;

        table.appendChild(row);
    }
}


function updateRecent(events) {

    const table =
        document.getElementById("recent-table");

    table.innerHTML = "";

    for (const event of events) {

        const row = document.createElement("tr");

        const time =
            new Date(event.created_at)
                .toLocaleTimeString();

        row.innerHTML = `
            <td>${event.customer_id}</td>
            <td>${event.product_id}</td>
            <td>${event.quantity}</td>
            <td>$${event.unit_price.toFixed(2)}</td>
            <td>$${event.total_price.toFixed(2)}</td>
            <td>${time}</td>
        `;

        table.appendChild(row);
    }
}