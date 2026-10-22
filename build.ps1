$ErrorActionPreference = 'Stop'
$windowsPath = $PSScriptRoot.Replace('\', '/')
$sourcePath = (& wsl.exe -d CompilerLab -- wslpath -a $windowsPath | Out-String).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Source path conversion failed' }
$buildPath = '/opt/compiler-lab/build/pr001'
& wsl.exe -d CompilerLab -u root -- cmake -S $sourcePath -B $buildPath -G Ninja -DCMAKE_BUILD_TYPE=Debug
if ($LASTEXITCODE -ne 0) { throw 'CMake configuration failed' }
& wsl.exe -d CompilerLab -u root -- cmake --build $buildPath -j 4
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
& wsl.exe -d CompilerLab -u root -- ctest --test-dir $buildPath --output-on-failure
if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }
