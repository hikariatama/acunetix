import dataclasses
import typing


@dataclasses.dataclass
class ReportTemplate:
    template_id: str
    group: str
    name: str
    accepted_sources: typing.Optional[typing.List[str]] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ReportTemplate":
        return cls(**data)

    def to_json(self) -> dict:
        data = dataclasses.asdict(self)

        if data["accepted_sources"] is None:
            data.pop("accepted_sources")

        return data


DEVELOPER = ReportTemplate(
    "11111111-1111-1111-1111-111111111111",
    "Standart Reports",
    "Developer",
)

QUICK = ReportTemplate(
    "11111111-1111-1111-1111-111111111112",
    "Standart Reports",
    "Quick",
)

EXECUTIVE_SUMMARY = ReportTemplate(
    "11111111-1111-1111-1111-111111111113",
    "Standart Reports",
    "Executive Summary",
)

AFFECTED_ITEMS = ReportTemplate(
    "11111111-1111-1111-1111-111111111115",
    "Standart Reports",
    "Affected Items",
)

COMPREHENSIVE = ReportTemplate(
    "11111111-1111-1111-1111-111111111126",
    "Standart Reports",
    "Comprehensive (New)",
)

HIPAA = ReportTemplate(
    "11111111-1111-1111-1111-111111111114",
    "Compliance Reports",
    "HIPAA",
)


SCAN_COMPARISON = ReportTemplate(
    "11111111-1111-1111-1111-111111111124",
    "Compliance Reports",
    "Scan Comparison",
)

CWE_SANS_TOP_25 = ReportTemplate(
    "11111111-1111-1111-1111-111111111116",
    "Compliance Reports",
    "CWE 2011",
)

ISO_27001 = ReportTemplate(
    "11111111-1111-1111-1111-111111111117",
    "Compliance Reports",
    "ISO 27001",
)

NIST_SP800_53 = ReportTemplate(
    "11111111-1111-1111-1111-111111111118",
    "Compliance Reports",
    "NIST SP800 53",
)

OWASP_TOP_10_2013 = ReportTemplate(
    "11111111-1111-1111-1111-111111111119",
    "Compliance Reports",
    "OWASP Top 10 2013",
)

OWASP_TOP_10_2017 = ReportTemplate(
    "11111111-1111-1111-1111-111111111125",
    "Compliance Reports",
    "OWASP Top 10 2017",
)

OWASP_TOP_10_2021 = ReportTemplate(
    "11111111-1111-1111-1111-111111111127",
    "Compliance Reports",
    "OWASP Top 10 2021",
)

PCI_DSS_3_2 = ReportTemplate(
    "11111111-1111-1111-1111-111111111120",
    "Compliance Reports",
    "PCI DSS 3.2",
)

SARBANES_OXLEY = ReportTemplate(
    "11111111-1111-1111-1111-111111111121",
    "Compliance Reports",
    "Sarbanes Oxley",
)

STIG_DISA = ReportTemplate(
    "11111111-1111-1111-1111-111111111122",
    "Compliance Reports",
    "STIG DISA",
)

WASC_THREAT_CLASSIFICATION = ReportTemplate(
    "11111111-1111-1111-1111-111111111123",
    "Compliance Reports",
    "WASC Threat Classification",
)

TEMPLATE_MAP = {
    DEVELOPER.template_id: DEVELOPER,
    QUICK.template_id: QUICK,
    EXECUTIVE_SUMMARY.template_id: EXECUTIVE_SUMMARY,
    AFFECTED_ITEMS.template_id: AFFECTED_ITEMS,
    COMPREHENSIVE.template_id: COMPREHENSIVE,
    HIPAA.template_id: HIPAA,
    SCAN_COMPARISON.template_id: SCAN_COMPARISON,
    CWE_SANS_TOP_25.template_id: CWE_SANS_TOP_25,
    ISO_27001.template_id: ISO_27001,
    NIST_SP800_53.template_id: NIST_SP800_53,
    OWASP_TOP_10_2013.template_id: OWASP_TOP_10_2013,
    OWASP_TOP_10_2017.template_id: OWASP_TOP_10_2017,
    OWASP_TOP_10_2021.template_id: OWASP_TOP_10_2021,
    PCI_DSS_3_2.template_id: PCI_DSS_3_2,
    SARBANES_OXLEY.template_id: SARBANES_OXLEY,
    STIG_DISA.template_id: STIG_DISA,
    WASC_THREAT_CLASSIFICATION.template_id: WASC_THREAT_CLASSIFICATION,
}
