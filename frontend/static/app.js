async function signup() {
    const name = document.getElementById('name').value.trim()
    const telegram = document.getElementById('telegram_username').value.trim()

    if (!name || !telegram) {
        alert('Please fill in all fields')
        return
    }

    try {
        const response = await fetch('/api/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                telegram_username: telegram
            })
        })

        const data = await response.json()
        userId = data.user_id

        showStep2()
        await provisionAgent(userId)

    } catch (error) {
        alert('Something went wrong. Please try again.')
        console.error(error)
    }
}