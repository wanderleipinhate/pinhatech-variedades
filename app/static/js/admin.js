/**
 * Pinhatech & Variedades - Admin Panel JavaScript
 * Gerador de Copy, Copiar Links Curtos e Utilitários de Produtividade
 */

document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) {
        window.lucide.createIcons();
    }

    initAutoSlug();
});

/**
 * Copia o link curto /ir/{slug} para a área de transferência
 */
function copyShortLink(fullUrl) {
    navigator.clipboard.writeText(fullUrl).then(() => {
        showToast('Link curto copiado com sucesso! Pronto para colar.', 'success');
    }).catch(err => {
        console.error('Erro ao copiar link:', err);
        fallbackCopyTextToClipboard(fullUrl);
    });
}

/**
 * Abre o modal com texto pronto para Telegram, WhatsApp e Facebook
 */
function openCopyModal(productData) {
    const modal = document.getElementById('copy-modal');
    const textarea = document.getElementById('copy-text-content');
    
    if (!modal || !textarea) return;

    // Formatação de alta conversão para redes sociais
    const lines = [
        '🔥 *SUPER OFERTA PINHATECH & VARIEDADES!* 🔥',
        '',
        `⚡ *${productData.title}*`,
        productData.oldPrice ? `🏷️ ~De: ${productData.oldPrice}~` : '',
        `💰 *Por apenas: ${productData.currentPrice}*`,
        productData.installments ? `💳 ${productData.installments}` : '',
        productData.badge ? `📦 Selo: ${productData.badge}` : '',
        '',
        '👇 *Garanta o seu no link oficial do Mercado Livre:*',
        `👉 ${productData.shortUrl}`,
        '',
        '⚠️ _Preço e estoque sujeitos a alteração a qualquer momento!_'
    ].filter(line => line !== null && line !== undefined);

    const formattedMessage = lines.join('\n');
    textarea.value = formattedMessage;

    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

/**
 * Fecha o modal de copy
 */
function closeCopyModal() {
    const modal = document.getElementById('copy-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

/**
 * Copia o conteúdo atual do textarea do modal para o clipboard
 */
function copyFormattedText() {
    const textarea = document.getElementById('copy-text-content');
    if (!textarea) return;

    textarea.select();
    navigator.clipboard.writeText(textarea.value).then(() => {
        showToast('Texto para redes sociais copiado com sucesso!', 'success');
        closeCopyModal();
    }).catch(err => {
        fallbackCopyTextToClipboard(textarea.value);
        closeCopyModal();
    });
}

/**
 * Sincronização automática do Slug conforme o usuário digita o Título
 */
function initAutoSlug() {
    const titleInput = document.getElementById('title');
    const slugInput = document.getElementById('slug');

    if (!titleInput || !slugInput) return;

    // Se o slug estiver vazio (produto novo), sincroniza com o título
    titleInput.addEventListener('input', () => {
        if (!slugInput.dataset.manualEdit) {
            slugInput.value = slugifyText(titleInput.value);
        }
    });

    // Se o usuário editar o slug manualmente, para de sobrescrever
    slugInput.addEventListener('input', () => {
        slugInput.dataset.manualEdit = 'true';
    });
}

function slugifyText(text) {
    return text
        .toString()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .trim()
        .replace(/[^a-z0-9 -]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-');
}

/**
 * Confirmação de Exclusão de Produto
 */
function confirmDelete(productTitle) {
    return confirm(`Tem certeza que deseja excluir o produto "${productTitle}"?\nEsta ação não poderá ser desfeita.`);
}

/**
 * Fallback para navegadores sem suporte direto à Clipboard API
 */
function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        document.execCommand('copy');
        showToast('Texto copiado para a área de transferência!', 'success');
    } catch (err) {
        showToast('Não foi possível copiar automaticamente.', 'error');
    }
    document.body.removeChild(textArea);
}

/**
 * Toast flutuante para feedback visual
 */
function showToast(message, type = 'success') {
    let toast = document.getElementById('toast-notification');
    
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast-notification';
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
