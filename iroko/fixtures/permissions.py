

def iroko_permissions():

    #concediendo acceso a un usuario, puede ser por rol# 1- si es por usuario hay q obtener el usuario, si es por rol igual# 
    eduardo = db.session.query(User).filter_by(email="eduardo.arencibia@upr.edu.cu").first()
    # 2- agregar a la base de datos de access# 
    db.session.add(ActionUsers.allow(vocabulary_create_permission, user=eduardo))
    db.session.commit()