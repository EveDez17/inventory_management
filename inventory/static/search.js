function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(this, args);
        }, wait);
    };
}

document.getElementById('skuSearch').addEventListener('keyup', function(event) {
    debounce(function() {
        let input = event.target;
        let filter = input.value.toUpperCase();
        let div = document.getElementById('skuList');
        div.innerHTML = '';  // Clear previous results

        if (!filter) {
            div.style.display = "none";
            return;
        }

        // Fetch search results
        fetch(`/search_skus/?query=${filter}`)
            .then(response => response.json())
            .then(skus => {
                skus.forEach(sku => {
                    let a = document.createElement('a');
                    a.innerText = sku.name;
                    a.href = "javascript:void(0)";
                    a.classList.add('list-group-item');
                    a.addEventListener('click', function() {
                        document.getElementById('hiddenSearchQuery').value = sku.name;
                        document.getElementById('searchForm').submit();
                    });
                    div.appendChild(a);
                });
                div.style.display = skus.length ? "block" : "none";
            })
            .catch(error => console.error('Error fetching SKU data:', error));
    }, 250)();
});
