let userId = null
let pollingInterval = null
let selectedApps = []

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
                setTimeout(() => showStep2b(), 500)
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

function showStep2b() {
    document.getElementById('step-2').classList.add('hidden')
    document.getElementById('step-2b').classList.remove('hidden')
}

function toggleApp(el) {
    const app = el.getAttribute('data-app')
    el.classList.toggle('selected')

    if (el.classList.contains('selected')) {
        el.querySelector('.app-check').textContent = '✓'
        selectedApps.push(app)
    } else {
        el.querySelector('.app-check').textContent = '+'
        selectedApps = selectedApps.filter(a => a !== app)
    }
}

function connectApps() {
    if (selectedApps.length === 0) {
        alert('Please select at least one app to connect')
        return
    }

    document.getElementById('step-2b').classList.add('hidden')
    document.getElementById('step-2c').classList.remove('hidden')

    animateConnections(selectedApps)
}

const appDetails = {
    gmail: { icon: '📧', name: 'Gmail' },
    imessage: { icon: '💬', name: 'iMessage' },
    calendar: { icon: '📅', name: 'Google Calendar' },
    notes: { icon: '📝', name: 'Notes' },
    reminders: { icon: '🔔', name: 'Reminders' },
    whatsapp: { icon: '📲', name: 'WhatsApp' },
    slack: { icon: '💼', name: 'Slack' },
    spotify: { icon: '🎵', name: 'Spotify' }
}

function animateConnections(apps) {
    const list = document.getElementById('connection-steps-list')
    list.innerHTML = ''

    apps.forEach((app, i) => {
        const details = appDetails[app]
        const item = document.createElement('div')
        item.className = 'connection-item'
        item.id = `conn-${i}`
        item.innerHTML = `
            <span class="conn-icon">${details.icon}</span>
            <span class="conn-text">Connecting ${details.name}...</span>
            <span class="conn-status">⏳</span>
        `
        list.appendChild(item)
    })

    let index = 0

    const interval = setInterval(() => {
        if (index > 0) {
            const prev = document.getElementById(`conn-${index - 1}`)
            if (prev) {
                prev.classList.remove('active')
                prev.classList.add('done')
                prev.querySelector('.conn-status').textContent = '✅'
                const appName = appDetails[apps[index - 1]].name
                prev.querySelector('.conn-text').textContent = `${appName} connected`
            }
        }

        if (index < apps.length) {
            const current = document.getElementById(`conn-${index}`)
            if (current) {
                current.classList.add('active')
                current.querySelector('.conn-status').textContent = '⚡'
            }
            index++
        } else {
            const last = document.getElementById(`conn-${apps.length - 1}`)
            if (last) {
                last.classList.remove('active')
                last.classList.add('done')
                last.querySelector('.conn-status').textContent = '✅'
                const appName = appDetails[apps[apps.length - 1]].name
                last.querySelector('.conn-text').textContent = `${appName} connected`
            }
            clearInterval(interval)
            setTimeout(() => showStep3(), 1000)
        }
    }, 1200)
}

function showStep3() {
    document.getElementById('step-2c').classList.add('hidden')
    document.getElementById('step-3').classList.remove('hidden')
}