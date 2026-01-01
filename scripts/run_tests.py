#!/usr/bin/env python3
"""
Script pour exécuter les tests d'intégration.

Ce script facilite l'exécution des différents types de tests :
- Tests d'intégration uniquement
- Tests unitaires uniquement  
- Tous les tests
- Avec ou sans couverture de code
"""

import subprocess
import sys
import argparse


def run_tests(test_type="all", coverage=False, verbose=True):
    """
    Exécute les tests selon les spécifications.
    
    Args:
        test_type: Type de tests à exécuter ('all', 'integration', 'unitary')
        coverage: Générer un rapport de couverture
        verbose: Mode verbeux
    """
    cmd = ["python", "-m", "pytest"]
    
    # Sélection des tests
    if test_type == "integration":
        cmd.append("../tests/test_integration.py")
    elif test_type == "unitary":
        cmd.extend(["../tests/", "-k", "not integration"])
    else:  # all
        cmd.append("../tests/")
    
    # Options
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=html"])
    
    print(f"Exécution de la commande: {' '.join(cmd)}")
    print("-" * 80)
    
    result = subprocess.run(cmd)
    
    if coverage:
        print("-" * 80)
        print("Rapport de couverture généré dans: htmlcov/index.html")
    
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Exécuteur de tests pour le projet MCP"
    )
    parser.add_argument(
        "--type", "-t",
        choices=["all", "integration", "unitary"],
        default="all",
        help="Type de tests à exécuter (default: all)"
    )
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Générer un rapport de couverture de code"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Mode silencieux (moins verbeux)"
    )
    
    args = parser.parse_args()
    
    return_code = run_tests(
        test_type=args.type,
        coverage=args.coverage,
        verbose=not args.quiet
    )
    
    sys.exit(return_code)


if __name__ == "__main__":
    main()