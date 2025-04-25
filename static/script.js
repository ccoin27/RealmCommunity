document.addEventListener('DOMContentLoaded', function() {

    function animateCounters() {
        const counters = {
            members: parseInt("{{ counters.members }}"),
            online: parseInt("{{ counters.online }}"),
            messages: parseInt("{{ counters.messages }}"),
            rpg_players: parseInt("{{ counters.rpg_players }}")
        };

        animateCounter('members-count', counters.members);
        animateCounter('online-count', counters.online);
        animateCounter('messages-count', counters.messages);
        animateCounter('rpg-count', counters.rpg_players);
    }

    function animateCounter(elementId, target) {
        const element = document.getElementById(elementId);
        const duration = 2000;
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;

        const counter = setInterval(() => {
            current += increment;
            if (current >= target) {
                clearInterval(counter);
                element.textContent = target + "+";
            } else {
                element.textContent = Math.floor(current) + "+";
            }
        }, 16);
    }

    function checkForUpdates() {
        fetch('/api/counters')
            .then(response => response.json())
            .then(data => {
                if (new Date(data.last_updated) > new Date("{{ counters.last_updated }}")) {
                    updateCountersUI(data);
                }
            });
    }

    function updateCountersUI(data) {
        document.getElementById('members-count').textContent = data.members + "+";
        document.getElementById('online-count').textContent = data.online + "+";
        document.getElementById('messages-count').textContent = data.messages + "+";
        document.getElementById('rpg-count').textContent = data.rpg_players + "+";
        document.getElementById('last-updated').textContent = new Date(data.last_updated).toLocaleString();
    }

    // Инициализация
    animateCounters();
    setInterval(checkForUpdates, 300000); 
});