"""
Change Tracker - Real-time ATS Preview Feature
Tracks every single modification made during optimization for interactive review
Author: Built for ApplyTune's next-level UX
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class ChangeType(Enum):
    """Types of changes we can make"""
    KEYWORD_ADDED = "keyword_added"
    SKILL_ADDED = "skill_added"
    SKILL_REMOVED = "skill_removed"
    CONTENT_ENHANCED = "content_enhanced"
    BULLET_MODIFIED = "bullet_modified"

class ChangeStatus(Enum):
    """Validation status of each change"""
    ACCEPTED = "accepted"  # Passed all validation layers
    REJECTED = "rejected"  # Failed validation
    PENDING = "pending"    # Not yet validated

@dataclass
class Change:
    """
    Represents a single atomic change made to the resume
    """
    id: str  # Unique identifier for this change
    type: ChangeType
    status: ChangeStatus
    
    # What changed
    original_text: str
    modified_text: str
    
    # Context
    section: str  # e.g., "Experience - Citi", "Projects - Bull Mart"
    bullet_index: Optional[int] = None
    
    # Why it changed
    reason: str = ""  # e.g., "Added missing keyword: Kubernetes"
    keywords_added: List[str] = None
    
    # Validation details
    validation_layers_passed: List[str] = None
    validation_warnings: List[str] = None
    
    # Impact on ATS score
    ats_impact: float = 0.0  # Estimated % improvement
    
    def __post_init__(self):
        if self.keywords_added is None:
            self.keywords_added = []
        if self.validation_layers_passed is None:
            self.validation_layers_passed = []
        if self.validation_warnings is None:
            self.validation_warnings = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for JSON serialization"""
        return {
            "id": self.id,
            "type": self.type.value,
            "status": self.status.value,
            "original_text": self.original_text,
            "modified_text": self.modified_text,
            "section": self.section,
            "bullet_index": self.bullet_index,
            "reason": self.reason,
            "keywords_added": self.keywords_added,
            "validation_layers_passed": self.validation_layers_passed,
            "validation_warnings": self.validation_warnings,
            "ats_impact": self.ats_impact
        }

class ChangeTracker:
    """
    Tracks all changes made during resume optimization
    Enables interactive review and undo functionality
    """
    
    def __init__(self):
        self.changes: List[Change] = []
        self._change_counter = 0
    
    def track_bullet_modification(
        self,
        original: str,
        modified: str,
        section: str,
        bullet_index: int,
        keywords_added: List[str],
        validation_result: Dict[str, Any],
        ats_impact: float = 0.0
    ) -> str:
        """
        Track a bullet point modification
        Returns the change ID
        """
        self._change_counter += 1
        change_id = f"change_{self._change_counter}"
        
        # Determine status from validation
        status = ChangeStatus.ACCEPTED if validation_result.get("is_valid", True) else ChangeStatus.REJECTED
        
        # Build reason string
        if keywords_added:
            reason = f"Added keywords: {', '.join(keywords_added)}"
        else:
            reason = "Content enhanced for ATS compatibility"
        
        change = Change(
            id=change_id,
            type=ChangeType.BULLET_MODIFIED,
            status=status,
            original_text=original,
            modified_text=modified,
            section=section,
            bullet_index=bullet_index,
            reason=reason,
            keywords_added=keywords_added,
            validation_layers_passed=validation_result.get("layers_passed", []),
            validation_warnings=validation_result.get("warnings", []),
            ats_impact=ats_impact
        )
        
        self.changes.append(change)
        return change_id
    
    def track_skill_addition(
        self,
        skill: str,
        section: str,
        reason: str,
        ats_impact: float = 0.0
    ) -> str:
        """Track a skill being added"""
        self._change_counter += 1
        change_id = f"change_{self._change_counter}"
        
        change = Change(
            id=change_id,
            type=ChangeType.SKILL_ADDED,
            status=ChangeStatus.ACCEPTED,
            original_text="",
            modified_text=skill,
            section=section,
            reason=reason,
            keywords_added=[skill],
            ats_impact=ats_impact
        )
        
        self.changes.append(change)
        return change_id
    
    def track_skill_removal(
        self,
        skill: str,
        section: str,
        reason: str
    ) -> str:
        """Track a skill being removed"""
        self._change_counter += 1
        change_id = f"change_{self._change_counter}"
        
        change = Change(
            id=change_id,
            type=ChangeType.SKILL_REMOVED,
            status=ChangeStatus.ACCEPTED,
            original_text=skill,
            modified_text="",
            section=section,
            reason=reason,
            ats_impact=0.0
        )
        
        self.changes.append(change)
        return change_id
    
    def get_accepted_changes(self) -> List[Change]:
        """Get all changes that passed validation"""
        return [c for c in self.changes if c.status == ChangeStatus.ACCEPTED]
    
    def get_rejected_changes(self) -> List[Change]:
        """Get all changes that failed validation"""
        return [c for c in self.changes if c.status == ChangeStatus.REJECTED]
    
    def get_total_ats_impact(self) -> float:
        """Calculate total estimated ATS score improvement"""
        return sum(c.ats_impact for c in self.get_accepted_changes())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert all changes to dict for JSON response"""
        return {
            "total_changes": len(self.changes),
            "accepted": len(self.get_accepted_changes()),
            "rejected": len(self.get_rejected_changes()),
            "total_ats_impact": round(self.get_total_ats_impact(), 2),
            "changes": [c.to_dict() for c in self.changes]
        }
    
    def apply_user_selections(self, selected_change_ids: List[str], latex_content: str) -> str:
        """
        Apply only user-selected changes to the resume
        This enables interactive undo/redo functionality
        """
        # Start with original
        result = latex_content
        
        # Apply only selected changes in order
        for change in self.changes:
            if change.id in selected_change_ids and change.status == ChangeStatus.ACCEPTED:
                result = result.replace(change.original_text, change.modified_text, 1)
        
        return result
