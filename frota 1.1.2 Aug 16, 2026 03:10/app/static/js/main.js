/* ==========================================================================
   ARQUIVO JAVASCRIPT GLOBAL - LOGÍSTICA FÁCIL
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    
    // --- LÓGICA DO MENU HAMBURGUER RESPONSIVO (_base) ---
    const btnMenuMobile = document.getElementById('btnMenuMobile');
    const navegacaoPrincipal = document.getElementById('navegacaoPrincipal');

    if (btnMenuMobile && navegacaoPrincipal) {
        btnMenuMobile.addEventListener('click', function() {
            // Alterna a classe de exibição do menu mobile
            navegacaoPrincipal.classList.toggle('menu_ativo-base');
        });

        // Fecha o menu ao clicar fora dele
        document.addEventListener('click', function(evento) {
            const clicouNoMenu = navegacaoPrincipal.contains(evento.target);
            const clicouNoBotao = btnMenuMobile.contains(evento.target);

            if (!clicouNoMenu && !clicouNoBotao && navegacaoPrincipal.classList.contains('menu_ativo-base')) {
                navegacaoPrincipal.classList.remove('menu_ativo-base');
            }
        });
    }

});







