from ._common import register_fixer


@register_fixer("castilla_la_mancha", 2011, 5)
def fix_castilla_la_mancha_2011_05(text: str) -> str:
    text = text.replace(
        "4. DON DAVID PARDO MOYA\n5. DOÑA MARIA ELENA ESCOBAR GUERRERO\n6. DON PABLO JESUS CANO DURAN",
        "1. DON DAVID PARDO MOYA\n2. DOÑA MARIA ELENA ESCOBAR GUERRERO\n3. DON PABLO JESUS CANO DURAN",
    )
    return text


@register_fixer("castilla_la_mancha", 2015, 5)
def fix_castilla_la_mancha_2015_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "Candidatura núm.: 9. PARTIDO CASTELLANO (PCAS)",
        "Candidatura núm.: 9. PARTIDO CASTELLANO-UNIDAD CASTELLANA (PCAS-UdCA)",
    )
    return text


@register_fixer("castilla_la_mancha", 2023, 5)
def fix_castilla_la_mancha_2023_05(text: str) -> str:
    # Fix dangling suplentes
    text = text.replace("SUPLENTES:\nY para que conste", "")
    return text
