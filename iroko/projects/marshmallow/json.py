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
from marshmallow import INCLUDE, fields, missing, validate

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


class TitleTypeEnum(Enum):
    ALT = "AlternativeTitle"
    SUBT = "Subtitle"
    TRANST = "TranslatedTitle"
    OTHER = "Other"


class NameTypeEnum(Enum):
    ORG = "Organizational"
    PER = "Personal"


class ContributorTypeEnum(Enum):
    CONTP = "ContactPerson"
    DATCL = "DataCollector"
    DATCR = "DataCurator"
    DATM = "DataManager"
    DIST = "Distributor"
    EDIT = "Editor"
    HOSTINS = "HostingInstitution"
    PROD = "Producer"
    PROJL = "ProjectLeader"
    PROJM = "ProjectManager"
    PROJMEM = "ProjectMember"
    REGAG = "RegistrationAgency"
    REGAUTH = "RegistrationAuthority"
    RELPER = "RelatedPerson"
    RESEARCH = "Researcher"
    REESEARCHG = "ResearchGroup"
    RIGHTHOLD = "RightsHolder"
    SPONSOR = "Sponsor"
    SUPERV = "Supervisor"
    WORKPACKLEAD = "WorkPackageLeader"
    OTHER = "Other"


class FundTypeEnum(Enum):
    ISNI = "ISNI"
    GRID = "GRID"
    CF = "Crossref Funder"


class AlternateIdTypeEnum(Enum):
    ARK = "ARK"
    ARXIV = "arXiv"
    BIBCODE = "bibcode"
    DOI = "DOI"
    EAN13 = "EAN13"
    EISSN = "EISSN"
    HANDLE = "Handle"
    IGSN = "IGSN"
    ISBN = "ISBN"
    ISSN = "ISSN"
    ISTC = "ISTC"
    LISSN = "LISSN"
    LSID = "LSID"
    PISSN = "PISSN"
    PMID = "PMID"
    PURL = "PURL"
    UPC = "UPC"
    URL = "URL"
    URN = "URN"
    WOS = "WOS"


class DateTypeEnum(Enum):
    ACCEPTED = "Accepted"
    AVAILABLE = "Available"
    ISSUED = "Issued"


class ResourceTypeEnum(Enum):
    LITERATURE = "literature"
    DATASET = "dataset"
    SOFTWARE = "software"
    OTHER = "other research product"


class IdentifierTypeEnum(Enum):
    ARK = "ARK"
    DOI = "DOI"
    HANDLE = "Hanlde"
    PURL = "PURL"
    URL = "URL"
    URN = "URN"


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


class TitleSchemaV1(StrictKeysMixin):
    title = SanitizedUnicode()
    lang = SanitizedUnicode()
    titleType = fields.Enum(TitleTypeEnum, by_value=True)


class IdentifierSchemaV1(StrictKeysMixin):
    idType = fields.Enum(IdentifierTypeEnum, by_value=True)
    value = SanitizedUnicode()


class AfiliationsSchemaV1(StrictKeysMixin):
    id = SanitizedUnicode()
    identifiers = Nested(IdentifierSchemaV1, many=True)


class CreatorSchemaV1(StrictKeysMixin):
    creatorName = SanitizedUnicode(required=True)
    # nameType = fields.Enum(NameTypeEnum, by_value=True)
    # givenName = SanitizedUnicode(required=True)
    # familyName = SanitizedUnicode(required=True)
    # id = SanitizedUnicode(required=True)
    # identifiers = Nested(IdentifierSchemaV1, many=True)
    # affiliations = Nested(AfiliationsSchemaV1, many=True)


class ContributorSchemaV1(StrictKeysMixin):
    contributorType = fields.Enum(
        ContributorTypeEnum, by_value=True, required=True)
    contributorName = SanitizedUnicode(required=True)
    nameType = fields.Enum(NameTypeEnum, by_value=True)
    givenName = SanitizedUnicode()
    familyName = SanitizedUnicode()
    id = SanitizedUnicode(required=True)
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
    awardURI = SanitizedUnicode(required=True)
    awardTitle = SanitizedUnicode()


class AlternateIdentifierSchemaV1(StrictKeysMixin):
    idValue = SanitizedUnicode()
    idType = fields.Enum(AlternateIdTypeEnum, by_value=True)


class RelatedIdentifierSchemaV1(StrictKeysMixin):
    idValue = SanitizedUnicode()
    IdType = fields.Enum(AlternateIdTypeEnum, by_value=True)


class DateRightsSchemaV1(StrictKeysMixin):
    dateValue = fields.DateTime()
    dateType = fields.Enum(DateTypeEnum, by_value=True)


class PublishDateSchemaV1(StrictKeysMixin):
    dateValue = fields.DateTime()
    dateType = fields.Enum(DateTypeEnum, by_value=True)


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
    title = Nested(TitleSchemaV1, many=True, )
    creator = Nested(CreatorSchemaV1, many=True, )
    # contributor = Nested(ContributorSchemaV1, many=True, )
    # fundingReference = Nested(FundingReferenceSchemaV1, many=True)
    # alternateIdentifier = Nested(AlternateIdentifierSchemaV1, many=True)
    # relatedIdentifier = Nested(RelatedIdentifierSchemaV1, many=True)
    # dateRights = Nested(DateRightsSchemaV1, many=True, max=2, min=2)
    # lenguaje = fields.List(SanitizedUnicode())
    # publisher = fields.List(SanitizedUnicode())
    # publishDate = Nested(PublishDateSchemaV1, many=False)
    # resourceType = Nested(ResourceTypeSchemaV1, many=False)
    # description = Nested(DescriptionSchemaV1, many=True)
    # format = fields.List(SanitizedUnicode())
    identifiers = Nested(IdentifierSchemaV1, many=False)
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
