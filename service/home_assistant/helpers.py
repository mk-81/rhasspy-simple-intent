def get_domain_from_entity_id(entity_id):
    parts = entity_id.split(".",1)
    if len(parts) == 2:
        return parts[0]
    else:
        return None

def entity_name_contains_domain(entity_id, domain_name):
    return entity_id.startswith(domain_name + ".")

def entity_name_add_domain(entity_id, domain_name):
    if domain_name != None and not entity_name_contains_domain(entity_id, domain_name):
        return domain_name + "." + entity_id
    else:
        return entity_id