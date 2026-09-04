


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















/* ==========================================================================
   LÓGICA DA TELA DE PERFIL DO USUÁRIO (_perfil_user)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // --- AUTO-OCULTAR MENSAGENS DE SUCESSO/ALERTA DO PERFIL ---
    const mensagensPerfil = document.querySelectorAll('.mensagem_sucesso-content');
    if (mensagensPerfil.length > 0) {
        setTimeout(function () {
            mensagensPerfil.forEach(function (msg) {
                msg.style.transition = 'opacity 0.6s ease';
                msg.style.opacity = '0';
                setTimeout(function () {
                    msg.style.display = 'none';
                }, 600);
            });
        }, 4000); // Esconde a mensagem após 4 segundos
    }

});



/* ==========================================================================
   LÓGICA DA TELA DE EDIÇÃO DE PERFIL (_edit_user)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const formEditUser = document.getElementById('form-edit_user');

    if (formEditUser) {
        // Foca automaticamente no primeiro campo editável ao carregar
        const primeiroInputEditUser = formEditUser.querySelector('input:not([type="hidden"])');
        if (primeiroInputEditUser) {
            primeiroInputEditUser.focus();
        }

        // Previne envios duplicados ao salvar
        formEditUser.addEventListener('submit', function () {
            const btnSalvarEditUser = document.getElementById('btn_salvar-edit_user');
            if (btnSalvarEditUser) {
                btnSalvarEditUser.disabled = true;
                btnSalvarEditUser.textContent = 'Salvando...';
            }
        });
    }

});






/* ==========================================================================
   LÓGICA DA TELA DE ALTERAÇÃO DE SENHA (_alterar_senha_user)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const formAlterarSenha = document.getElementById('form-alterar_senha_user');

    if (formAlterarSenha) {
        // Foca no primeiro campo de senha automaticamente
        const primeiroCampoSenha = formAlterarSenha.querySelector('input[type="password"]');
        if (primeiroCampoSenha) {
            primeiroCampoSenha.focus();
        }

        // Evita múltiplos disparos do botão ao enviar
        formAlterarSenha.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-alterar_senha_user');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Atualizando...';
            }
        });
    }

});




/* ==========================================================================
   LÓGICA DA TELA DE GERENCIAMENTO DE VEÍCULOS (_veiculo)
   ========================================================================== */

/* ==========================================================================
   LÓGICA DA TELA DE LISTAGEM DE VEÍCULOS (_lista_veiculos)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // --- CONFIRMAÇÃO DE EXCLUSÃO DE VEÍCULO ---
    const formulariosExclusao = document.querySelectorAll('.form_excluir-lista_veiculos[data-confirm-exclusao]');

    formulariosExclusao.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const confirmacao = confirm('Deseja realmente excluir este veículo do sistema?');
            if (!confirmacao) {
                e.preventDefault();
            }
        });
    });

    // --- AUTO-OCULTAR ALERTAS DE SUCESSO ---
    const alertasVeiculos = document.querySelectorAll('.alerta_sucesso-lista_veiculos');
    if (alertasVeiculos.length > 0) {
        setTimeout(function () {
            alertasVeiculos.forEach(function (alerta) {
                alerta.style.transition = 'opacity 0.5s ease';
                alerta.style.opacity = '0';
                setTimeout(function () {
                    alerta.style.display = 'none';
                }, 500);
            });
        }, 4000);
    }

});




/* ==========================================================================
   LÓGICA DA TELA DE ADICIONAR VEÍCULO (_add_veiculo)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const formAddVeiculo = document.getElementById('form-add_veiculo');

    if (formAddVeiculo) {
        // Foca automaticamente no primeiro campo do formulário
        const primeiroCampoAddVeiculo = formAddVeiculo.querySelector('input:not([type="hidden"]), select, textarea');
        if (primeiroCampoAddVeiculo) {
            primeiroCampoAddVeiculo.focus();
        }

        // Evita múltiplos cliques ao salvar o formulário
        formAddVeiculo.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-add_veiculo');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Salvando Veículo...';
            }
        });
    }

});






/* ==========================================================================
   LÓGICA DA TELA DE EDITAR VEÍCULO (_editar_veiculo)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    const formEditarVeiculo = document.getElementById('form-editar_veiculo');

    if (formEditarVeiculo) {
        // Foca automaticamente no primeiro campo do formulário
        const primeiroCampoEditarVeiculo = formEditarVeiculo.querySelector('input:not([type="hidden"]), select, textarea');
        if (primeiroCampoEditarVeiculo) {
            primeiroCampoEditarVeiculo.focus();
        }

        // Evita múltiplos disparos do botão ao salvar
        formEditarVeiculo.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-editar_veiculo');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Salvando Alterações...';
            }
        });
    }

});















/* ==========================================================================
   LÓGICA DO MÓDULO DE FUNCIONÁRIOS (_lista_funcionario, _add_funcionario, _editar_funcionario)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // --- 1. CONFIRMAÇÃO DE EXCLUSÃO DE FUNCIONÁRIO ---
    const formsExcluirFunc = document.querySelectorAll('.form_excluir-lista_funcionario[data-confirm-exclusao]');
    formsExcluirFunc.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (!confirm('Deseja realmente remover este funcionário da equipe?')) {
                e.preventDefault();
            }
        });
    });

    // --- 2. AUTO-OCULTAR ALERTAS ---
    const alertasFunc = document.querySelectorAll('.alerta_sucesso-lista_funcionario');
    if (alertasFunc.length > 0) {
        setTimeout(function () {
            alertasFunc.forEach(function (alerta) {
                alerta.style.transition = 'opacity 0.5s ease';
                alerta.style.opacity = '0';
                setTimeout(function () { alerta.style.display = 'none'; }, 500);
            });
        }, 4000);
    }

    // --- 3. FOCO AUTOMÁTICO E PREVENÇÃO DE DUPLO CLIQUE EM ADD FUNCIONÁRIO ---
    const formAddFunc = document.getElementById('form-add_funcionario');
    if (formAddFunc) {
        const primeiroCampo = formAddFunc.querySelector('input:not([type="hidden"]), select');
        if (primeiroCampo) primeiroCampo.focus();

        formAddFunc.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-add_funcionario');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Salvando Funcionário...';
            }
        });
    }

    // --- 4. FOCO AUTOMÁTICO E PREVENÇÃO DE DUPLO CLIQUE EM EDITAR FUNCIONÁRIO ---
    const formEditarFunc = document.getElementById('form-editar_funcionario');
    if (formEditarFunc) {
        const primeiroCampo = formEditarFunc.querySelector('input:not([type="hidden"]), select');
        if (primeiroCampo) primeiroCampo.focus();

        formEditarFunc.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-editar_funcionario');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Salvando Alterações...';
            }
        });
    }

});










/* ==========================================================================
   LÓGICA DO MÓDULO DE FUNCIONÁRIOS (_lista_funcionario, _add_funcionario, _editar_funcionario)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // 1. Confirmação de Exclusão de Funcionário
    const formulariosExclusaoFunc = document.querySelectorAll('.form_excluir-lista_funcionario[data-confirm-exclusao]');
    formulariosExclusaoFunc.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const confirmacao = confirm('Deseja realmente excluir este funcionário?');
            if (!confirmacao) {
                e.preventDefault();
            }
        });
    });

    // 2. Auto-ocultar mensagens de sucesso
    const alertasFunc = document.querySelectorAll('.alerta_sucesso-lista_funcionario');
    if (alertasFunc.length > 0) {
        setTimeout(function () {
            alertasFunc.forEach(function (alerta) {
                alerta.style.transition = 'opacity 0.5s ease';
                alerta.style.opacity = '0';
                setTimeout(function () {
                    alerta.style.display = 'none';
                }, 500);
            });
        }, 4000);
    }

    // 3. Foco e prevenção de múltiplos envios em Adicionar Funcionário
    const formAddFunc = document.getElementById('form-add_funcionario');
    if (formAddFunc) {
        const primeiroCampoAdd = formAddFunc.querySelector('input:not([type="hidden"]), select, textarea');
        if (primeiroCampoAdd) primeiroCampoAdd.focus();

        formAddFunc.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-add_funcionario');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Adicionando...';
            }
        });
    }

    // 4. Foco e prevenção de múltiplos envios em Editar Funcionário
    const formEditarFunc = document.getElementById('form-editar_funcionario');
    if (formEditarFunc) {
        const primeiroCampoEdit = formEditarFunc.querySelector('input:not([type="hidden"]), select, textarea');
        if (primeiroCampoEdit) primeiroCampoEdit.focus();

        formEditarFunc.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-editar_funcionario');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Salvando Alterações...';
            }
        });
    }

});



















/* ==========================================================================
   LÓGICA UNIFICADA DO SISTEMA (content.js)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // --------------------------------------------------------------------------
    // 1. LÓGICA DA TELA DE VEÍCULOS (_lista_veiculos)
    // --------------------------------------------------------------------------
    const formulariosExclusaoVeiculo = document.querySelectorAll('.form_excluir-lista_veiculos[data-confirm-exclusao]');
    formulariosExclusaoVeiculo.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const confirmacao = confirm('Deseja realmente excluir este veículo do sistema?');
            if (!confirmacao) {
                e.preventDefault();
            }
        });
    });

    const alertasVeiculos = document.querySelectorAll('.alerta_sucesso-lista_veiculos');
    if (alertasVeiculos.length > 0) {
        setTimeout(function () {
            alertasVeiculos.forEach(function (alerta) {
                alerta.style.transition = 'opacity 0.5s ease';
                alerta.style.opacity = '0';
                setTimeout(function () {
                    alerta.style.display = 'none';
                }, 500);
            });
        }, 4000);
    }

    // --------------------------------------------------------------------------
    // 2. LÓGICA DA TELA DE ADICIONAR VEÍCULO (_add_veiculo)
    // --------------------------------------------------------------------------
    const formAddVeiculo = document.getElementById('form-add_veiculo');
    if (formAddVeiculo) {
        const primeiroCampoAddVeiculo = formAddVeiculo.querySelector('input:not([type="hidden"]), select, textarea');
        if (primeiroCampoAddVeiculo) {
            primeiroCampoAddVeiculo.focus();
        }

        formAddVeiculo.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-add_veiculo');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Salvando Veículo...';
            }
        });
    }

    // --------------------------------------------------------------------------
    // 3. LÓGICA DA TELA DE EDITAR VEÍCULO (_editar_veiculo)
    // --------------------------------------------------------------------------
    const formEditarVeiculo = document.getElementById('form-editar_veiculo');
    if (formEditarVeiculo) {
        const primeiroCampoEditarVeiculo = formEditarVeiculo.querySelector('input:not([type="hidden"]), select, textarea');
        if (primeiroCampoEditarVeiculo) {
            primeiroCampoEditarVeiculo.focus();
        }

        formEditarVeiculo.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-editar_veiculo');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Salvando Alterações...';
            }
        });
    }

    // --------------------------------------------------------------------------
    // 4. LÓGICA DO MÓDULO DE FUNCIONÁRIOS
    // --------------------------------------------------------------------------
    const formulariosExclusaoFunc = document.querySelectorAll('.form_excluir-lista_funcionario[data-confirm-exclusao]');
    formulariosExclusaoFunc.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const confirmacao = confirm('Deseja realmente excluir este funcionário?');
            if (!confirmacao) {
                e.preventDefault();
            }
        });
    });

    const alertasFunc = document.querySelectorAll('.alerta_sucesso-lista_funcionario');
    if (alertasFunc.length > 0) {
        setTimeout(function () {
            alertasFunc.forEach(function (alerta) {
                alerta.style.transition = 'opacity 0.5s ease';
                alerta.style.opacity = '0';
                setTimeout(function () {
                    alerta.style.display = 'none';
                }, 500);
            });
        }, 4000);
    }

    const formAddFunc = document.getElementById('form-add_funcionario');
    if (formAddFunc) {
        const primeiroCampoAdd = formAddFunc.querySelector('input:not([type="hidden"]), select, textarea');
        if (primeiroCampoAdd) primeiroCampoAdd.focus();

        formAddFunc.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-add_funcionario');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Adicionando...';
            }
        });
    }

    const formEditarFunc = document.getElementById('form-editar_funcionario');
    if (formEditarFunc) {
        const primeiroCampoEdit = formEditarFunc.querySelector('input:not([type="hidden"]), select, textarea');
        if (primeiroCampoEdit) primeiroCampoEdit.focus();

        formEditarFunc.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-editar_funcionario');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Salvando Alterações...';
            }
        });
    }

    // --------------------------------------------------------------------------
    // 5. LÓGICA DO MÓDULO DE VIAGENS
    // --------------------------------------------------------------------------
    const formulariosExclusaoViagem = document.querySelectorAll('.form_excluir-lista_viagem[data-confirm-exclusao]');
    formulariosExclusaoViagem.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const confirmacao = confirm('Tem certeza que deseja excluir esta viagem do sistema?');
            if (!confirmacao) {
                e.preventDefault();
            }
        });
    });

    const alertasViagem = document.querySelectorAll('.alerta_sucesso-lista_viagem');
    if (alertasViagem.length > 0) {
        setTimeout(function () {
            alertasViagem.forEach(function (alerta) {
                alerta.style.transition = 'opacity 0.5s ease';
                alerta.style.opacity = '0';
                setTimeout(function () {
                    alerta.style.display = 'none';
                }, 500);
            });
        }, 4000);
    }

    const formAddViagem = document.getElementById('form-add_viagem');
    if (formAddViagem) {
        const primeiroCampoAddViagem = formAddViagem.querySelector('input:not([type="hidden"]), select, textarea');
        if (primeiroCampoAddViagem) primeiroCampoAddViagem.focus();

        formAddViagem.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-add_viagem');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Salvando Viagem...';
            }
        });
    }

    const formEditarViagem = document.getElementById('form-editar_viagem');
    if (formEditarViagem) {
        const primeiroCampoEditViagem = formEditarViagem.querySelector('input:not([type="hidden"]), select, textarea');
        if (primeiroCampoEditViagem) primeiroCampoEditViagem.focus();

        formEditarViagem.addEventListener('submit', function () {
            const btnSalvar = document.getElementById('btn_salvar-editar_viagem');
            if (btnSalvar) {
                btnSalvar.disabled = true;
                btnSalvar.textContent = 'Salvando Alterações...';
            }
        });
    }

});




















document.addEventListener('DOMContentLoaded', function () {

    // Lógica para exclusão de lançamentos no caixa
    const formulariosExclusaoCaixa = document.querySelectorAll('.form_excluir-lista_caixa[data-confirm-exclusao]');
    formulariosExclusaoCaixa.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const confirmacao = confirm('Tem certeza que deseja excluir este lançamento do caixa?');
            if (!confirmacao) {
                e.preventDefault();
            }
        });
    });

    // Animação de fechamento dos alertas de sucesso no caixa
    const alertasCaixa = document.querySelectorAll('.alerta_sucesso-lista_caixa');
    if (alertasCaixa.length > 0) {
        setTimeout(function () {
            alertasCaixa.forEach(function (alerta) {
                alerta.style.transition = 'opacity 0.5s ease';
                alerta.style.opacity = '0';
                setTimeout(function () {
                    alerta.style.display = 'none';
                }, 500);
            });
        }, 4000);
    }

    // Trava de botão no envio - Form Despesa
    const formDespesa = document.getElementById('form-despesa_caixa');
    if (formDespesa) {
        formDespesa.addEventListener('submit', function () {
            const btn = document.getElementById('btn_salvar-despesa_caixa');
            if (btn) {
                btn.disabled = true;
                btn.textContent = 'Salvando Despesa...';
            }
        });
    }

    // Trava de botão no envio - Form Entrada
    const formEntrada = document.getElementById('form-entrada_caixa');
    if (formEntrada) {
        formEntrada.addEventListener('submit', function () {
            const btn = document.getElementById('btn_salvar-entrada_caixa');
            if (btn) {
                btn.disabled = true;
                btn.textContent = 'Salvando Entrada...';
            }
        });
    }

});












document.addEventListener('DOMContentLoaded', function () {
    const formsExcluirAbastecimento = document.querySelectorAll('.form_excluir');
    formsExcluirAbastecimento.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const confirmacao = confirm('Excluir este abastecimento também removerá a despesa do Caixa e atualizará os litros acumulados da viagem. Confirmar?');
            if (!confirmacao) {
                e.preventDefault();
            }
        });
    });
});
































// ==========================================================================
// CONFIRMAÇÃO DE SEGURANÇA PARA EXCLUSÃO DE CONTA
// ==========================================================================
document.addEventListener('DOMContentLoaded', function () {
    const formExcluirConta = document.querySelector('#form-excluir_conta');

    if (formExcluirConta) {
        formExcluirConta.addEventListener('submit', function (e) {
            const campoSenha = formExcluirConta.querySelector('input[type="password"]');

            if (!campoSenha || campoSenha.value.trim() === '') {
                e.preventDefault();
                alert('Por favor, digite sua senha atual para confirmar a exclusão.');
                campoSenha.focus();
                return;
            }

            const confirmacao = confirm(
                'ATENÇÃO: Você tem certeza absoluta que deseja excluir sua conta?\n\n' +
                'Esta ação apagará permanentemente todos os seus Veículos, Viagens, Caixas e Abastecimentos registrados. Essa ação NÃO poderá ser desfeita.'
            );

            if (!confirmacao) {
                e.preventDefault();
            }
        });
    }
});
















/* ==========================================================================
   ARQUIVO: app/static/js/content.js
   MÓDULO: CONTROLE DE EXIBIÇÃO DE SALDO CENSURADO NA HOME
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Seleção dos elementos do Card do Caixa
    const btnToggle = document.getElementById('btnToggleCaixaHome');
    const valorOculto = document.getElementById('valorCaixaHome');
    const valorReal = document.getElementById('valorRealCaixaHome');

    if (btnToggle && valorOculto && valorReal) {
        
        // Verifica preferência salva no navegador (padrão: oculta)
        const saldoVisivel = localStorage.getItem('saldo_visivel_home') === 'true';

        function atualizarExibicao(mostrar) {
            if (mostrar) {
                valorOculto.classList.add('desativado-home');
                valorReal.classList.remove('desativado-home');
                btnToggle.textContent = '🙈'; // Ícone de ocultar
                btnToggle.title = 'Ocultar valor';
            } else {
                valorReal.classList.add('desativado-home');
                valorOculto.classList.remove('desativado-home');
                btnToggle.textContent = '👁️'; // Ícone de mostrar
                btnToggle.title = 'Mostrar valor';
            }
        }

        // Aplica o estado inicial
        atualizarExibicao(saldoVisivel);

        // Evento de clique no botão
        btnToggle.addEventListener('click', function() {
            const estadoAtual = valorReal.classList.contains('desativado-home');
            atualizarExibicao(estadoAtual);
            localStorage.setItem('saldo_visivel_home', estadoAtual);
        });
    }
});