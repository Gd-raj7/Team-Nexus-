"""
CivicNexus AI — Unified Incident State Architecture
Every autonomous agent reads/writes a single shared IncidentContext contract.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


# ─── Enums ──────────────────────────────────────────────────────────────────────

class IncidentStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ASSIGNED = "ASSIGNED"
    ACTION_IN_PROGRESS = "ACTION_IN_PROGRESS"
    AWAITING_RESOLUTION_EVIDENCE = "AWAITING_RESOLUTION_EVIDENCE"
    RESOLUTION_REVIEW = "RESOLUTION_REVIEW"
    RESOLVED = "RESOLVED"
    REOPENED = "REOPENED"
    ESCALATED = "ESCALATED"


class IssueType(str, Enum):
    POTHOLE = "POTHOLE"
    WATER_LEAKAGE = "WATER_LEAKAGE"
    WATERLOGGING = "WATERLOGGING"
    GARBAGE_OVERFLOW = "GARBAGE_OVERFLOW"
    BROKEN_STREETLIGHT = "BROKEN_STREETLIGHT"
    DRAINAGE_PROBLEM = "DRAINAGE_PROBLEM"
    ROAD_DAMAGE = "ROAD_DAMAGE"
    EXPOSED_WIRES = "EXPOSED_WIRES"
    SEWAGE_OVERFLOW = "SEWAGE_OVERFLOW"
    DRAIN_BLOCKAGE = "DRAIN_BLOCKAGE"


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ReportStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    LINKED_TO_INCIDENT = "LINKED_TO_INCIDENT"
    RESOLVED = "RESOLVED"


class VerificationResult(str, Enum):
    RESOLUTION_VERIFIED = "RESOLUTION_VERIFIED"
    LOCATION_MISMATCH = "LOCATION_MISMATCH"
    POSSIBLE_FAILED_RESOLUTION = "POSSIBLE_FAILED_RESOLUTION"
    PENDING = "PENDING"


class IncidentClassification(str, Enum):
    INDEPENDENT_COMPLAINTS = "INDEPENDENT_COMPLAINTS"
    DUPLICATE_REPORTS = "DUPLICATE_REPORTS"
    POSSIBLE_CONNECTED_INCIDENT = "POSSIBLE_CONNECTED_INCIDENT"
    HIGH_CONFIDENCE_CONNECTED_INCIDENT = "HIGH_CONFIDENCE_CONNECTED_INCIDENT"


# ─── Sub-models ─────────────────────────────────────────────────────────────────

class Location(BaseModel):
    latitude: float
    longitude: float
    address: str = ""
    ward: str = ""


class CivicReport(BaseModel):
    """A single citizen complaint report in CivicNexus."""
    report_id: str
    timestamp: str
    citizen_name: str = "Anonymous Citizen"
    phone: str = ""
    location: Location
    description: str
    image_filename: str = ""
    status: str = ReportStatus.SUBMITTED
    linked_incident_id: Optional[str] = None
    ward: str = ""
    scenario_id: Optional[int] = None


class PerceptionResult(BaseModel):
    """Output of the Perception Agent."""
    report_id: str
    issue_type: str
    severity: str
    confidence: float
    evidence_text: str = ""
    image_filename: str = ""
    visual_evidence: List[str] = Field(default_factory=list)


class ClusterInfo(BaseModel):
    """Cluster metadata from the Geo-Temporal Clustering Engine."""
    radius_m: float = 0.0
    time_window_days: int = 0
    center_lat: float = 0.0
    center_lon: float = 0.0
    report_count: int = 0


class RootCause(BaseModel):
    """Output of the Root Cause Investigation Agent."""
    hypothesis: str = ""
    confidence: float = 0.0
    evidence: List[str] = Field(default_factory=list)
    chain: List[str] = Field(default_factory=list)
    disclaimer: str = (
        "AI-generated infrastructure incident hypothesis. "
        "Municipal physical site inspection recommended before final dispatch."
    )


class ImpactBreakdown(BaseModel):
    """Multi-factor breakdown of the civic threat score."""
    severity_score: float = 0.0
    infrastructure_proximity: float = 0.0
    people_affected: float = 0.0
    duration: float = 0.0
    repeat_reports: float = 0.0
    secondary_risk: float = 0.0


class ImpactScore(BaseModel):
    """Output of the Civic Impact Assessment Agent."""
    score: float = 0.0
    priority: str = Priority.LOW
    breakdown: ImpactBreakdown = Field(default_factory=ImpactBreakdown)
    explanation: str = ""


class EconomicImpact(BaseModel):
    """Output of the Municipal Economic Savings & Resource Optimizer Agent."""
    estimated_damage_if_neglected_inr: int = 0
    root_cause_fix_cost_inr: int = 0
    estimated_savings_inr: int = 0
    prevented_road_redigging_cycles: int = 0
    infrastructure_longevity_boost: str = "High"
    cost_benefit_summary: str = ""


class ResponseStep(BaseModel):
    """A single sequential step in a multi-department response plan."""
    step_number: int
    department: str
    department_name: str = ""
    action: str
    reason: str = ""
    estimated_hours: int = 0
    depends_on: List[int] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    issues: List[str] = Field(default_factory=list)


class ResponsePlan(BaseModel):
    """Output of the Response Orchestration Agent."""
    steps: List[ResponseStep] = Field(default_factory=list)
    rationale: str = ""
    approved: bool = False
    approved_by: str = ""
    approved_at: str = ""


class Resolution(BaseModel):
    """Resolution verification audit contract."""
    before_photo: str = ""
    after_photo: str = ""
    before_gps: Optional[Location] = None
    after_gps: Optional[Location] = None
    submitted_at: str = ""
    verification_result: str = VerificationResult.PENDING
    verification_details: str = ""
    confidence: float = 0.0
    verified_by_agent: bool = False


class SLA(BaseModel):
    """SLA tracking for an incident."""
    deadline: str = ""
    reminders_sent: int = 0
    escalated: bool = False
    escalation_reason: str = ""
    original_deadline: str = ""


class AgentLogEntry(BaseModel):
    """Explainable AI audit trail."""
    timestamp: str
    agent: str
    message: str
    decision: str = ""
    evidence_used: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    recommended_action: str = ""


class MemoryProfile(BaseModel):
    """Civic memory, spatial recurrence, and historical intervention logs."""
    total_historical_reports: int = 0
    chronic_recurrence_score: float = 0.0
    primary_vulnerability: str = "General Infrastructure"
    civic_memory_insight: str = "First recorded incident at this location."
    historical_incidents: List[dict] = Field(default_factory=list)
    past_interventions: List[dict] = Field(default_factory=list)


# ─── Unified Shared State ───────────────────────────────────────────────────────

class IncidentContext(BaseModel):
    """The central unified state contract for CivicNexus AI."""
    incident_id: str
    status: str = IncidentStatus.SUBMITTED
    classification: str = IncidentClassification.INDEPENDENT_COMPLAINTS
    created_at: str = ""
    updated_at: str = ""
    connected_reports: List[str] = Field(default_factory=list)
    cluster: ClusterInfo = Field(default_factory=ClusterInfo)
    perception_results: List[PerceptionResult] = Field(default_factory=list)
    root_cause: RootCause = Field(default_factory=RootCause)
    impact_score: ImpactScore = Field(default_factory=ImpactScore)
    economic_impact: EconomicImpact = Field(default_factory=EconomicImpact)
    memory_profile: MemoryProfile = Field(default_factory=MemoryProfile)
    response_plan: ResponsePlan = Field(default_factory=ResponsePlan)
    resolution: Resolution = Field(default_factory=Resolution)
    sla: SLA = Field(default_factory=SLA)
    agent_log: List[AgentLogEntry] = Field(default_factory=list)
    scenario_id: Optional[int] = None


# ─── API Requests / Responses ───────────────────────────────────────────────────

class SubmitReportRequest(BaseModel):
    citizen_name: str = "Anonymous Citizen"
    phone: str = ""
    latitude: float
    longitude: float
    address: str = ""
    ward: str = ""
    description: str
    image_filename: str = ""


class SubmitReportResponse(BaseModel):
    report_id: str
    status: str
    message: str
    timestamp: str


class ResolutionSubmission(BaseModel):
    after_photo: str
    after_latitude: float
    after_longitude: float
    notes: str = ""


class AdvanceDemoTimeRequest(BaseModel):
    hours: int = 72


class DashboardStats(BaseModel):
    total_reports: int = 0
    total_incidents: int = 0
    active_incidents: int = 0
    critical_incidents: int = 0
    resolved_incidents: int = 0
    reopened_incidents: int = 0
    escalated_incidents: int = 0
    total_estimated_savings_inr: int = 0

