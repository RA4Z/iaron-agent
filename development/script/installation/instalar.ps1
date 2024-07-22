# Instala o Poetry
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Define o caminho para a pasta Scripts do Python
$pythonScriptsPath = "$env:APPDATA\Python\Scripts"

# Obtém as variáveis de ambiente existentes
$pathEnv = [System.Environment]::GetEnvironmentVariable("PATH", "Machine")

# Verifica se o caminho para a pasta Scripts do Python já existe nas variáveis de ambiente
if ($pathEnv -notlike "*$pythonScriptsPath*") {
    # Adiciona o caminho para a pasta Scripts do Python às variáveis de ambiente existentes
    $newPathEnv = $pathEnv + ";" + $pythonScriptsPath
    [System.Environment]::SetEnvironmentVariable("PATH", $newPathEnv, "Machine")

    # Exibe uma mensagem de sucesso
    Write-Host "Variável de ambiente PATH atualizada com sucesso."
} else {
    # Exibe uma mensagem informando que o caminho já existe
    Write-Host "O caminho '$pythonScriptsPath' já existe nas variáveis de ambiente PATH."
}

# Reinicia o terminal para aplicar as alterações nas variáveis de ambiente
$host.Quit()