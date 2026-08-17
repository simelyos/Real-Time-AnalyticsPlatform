async function loadDashboard() {

    try {

        console.log("Trying to load dashboard.");

        const summaryResponse =
            await fetch("/api/analytics/summary");

        const productsResponse =
            await fetch("/api/analytics/products");

        const customersResponse =
            await fetch("/api/analytics/customers");

        const categoriesResponse =
            await fetch("/api/analytics/categories");


        if (!summaryResponse.ok ||
            !productsResponse.ok ||
            !customersResponse.ok ||
            !categoriesResponse.ok) {

            throw new Error(
                "Failed to fetch analytics data"
            );
        }


        const summary =
            await summaryResponse.json();

        const products =
            await productsResponse.json();

        const customers =
            await customersResponse.json();

        const categories =
            await categoriesResponse.json();


        updateSummary(summary);

        updateProducts(products);

        updateCustomers(customers);

        updateCategories(categories);

    }

    catch (error) {

        console.error(
            "Failed to load dashboard:",
            error
        );

    }
}

function updateSummary(data) {

    document.getElementById("total-orders").textContent =
        data.total_orders;

    document.getElementById("total-items").textContent =
        data.total_items;

    document.getElementById("total-revenue").textContent =
        Number(data.total_revenue).toFixed(2);

    document.getElementById("average-order-value").textContent =
        Number(data.average_order_value).toFixed(2);
}

function updateProducts(products) {

    const table =
        document.getElementById("products-table");

    table.innerHTML = "";


    for (const product of products) {

        const row =
            document.createElement("tr");


        row.innerHTML = `
            <td>${product.name}</td>
            <td>${product.quantity}</td>
            <td>$${Number(product.revenue).toFixed(2)}</td>
        `;


        table.appendChild(row);
    }
}

function updateCustomers(customers) {

    const table =
        document.getElementById("customers-table");

    table.innerHTML = "";


    for (const customer of customers) {

        const row =
            document.createElement("tr");


        row.innerHTML = `
            <td>${customer.name}</td>
            <td>${customer.orders}</td>
            <td>$${Number(customer.spending).toFixed(2)}</td>
        `;


        table.appendChild(row);
    }
}

function updateCategories(categories) {

    const table =
        document.getElementById("categories-table");

    table.innerHTML = "";


    for (const category of categories) {

        const row =
            document.createElement("tr");


        row.innerHTML = `
            <td>${category.category}</td>
            <td>${category.quantity}</td>
            <td>$${Number(category.revenue).toFixed(2)}</td>
        `;


        table.appendChild(row);
    }
}


loadDashboard();