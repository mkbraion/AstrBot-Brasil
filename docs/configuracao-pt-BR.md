# Configuração — AstrBot Brasil

## Idioma

O dashboard desta edição usa `pt-BR` como padrão. O idioma pode ser trocado pelo seletor da interface e a preferência fica salva no navegador.

## Provedor de IA

Configure o provedor pelo dashboard. Dependendo do serviço, você precisará informar API key, endpoint e modelo.

Nunca salve credenciais reais em arquivos versionados.

## Segurança do Agent

Antes de permitir acesso ao computador, revise cuidadosamente as opções disponíveis. Permissões de shell, Python e sistema de arquivos aumentam a capacidade do Agent e também o impacto potencial de uma configuração incorreta.

## Métricas

Quando suportado pelo runtime, as métricas anônimas podem ser desativadas com:

```powershell
$env:ASTRBOT_DISABLE_METRICS = "1"
```

Para uma configuração persistente no Windows, use as ferramentas de variáveis de ambiente do sistema e reinicie o terminal.
