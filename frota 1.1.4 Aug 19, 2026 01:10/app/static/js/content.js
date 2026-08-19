


/* ==========================================================================
   LÓGICA GLOBAL DA BASE (main.js)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // 1. MENU HAMBÚRGUER MOBILE
    const btnMenuMobile = document.getElementById('btnMenuMobileBase');
    const navegacaoBase = document.getElementById('navegacaoBase');

    if (btnMenuMobile && navegacaoBase) {
        btnMenuMobile.addEventListener('click', function (e) {
            e.stopPropagation();
            navegacaoBase.classList.toggle('menu_ativo-base');
        });

        // Fecha o menu mobile ao clicar fora dele na tela
        document.addEventListener('click', function (e) {
            if (!navegacaoBase.contains(e.target) && !btnMenuMobile.contains(e.target)) {
                navegacaoBase.classList.remove('menu_ativo-base');
            }
        });
    }

    // 2. DROPDOWN OU CLIQUE NO PERFIL DO USUÁRIO
    const btnPerfilUsuario = document.getElementById('btnPerfilUsuarioBase');
    const menuUsuarioDropdown = document.getElementById('menuUsuarioDropdownBase');

    if (btnPerfilUsuario && menuUsuarioDropdown) {
        btnPerfilUsuario.addEventListener('click', function (e) {
            e.stopPropagation();
            menuUsuarioDropdown.classList.toggle('dropdown_ativo-base');
        });

        // Fecha o menu do usuário ao clicar fora
        document.addEventListener('click', function (e) {
            if (!menuUsuarioDropdown.contains(e.target)) {
                menuUsuarioDropdown.classList.remove('dropdown_ativo-base');
            }
        });
    }

});












/* ==========================================================================
   INTERAÇÕES DO CONTEÚDO (HOME, LOGIN E CADASTRO)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // --- 1. MOSTRAR / OCULTAR SALDO DO CAIXA (HOME) ---
    const btnToggleCaixa = document.getElementById('btnToggleCaixaHome');
    const valorCaixaOculto = document.getElementById('valorCaixaHome');
    const valorCaixaReal = document.getElementById('valorRealCaixaHome');

    if (btnToggleCaixa && valorCaixaOculto && valorCaixaReal) {
        btnToggleCaixa.addEventListener('click', function (e) {
            e.preventDefault();
            valorCaixaOculto.classList.toggle('desativado-home');
            valorCaixaReal.classList.toggle('desativado-home');
        });
    }

    // --- 2. MOSTRAR / OCULTAR SENHA (LOGIN) ---
    const btnToggleSenha = document.getElementById('btnToggleSenhaLogin');
    const campoSenha = document.getElementById('password');

    if (btnToggleSenha && campoSenha) {
        btnToggleSenha.addEventListener('click', function (e) {
            e.preventDefault();
            const tipoAtual = campoSenha.getAttribute('type');
            if (tipoAtual === 'password') {
                campoSenha.setAttribute('type', 'text');
                btnToggleSenha.textContent = '🙈';
            } else {
                campoSenha.setAttribute('type', 'password');
                btnToggleSenha.textContent = '👁️';
            }
        });
    }

});



















