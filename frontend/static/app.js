let userId = null
let pollingInterval = null

async function signup() {
    const name = document.getElementById('name').value.trim()
    const telegram = document.getElementById('telegram_username').value.trim()
    const phone = document.getElementById('phone_number').value.trim()

    if (!name || !telegram || !phone) {
        alert('Please fill in all fields')
        return
    }

    try {
        const response = await fetch('/api/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                telegram_username: telegram,
                phone_number: phone
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

async function provisionAgent(userId) {
    try {
        await fetch('/api/agent/provision', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId })
        })

        startPolling(userId)

    } catch (error) {
        console.error('Provisioning failed:', error)
    }
}

function startPolling(userId) {
    let progress = 0

    pollingInterval = setInterval(async () => {
        try {
            const response = await fetch(
                `/api/agent/status/${userId}`
            )
            const data = await response.json()

            progress = Math.min(progress + 10, 90)
            updateProgress(progress)

            updateMessage(data.status)

            if (data.status === 'ready') {
                clearInterval(pollingInterval)
                updateProgress(100)
                setTimeout(() => showStep3(data), 500)
            }

            if (data.status === 'failed') {
                clearInterval(pollingInterval)
                document.getElementById('provision-message')
                    .textContent = 'Something went wrong. Please refresh and try again.'
            }

        } catch (error) {
            console.error('Polling error:', error)
        }
    }, 2000)
}

function updateMessage(status) {
    const messages = {
        'created': 'Creating your account...',
        'provisioning': 'Spinning up your personal agent...',
        'ready': 'Your agent is ready!',
        'failed': 'Something went wrong...'
    }

    const el = document.getElementById('provision-message')
    if (el && messages[status]) {
        el.textContent = messages[status]
    }
}

function updateProgress(percent) {
    const fill = document.getElementById('progress-fill')
    if (fill) {
        fill.style.width = `${percent}%`
    }
}

function showStep2() {
    document.getElementById('step-1').classList.add('hidden')
    document.getElementById('step-2').classList.remove('hidden')
}

function showStep3(data) {
    document.getElementById('step-2').classList.add('hidden')
    document.getElementById('step-3').classList.remove('hidden')

    const botUsername = 'your_bot_username'
    const link = document.getElementById('telegram-link')
    if (link) {
        link.href = `https://t.me/${botUsername}`
    }
}