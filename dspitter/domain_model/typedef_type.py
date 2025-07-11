from dspitter.domain_model import declaration_type

type TypedefAlias = (
    declaration_type.DeclarationType | declaration_type.DeclarationTypeFunction
)
