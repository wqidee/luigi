# Checklist para Deploy no Hostinger

## ✅ CORREÇÕES FEITAS

1. ✅ **Basename React Router**: Configurado para `basename="/ger"`
2. ✅ **Caminhos no index.html**: Atualizados para `/ger/static/js/...` e `/ger/static/css/...`
3. ✅ **Script Prisma**: Substituído para `neutrawave.online`

## 📁 ESTRUTURA DE ARQUIVOS NECESSÁRIA

Quando hospedar, a estrutura deve ser:

```
/public_html/ger/
├── index.html          ← Este arquivo (com caminhos corrigidos)
├── favicon.ico
├── robots.txt
└── static/
    ├── js/
    │   └── main.1cbf12b5.js  ← Com basename="/ger" e script Neutrawave
    ├── css/
    │   └── main.39a66c43.css
    └── media/
        └── (todos os arquivos de imagem)
```

## ⚠️ PROBLEMAS COMUNS

### Tela Branca - Possíveis Causas:

1. **Caminhos incorretos dos arquivos estáticos**
   - ✅ CORRIGIDO: index.html agora aponta para `/ger/static/...`

2. **JavaScript com erro no console**
   - Abrir DevTools (F12) e verificar erros no Console
   - Verificar Network tab para ver se arquivos estão sendo carregados

3. **Estrutura de pastas errada no servidor**
   - Certifique-se que NÃO há pasta `ger/ger/` (pasta duplicada)
   - Os arquivos devem estar em `/public_html/ger/` direto

4. **Cache do navegador**
   - Fazer hard refresh: Ctrl+Shift+R (Windows) ou Cmd+Shift+R (Mac)

## 🔍 VERIFICAÇÕES

Após fazer upload, verificar:

1. ✅ `index.html` está em `/public_html/ger/index.html`
2. ✅ `static/` está em `/public_html/ger/static/`
3. ✅ Não há pasta `ger/` duplicada dentro de `ger/`
4. ✅ Todos os arquivos foram enviados corretamente
5. ✅ Permissões dos arquivos estão corretas (644 para arquivos, 755 para pastas)

## 📝 NOTAS

- URL de acesso: `https://darkgreen-kangaroo-804914.hostingersite.com/ger/`
- O React Router está configurado com `basename="/ger"`, então todas as rotas funcionam em `/ger/*`
- O script do Prisma/Neutrawave carrega automaticamente quando a página abre
