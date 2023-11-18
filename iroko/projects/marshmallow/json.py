# -*- coding: utf-8 -*-

#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

#
#
# Iroko is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function
from enum import Enum
from re import L


from invenio_jsonschemas import current_jsonschemas
from invenio_records_rest.schemas import Nested, StrictKeysMixin
from invenio_records_rest.schemas.fields import (
    DateString, GenFunction,
    PersistentIdentifier, SanitizedUnicode,
)
from marshmallow import INCLUDE, fields, missing, validate, Schema

from iroko.projects.api import ProjectRecord

allow_empty = validate.Length(min=0)


def bucket_from_context(_, context):
    """Get the record's bucket from context."""
    record = (context or {}).get('record', {})
    return record.get('_bucket', missing)


def files_from_context(_, context):
    """Get the record's files from context."""
    record = (context or {}).get('record', {})
    return record.get('_files', missing)


def schema_from_context(_, context):
    """Get the record's schema from context."""
    record = (context or {}).get('record', {})
    return record.get(
        "_schema",
        current_jsonschemas.path_to_url(ProjectRecord._schema)
    )


"""Declarando Propiedades de Project Schema"""
"""Enums Here"""


TitleTypeEnum=["AlternativeTitle","Subtitle","TranslatedTitle","Other"]


class NameTypeEnum(Enum):
    ORG = "Organizational"
    PER = "Personal"


ContributorTypeEnum=["ContactPerson","DataCollector","DataCurator","DataManager","Distributor","Editor","HostingInstitution","Producer","ProjectLeader","ProjectManager"
    ,"ProjectMember"
    ,"RegistrationAgency"
    ,"RegistrationAuthority"
   ,"RelatedPerson"
    ,"Researcher"
    ,"ResearchGroup"
    ,"RightsHolder"
    ,"Sponsor"
    ,"Supervisor"
    ,"WorkPackageLeader"
   ,"Other"]


class FundTypeEnum(Enum):
    ISNI = "ISNI"
    GRID = "GRID"
    CF = "Crossref Funder"


AlternateIdTypeEnum=["ARK","arXiv","bibcode","DOI","EAN13","EISSN","Handle","IGSN","ISBN","ISSN","ISTC","LISSN","LSID","PISSN","PMID","PURL","UPC","URL","URN","WOS"]


DateTypeEnum=["Accepted","Available", "Issued",]

class ResourceTypeEnum(Enum):
    LITERATURE = "literature"
    DATASET = "dataset"
    SOFTWARE = "software"
    OTHER = "other research product"


IdentifierTypeEnum=["ARK","DOI","Hanlde","PURL","URL","URN"]


class ObjectTypeEnum(Enum):
    FULLTEXT = "fulltext"
    DATASET = "dataset"
    SOFTWARE = "software"
    OTHER = "other"


"""End Enums"""


class NameIdentifierSchemaV1(StrictKeysMixin):
    value = SanitizedUnicode(required=True)
    schemeURI = SanitizedUnicode()
    affiliation = fields.List(SanitizedUnicode())


class TitleSchemaV1(Schema):
    title = fields.Str(validate=validate.Length(min=3))
    lang = SanitizedUnicode()
    titleType = fields.Str(validate=validate.OneOf(choices=TitleTypeEnum))


class IdentifierSchemaV1(StrictKeysMixin):
    idtype = fields.Str(validate=validate.OneOf(choices=IdentifierTypeEnum))
    value = SanitizedUnicode()


class AfiliationsSchemaV1(StrictKeysMixin):
    id = SanitizedUnicode()
    identifiers = Nested(IdentifierSchemaV1, many=True)


class CreatorSchemaV1(StrictKeysMixin):
    creatorName = SanitizedUnicode(required=True)
    nameType = fields.Enum(NameTypeEnum, by_value=True)
    givenName = SanitizedUnicode(required=True)
    familyName = SanitizedUnicode(required=True)
    #id = SanitizedUnicode(required=True)
    identifiers = Nested(IdentifierSchemaV1, many=True)
    affiliations = Nested(AfiliationsSchemaV1, many=True)


class ContributorSchemaV1(StrictKeysMixin):
    contributorType = fields.Str( validate=validate.OneOf(ContributorTypeEnum), required=True)
    contributorName = SanitizedUnicode(required=True)
    nameType = fields.Enum(NameTypeEnum, by_value=True)
    givenName = SanitizedUnicode()
    familyName = SanitizedUnicode()
    # id = SanitizedUnicode(required=True)
    identifiers = Nested(IdentifierSchemaV1, many=True)
    affiliations = Nested(AfiliationsSchemaV1, many=True)


class FunderIdentifierSchemeV1(StrictKeysMixin):
    fundType = fields.Enum(FundTypeEnum, by_value=True)
    fundValue = SanitizedUnicode()


class FundingReferenceSchemaV1(StrictKeysMixin):
    founderName = SanitizedUnicode(required=True)
    funderIdentifier = Nested(FunderIdentifierSchemeV1)
    fundingStream = SanitizedUnicode()
    awardNumber = SanitizedUnicode(required=True)
    awardURI = SanitizedUnicode(required=True, validate=validate.URL())
    awardTitle = SanitizedUnicode()


class AlternateIdentifierSchemaV1(StrictKeysMixin):
    idValue = SanitizedUnicode(required=True)
    idType = fields.Str(validate=validate.OneOf(AlternateIdTypeEnum), required=True)


class RelatedIdentifierSchemaV1(StrictKeysMixin):
    idValue = SanitizedUnicode()
    idType = fields.Str(validate=validate.OneOf(AlternateIdTypeEnum))


class DateRightsSchemaV1(StrictKeysMixin):
    dateValue = fields.DateTime()
    dateType = SanitizedUnicode(validate=validate.OneOf(DateTypeEnum), required=True)


class PublishDateSchemaV1(StrictKeysMixin):
    dateValue = fields.Date( required=True)
    dateType = SanitizedUnicode(validate=validate.OneOf(DateTypeEnum), required=True)


class ResourceTypeSchemaV1(StrictKeysMixin):
    resourceTypeGeneral = fields.Enum(ResourceTypeEnum, by_value=True)
    uri = SanitizedUnicode(validate=validate.URL())


class DescriptionSchemaV1(StrictKeysMixin):
    descValue = SanitizedUnicode()
    lang = SanitizedUnicode()


class RightsSchemeV1(StrictKeysMixin):
    rightsValue = SanitizedUnicode()
    rightsUri = SanitizedUnicode(validate=validate.URL())


class SubjectSchemeV1(StrictKeysMixin):
    subjectValue = SanitizedUnicode()
    subjectScheme = SanitizedUnicode()
    subjectURI = SanitizedUnicode()
    valueURI = SanitizedUnicode()


class LicenseConditionSchemeV1(StrictKeysMixin):
    licenseValue = SanitizedUnicode()
    uri = SanitizedUnicode(required=True)
    startDate = fields.DateTime(required=True)


class GeolocationPointSchemeV1(StrictKeysMixin):
    pointLongitude = fields.Float()
    pointAltitude = fields.Float()


class GeolocationBoxSchemeV1(StrictKeysMixin):
    westBoundLongitude = fields.Float()
    eastBoundLongitude = fields.Float()
    southBoundLatitude = fields.Float()
    northBoundLatitude = fields.Float()


class PolygonPointSchemeV1(StrictKeysMixin):
    pointLongitude = fields.Float()
    pointLatitude = fields.Float()


class InPolygonPointSchemeV1(StrictKeysMixin):
    pointLongitude = fields.Float()
    pointLatitude = fields.Float()


class GeolocationPolygonSchemeV1(StrictKeysMixin):
    polygonPoint = Nested(PolygonPointSchemeV1, many=True, min=4)
    inPolygonPoint = Nested(InPolygonPointSchemeV1, many=False)


class GeoLocationSchemeV1(StrictKeysMixin):
    geoLocationPoint = Nested(GeolocationPointSchemeV1, many=False)
    geoLocationBox = Nested(GeolocationBoxSchemeV1, many=False)
    geoLocationPlace = SanitizedUnicode()
    geoLocationPolygon = Nested(GeolocationPolygonSchemeV1, many=False)


class VersionSchemeV1(StrictKeysMixin):
    versionValue = SanitizedUnicode()
    uri = SanitizedUnicode(validate=validate.URL())


class FileSchemeV1(StrictKeysMixin):
    fileValue = SanitizedUnicode(validate=validate.URL())
    accessRightsURI = SanitizedUnicode(validate=validate.URL())
    mimeType = SanitizedUnicode()
    objectType = fields.Enum(ObjectTypeEnum, by_value=True)


"""Fin de la Declaracion de Project Schema"""


class ProjectMetadataSchemaV1(StrictKeysMixin):
    """Schema for the record metadata."""

    id = PersistentIdentifier()
    title = Nested(TitleSchemaV1, many=True, required=True )
    creator = Nested(CreatorSchemaV1, many=True, required=True )
    contributor = Nested(ContributorSchemaV1, many=True, required=True )
    fundingReference = Nested(FundingReferenceSchemaV1, many=True,min=1)
    alternateIdentifier = Nested(AlternateIdentifierSchemaV1, many=True)
    relatedIdentifier = Nested(RelatedIdentifierSchemaV1, many=True, required=True)
    dateRights = Nested(DateRightsSchemaV1, many=True, max=2, min=2)
    lenguaje = fields.List(SanitizedUnicode(),required=True, min=1)
    publisher = fields.List(SanitizedUnicode(), required=True, min=1)
    publishDate = Nested(PublishDateSchemaV1, many=False, required=True)
    # resourceType = Nested(ResourceTypeSchemaV1, many=False)
    # description = Nested(DescriptionSchemaV1, many=True)
    # format = fields.List(SanitizedUnicode())
    identifiers = Nested(IdentifierSchemaV1, many=True, required=True)
    # rights = Nested(RightsSchemeV1)
    # source = fields.List(SanitizedUnicode())
    # subject = Nested(SubjectSchemeV1, many=True)
    # licenseCondition = Nested(LicenseConditionSchemeV1, many=False)
    # coverage = fields.List(fields.DateTime, min=2, max=2)
    # size = fields.List(SanitizedUnicode())
    # geoLocation = Nested(GeoLocationSchemeV1, many=True)
    # version = Nested(VersionSchemeV1, many=False)
    # file = Nested(FileSchemeV1, many=True)
    # citationTitle = SanitizedUnicode()
    # citationVolume = fields.Number()
    # citationIssue = fields.Number()
    # citationStartPage = fields.Number()
    # citationEndPage = fields.Number()
    # citationEdition = fields.Number()
    # citationConferencePlace = SanitizedUnicode()
    # citationConferenceDate = fields.DateTime()
    # audience = fields.List(SanitizedUnicode())
    _schema = GenFunction(
        attribute="$schema",
        data_key="$schema",
        deserialize=schema_from_context,  # to be added only when loading
    )


class ProjectRecordSchemaV1(StrictKeysMixin):
    """Record schema."""
    metadata = fields.Nested(ProjectMetadataSchemaV1)
    created = fields.Str(dump_only=True)
    revision = fields.Integer(dump_only=True)
    updated = fields.Str(dump_only=True)
    links = fields.Dict(dump_only=True)
    id = PersistentIdentifier()
    files = GenFunction(
        serialize=files_from_context, deserialize=files_from_context)


projectMetadataSchema = ProjectMetadataSchemaV1(many=False, unknown=INCLUDE)
