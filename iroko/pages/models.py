#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

# from sqlalchemy_imageattach.entity import Image, image_attachment


# class Faq(db.Model):
#     __tablename__ = 'iroko_faq'

#     id = db.Column(db.Integer, primary_key=True)

#     question = db.Column(db.String, nullable=False, unique=True)
#     answer = db.Column(db.String, nullable=True)

#     def __str__(self):
#         """Representation."""
#         return self.question


# class IrokoNew(db.Model):
#     __tablename__ = 'iroko_news'

#     id = db.Column(db.Integer, primary_key=True)

#     published_by = db.Column(db.Integer, db.ForeignKey(User.id, name='fk_iroko_news_user_id'))
#     user = db.relationship(User, backref='iroko_news')

#     title = db.Column(db.String, nullable=False, unique=True)
#     summary = db.Column(db.String, nullable=True)
#     body = db.Column(db.String, nullable=False)
#     front_image =  image_attachment('NewsImage')
#     created_at = db.Column(db.DateTime)
#     published_until = db.Column(db.DateTime)

#     def __str__(self):
#         """Representation."""
#         return self.title


# class NewsImage(db.Model, Image):
#     new_id = db.Column(db.Integer, db.ForeignKey('iroko_new.id'), primary_key=True)
#     iroko_new = db.relationship('IrokoNew')
#     __tablename__ = 'new_picture'
