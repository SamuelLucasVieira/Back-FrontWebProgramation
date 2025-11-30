#!/usr/bin/env python
"""
Script auxiliar para executar testes de forma conveniente.
"""
import sys
import subprocess
import argparse


def run_tests(marker=None, file=None, verbose=False, coverage=False, watch=False):
    """Executa os testes com as opções especificadas."""
    cmd = ["pytest"]
    
    if verbose:
        cmd.append("-vv")
    else:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term-missing"])
    
    if marker:
        cmd.extend(["-m", marker])
    
    if file:
        cmd.append(file)
    
    if watch:
        cmd.insert(0, "pytest-watch")
        cmd.remove("pytest")
    
    print(f"Executando: {' '.join(cmd)}")
    print("-" * 60)
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Executa testes do projeto")
    parser.add_argument(
        "-m", "--marker",
        help="Executa apenas testes com o marcador especificado (ex: repository, service, api)"
    )
    parser.add_argument(
        "-f", "--file",
        help="Executa apenas o arquivo de teste especificado"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verboso (mais detalhes)"
    )
    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Gera relatório de cobertura"
    )
    parser.add_argument(
        "-w", "--watch",
        action="store_true",
        help="Modo watch (re-executa quando arquivos mudam)"
    )
    
    args = parser.parse_args()
    
    exit_code = run_tests(
        marker=args.marker,
        file=args.file,
        verbose=args.verbose,
        coverage=args.coverage,
        watch=args.watch
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

