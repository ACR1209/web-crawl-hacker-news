document.addEventListener('DOMContentLoaded', () => {
    
    const url = new URL(window.location.href)
    const filterVal = url.searchParams.get('filter')

    if (filterVal) {
        document.getElementById('filter').value = filterVal 
    }

    document.getElementById('refresh').addEventListener('click', async () => {
        // hit the refresh endpoint
        const response = await fetch('/refresh')

        if (response.status === 200) {
            // if successful, reload the page
            location.reload()
        }
    })

    document.getElementById('filter').addEventListener('change', async (event) => {
        const value = event.target.value
        
        switch (value) {
            case 'five-comments':
                filter(value, "comments", { min: 6 })
                break

            case 'not-five-points':
                filter(value, "points", { max: 5, min: 0 })
                break

            default:
                filter(null, "rank", {min: 0})
                break
        }


    })
})


function filter(filterValue, orderBy, countWords) {
    const url = new URL(window.location.href)

    if (filterValue) {
        url.searchParams.set('filter', filterValue)
    } else {
        url.searchParams.delete('filter')
    }

    url.searchParams.set('order_by', orderBy)
    url.searchParams.set('count_words_min', countWords.min)

    if (countWords.max) {
        url.searchParams.set('count_words_max', countWords.max)
    } else {
        url.searchParams.delete('count_words_max')
    }
    window.location.href = url
}