$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
        throw 'Instale o Node.js 20 ou superior para compilar o painel brasileiro.'
    }
    node -e "process.exit(Number(process.versions.node.split('.')[0]) >= 20 ? 0 : 1)"
    if ($LASTEXITCODE -ne 0) {
        throw 'Instale o Node.js 20 ou superior para compilar o painel brasileiro.'
    }
    $pnpm = Get-Command pnpm.cmd -ErrorAction SilentlyContinue
    $npx = Get-Command npx.cmd -ErrorAction SilentlyContinue
    if (-not $pnpm -and -not $npx) {
        throw 'Instale o npm (incluído no Node.js) ou o pnpm para compilar o painel.'
    }
    $pnpmVersion = '10.32.1'
    $runnerArgs = @()
    if ($pnpm) {
        $runner = $pnpm.Source
        $installedPnpmVersion = & $runner --version
        if ($LASTEXITCODE -ne 0) { throw 'Não foi possível executar o pnpm.' }
        if ($installedPnpmVersion.Trim() -ne $pnpmVersion) {
            $runnerArgs = @('dlx', "pnpm@$pnpmVersion")
        }
    } else {
        $runner = $npx.Source
        $runnerArgs = @('--yes', "pnpm@$pnpmVersion")
    }
    Push-Location (Join-Path $PSScriptRoot 'dashboard')
    try {
        foreach ($command in @(
            @('install', '--frozen-lockfile'),
            @('run', 'i18n:check'),
            @('run', 'i18n:check:ptbr'),
            @('run', 'build')
        )) {
            & $runner @runnerArgs @command
            if ($LASTEXITCODE -ne 0) { throw 'Falha ao preparar o painel brasileiro.' }
        }
    } finally { Pop-Location }
    $versionSource = Get-Content -LiteralPath 'astrbot/__init__.py' -Raw
    $version = [regex]::Match($versionSource, '__version__\s*=\s*"([^"]+)"').Groups[1].Value
    if (-not $version) { throw 'Não foi possível identificar a versão do AstrBot.' }
    if (-not (Test-Path -LiteralPath 'dashboard/dist/index.html' -PathType Leaf)) {
        throw 'A compilação não gerou dashboard/dist/index.html.'
    }
    New-Item -ItemType Directory -Path 'dashboard/dist/assets' -Force | Out-Null
    Set-Content -LiteralPath 'dashboard/dist/assets/version' -Value "v$version" -Encoding ascii
    Write-Host 'Painel brasileiro compilado e verificado.' -ForegroundColor Green
} finally { Pop-Location }
