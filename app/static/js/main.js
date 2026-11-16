/**
 * Pinhatech & Variedades - Main Client-Side JavaScript
 * Otimizado para UX fluida e alta conversão mobile e desktop.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Inicializa ícones do Lucide
    if (window.lucide) {
        window.lucide.createIcons();
    }

    initLiveSearch();
    initImageFallbacks();
});

/**
 * Filtro em tempo real no cliente para busca rápida enquanto o usuário digita
 */
function initLiveSearch() {
    const searchInput = document.getElementById('search-input');
    const productGrid = document.getElementById('products-grid');
    const noResultsMessage = document.getElementById('no-results-message');
    const resultsCount = document.getElementById('results-count');

    if (!searchInput || !productGrid) return;

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        const cards = productGrid.querySelectorAll('.product-card');
        let visibleCount = 0;

        cards.forEach(card => {
            const title = card.getAttribute('data-title')?.toLowerCase() || '';
            const category = card.getAttribute('data-category')?.toLowerCase() || '';

            if (title.includes(query) || category.includes(query)) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Atualiza contador de ofertas visíveis
        if (resultsCount) {
            resultsCount.textContent = visibleCount;
        }

        // Exibe mensagem caso nenhum produto coincida
        if (noResultsMessage) {
            if (visibleCount === 0 && cards.length > 0) {
                noResultsMessage.classList.remove('hidden');
            } else {
                noResultsMessage.classList.add('hidden');
            }
        }
    });
}

/**
 * Fallback para imagens com link quebrado ou erro de carregamento
 */
function initImageFallbacks() {
    const images = document.querySelectorAll('.product-image');
    images.forEach(img => {
        img.addEventListener('error', () => {
            img.src = 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80';
        });
    });
}

/**
 * Sistema de Toast Notification Flutuante
 */
function showToast(message, type = 'success') {
    let toast = document.getElementById('toast-notification');
    
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast-notification';
        toast.className = 'fixed bottom-5 right-5 z-50 flex items-center gap-3 px-5 py-3 rounded-xl shadow-2xl border transition-all duration-300 opacity-0 translate-y-4';
        document.body.appendChild(toast);
    }

    const isSuccess = type === 'success';
    toast.className = `fixed bottom-5 right-5 z-50 flex items-center gap-3 px-5 py-3 rounded-xl shadow-2xl border transition-all duration-300 opacity-100 translate-y-0 ${
        isSuccess 
            ? 'bg-[#1A1A1A] border-[#FF6B00] text-white' 
            : 'bg-red-950 border-red-500 text-red-200'
    }`;

    toast.innerHTML = `
        <span class="text-xl">${isSuccess ? '⚡' : '⚠️'}</span>
        <span class="font-medium text-sm">${message}</span>
    `;

    setTimeout(() => {
        toast.classList.remove('opacity-100', 'translate-y-0');
        toast.classList.add('opacity-0', 'translate-y-4');
    }, 3200);
}
