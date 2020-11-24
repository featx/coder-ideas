


def _from_domain_property(domain_property):
    return {
        "id": domain_property.id,
        "code": domain_property.code,
        "name": domain_property.name,
        "type": domain_property.type,
        "sort": domain_property.sort,
        "domain_code": domain_property.domain_code,
        "project_code": domain_property.project_code
    }