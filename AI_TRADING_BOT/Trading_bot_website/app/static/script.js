document.addEventListener("DOMContentLoaded", function () {
    console.log("Trading Bot Dashboard Loaded! ✅");

    // Function to update crypto price dynamically
    function updateCryptoPrice() {
        fetch('/get_crypto_price')
            .then(response => response.json())
            .then(data => {
                document.getElementById('crypto-price').textContent = `$${data.price}`;
            })
            .catch(error => console.error("Error fetching crypto price:", error));
    }

    // Function to update sentiment score dynamically
    function updateSentimentScore() {
        fetch('/get_sentiment_score')
            .then(response => response.json())
            .then(data => {
                document.getElementById('sentiment-score').textContent = data.score;
            })
            .catch(error => console.error("Error fetching sentiment score:", error));
    }

    // Function to fetch news articles dynamically
    function updateNews() {
        fetch('/get_news')
            .then(response => response.json())
            .then(data => {
                const newsList = document.getElementById('news-list');
                newsList.innerHTML = ""; // Clear old news
                data.articles.forEach(article => {
                    let listItem = document.createElement("li");
                    listItem.innerHTML = `<a href="${article.url}" target="_blank" class="text-blue-500 hover:underline">${article.title}</a>`;
                    newsList.appendChild(listItem);
                });
            })
            .catch(error => console.error("Error fetching news:", error));
    }

    // Auto-update every 10 seconds
    setInterval(() => {
        updateCryptoPrice();
        updateSentimentScore();
        updateNews();
    }, 10000);

    // Initialize Chart.js
    const ctx = document.getElementById('priceChart').getContext('2d');
    const priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1h', '2h', '3h', '4h', '5h', '6h'],
            datasets: [{
                label: 'BTC Price',
                data: [95000, 95500, 95300, 95600, 95800, 95653.4],
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: false }
            }
        }
    });

    // Initial fetch on page load
    updateCryptoPrice();
    updateSentimentScore();
    updateNews();
});
