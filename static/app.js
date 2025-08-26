// Seuils pour déterminer l'état visuel
const THRESHOLDS = {
    rainMM: 0.1,   // pluie visible si ≥ 0.1 mm
    cloudsPct: 70, // très nuageux si ≥ 70%
    windyKmh: 30   // vent fort si ≥ 30 km/h
};

// Lit les data-* du conteneur
function readInitialData() {
    const root = document.getElementById('app');
    if (!root) return null;

    const num = (x) => {
        const n = Number(x);
        return Number.isFinite(n) ? n : null;
    };

    return {
        temperature: num(root.dataset.temp),
        wind: num(root.dataset.wind),
        clouds: num(root.dataset.clouds),
        rain: num(root.dataset.rain),
    };
}

// Applique les classes météo sur <body> sans toucher au contenu
function applyTheme({rain, clouds, wind, temperature}) {
    const b = document.body;
    // enlève toutes les classes météo éventuellement présentes
    b.className = b.className.replace(/\b(sunny|cloudy|rainy|windy|temp-\w+)\b/g, '').trim();

    // état principal (pluie > nuages > soleil)
    if (typeof rain === 'number' && rain >= THRESHOLDS.rainMM) {
        b.classList.add('rainy');
    } else if (typeof clouds === 'number' && clouds >= THRESHOLDS.cloudsPct) {
        b.classList.add('cloudy');
    } else {
        b.classList.add('sunny');
    }

    // état vent (peut se combiner)
    if (typeof wind === 'number' && wind >= THRESHOLDS.windyKmh) {
        b.classList.add('windy');
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const data = readInitialData();
    if (data) applyTheme(data);
});
