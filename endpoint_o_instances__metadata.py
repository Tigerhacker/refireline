from endpoint_o_instances_register import _create_instance

def handler(request, match):
    from dbops_mysql import DB
    db = DB()

    iid = match.group(1)
    # technically we should only query the db, but it may cause issues as servers 
    # will already have an id from the real fireline
    name = _create_instance(iid) 

    db.createInstance(iid, name)
    response = {
        'attributes' : {},
        'display_name': name,
        'owner': '25721053-ebe8-59f1-95b3-de39bc253c7f'
    }
    return (200, response, {})

