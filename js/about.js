// Inicializar la página Sobre Nosotros
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    initializeAnimations();
});

// Configurar event listeners
function setupEventListeners() {
    // Botón de regreso al dashboard
    const backBtn = document.querySelector('.back-btn');
    if (backBtn) {
        backBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = 'index.html';
        });
    }
    
    // Navegación del sidebar
    const dashboardIcon = document.querySelector('.sidebar-icon:nth-child(1)');
    const downloadIcon = document.querySelector('.sidebar-icon:nth-child(2)');
    
    if (dashboardIcon) {
        dashboardIcon.addEventListener('click', function() {
            window.location.href = 'index.html';
        });
    }
    
    if (downloadIcon) {
        downloadIcon.addEventListener('click', function() {
            window.location.href = 'download.html';
        });
    }
    
    // Efectos hover en las tarjetas del equipo
    const teamCards = document.querySelectorAll('.team-card');
    teamCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Efectos hover en los valores
    const valueItems = document.querySelectorAll('.value-item');
    valueItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.05)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Inicializar animaciones
function initializeAnimations() {
    // Animación de entrada para las tarjetas del equipo
    const teamCards = document.querySelectorAll('.team-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    teamCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
    
    // Animación de entrada para los valores
    const valueItems = document.querySelectorAll('.value-item');
    valueItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(item);
    });
}

// Efecto de parallax suave en el scroll
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.team-intro, .mission-section');
    
    parallaxElements.forEach(element => {
        const speed = 0.5;
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// Efecto de brillo en las tarjetas del equipo
function addGlowEffect() {
    const teamCards = document.querySelectorAll('.team-card');
    
    teamCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Agregar efecto de brillo
            this.style.boxShadow = `
                0 10px 25px rgba(0, 168, 255, 0.2),
                0 0 30px rgba(0, 168, 255, 0.1)
            `;
        });
        
        card.addEventListener('mouseleave', function() {
            // Remover efecto de brillo
            this.style.boxShadow = '';
        });
    });
}

// Inicializar efectos especiales
addGlowEffect();

// Efecto de typing para el texto de introducción
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Aplicar efecto de typing al cargar la página
window.addEventListener('load', function() {
    const introText = document.querySelector('.team-intro p');
    if (introText) {
        const originalText = introText.textContent;
        typeWriter(introText, originalText, 30);
    }
});

// Efecto de partículas flotantes (opcional)
function createFloatingParticles() {
    const container = document.querySelector('.main-content');
    const particleCount = 20;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(0, 168, 255, 0.3);
            border-radius: 50%;
            pointer-events: none;
            animation: float ${Math.random() * 10 + 10}s infinite linear;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
        `;
        
        container.appendChild(particle);
    }
    
    // Agregar animación CSS para las partículas
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// Activar partículas flotantes (opcional)
// createFloatingParticles();

// Efecto de scroll suave para navegación interna
function smoothScrollTo(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Agregar indicador de scroll
function addScrollIndicator() {
    const scrollIndicator = document.createElement('div');
    scrollIndicator.className = 'scroll-indicator';
    scrollIndicator.innerHTML = '<i class="fas fa-chevron-down"></i>';
    scrollIndicator.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: var(--rosa-vibrante);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
        cursor: pointer;
        z-index: 1000;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 108, 171, 0.3);
    `;
    
    scrollIndicator.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    scrollIndicator.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1)';
        this.style.boxShadow = '0 6px 20px rgba(255, 108, 171, 0.5)';
    });
    
    scrollIndicator.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
        this.style.boxShadow = '0 4px 15px rgba(255, 108, 171, 0.3)';
    });
    
    document.body.appendChild(scrollIndicator);
    
    // Mostrar/ocultar según el scroll
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollIndicator.style.opacity = '1';
            scrollIndicator.style.visibility = 'visible';
        } else {
            scrollIndicator.style.opacity = '0';
            scrollIndicator.style.visibility = 'hidden';
        }
    });
}

// Activar indicador de scroll
addScrollIndicator();
