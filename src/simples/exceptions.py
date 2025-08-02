"""
Exceções personalizadas para o módulo simples.
"""

class GrafoGenerationError(Exception):
    """Exceção base para erros de geração de grafos."""
    pass


class ParametrosInvalidosError(GrafoGenerationError):
    """Exceção para parâmetros inválidos."""
    pass


class TentativasExcedidasError(GrafoGenerationError):
    """Exceção para quando o número máximo de tentativas é excedido."""
    pass


class ArestasInsuficientesError(GrafoGenerationError):
    """Exceção para quando não há arestas suficientes."""
    pass


class ComponentesInvalidasError(GrafoGenerationError):
    """Exceção para configurações inválidas de componentes."""
    pass 