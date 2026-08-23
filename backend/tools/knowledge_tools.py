"""
CivicNexus AI — Causal Graph & Municipal Dependency Intelligence Engine
Traverses causal directed acyclic graphs (DAG) to isolate root-cause failure mechanisms
and sequences departmental response plans using Kahn's topological sorting.
"""

import json
import os
from typing import List, Dict, Any, Tuple, Set
from collections import deque

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


class CausalInferenceEngine:
    """Graph intelligence service for urban infrastructure cascade modeling."""

    @staticmethod
    def _read_data(filename: str) -> dict:
        target = os.path.join(DATA_DIR, filename)
        with open(target, "r", encoding="utf-8") as stream:
            return json.load(stream)

    @classmethod
    def load_departments(cls) -> dict:
        return cls._read_data("departments.json")

    @classmethod
    def load_dependencies(cls) -> dict:
        return cls._read_data("civic_dependencies.json")

    @classmethod
    def resolve_department(cls, issue_type: str) -> List[Dict[str, Any]]:
        """Maps an issue classification to its responsible municipal directorates."""
        config = cls.load_departments()
        mapping = config.get("issue_to_departments", {})
        registry = config.get("departments", {})

        codes = mapping.get(issue_type, [])
        assigned = []
        for code in codes:
            if code in registry:
                meta = dict(registry[code])
                meta["code"] = code
                assigned.append(meta)
        return assigned

    @classmethod
    def trace_root_cause_chain(cls, observed_issues: List[str]) -> Dict[str, Any]:
        """
        Executes depth-first/breadth-first causal graph walk over infrastructure dependency DAG.
        """
        dep_graph = cls.load_dependencies().get("dependencies", {})

        if len(observed_issues) <= 1:
            return {
                "chain": observed_issues,
                "confidence": 0.5,
                "evidence": ["Single isolated symptom observed - no antecedent cascade."],
            }

        # Build adjacency list with edge confidence ratings
        adj: Dict[str, List[Tuple[str, float, str]]] = {}
        for src, data in dep_graph.items():
            adj[src] = []
            for edge in data.get("can_cause", []):
                adj[src].append((edge["target"], edge["confidence"], edge["mechanism"]))

        distinct_issues = list(set(observed_issues))
        best_path: List[Dict[str, Any]] = []
        max_coverage = 0
        max_prob = 0.0
        target_set = set(distinct_issues)

        for origin in distinct_issues:
            if origin not in adj:
                continue

            init_node = [{"type": origin, "edge_confidence": 1.0, "mechanism": "Root cause epicenter"}]
            visited = {origin}
            queue = deque([(origin, init_node)])
            local_best = list(init_node)

            while queue:
                current_node, current_path = queue.popleft()
                for neighbor, weight, mechanism in adj.get(current_node, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_step = current_path + [{
                            "type": neighbor,
                            "edge_confidence": weight,
                            "mechanism": mechanism,
                        }]

                        cov = len(set(s["type"] for s in next_step) & target_set)
                        if cov > len(set(s["type"] for s in local_best) & target_set):
                            local_best = next_step

                        queue.append((neighbor, next_step))

            cov = len(set(s["type"] for s in local_best) & target_set)
            path_confidence = 1.0
            for step in local_best:
                path_confidence *= step.get("edge_confidence", 1.0)

            if cov > max_coverage or (cov == max_coverage and path_confidence > max_prob):
                best_path = local_best
                max_coverage = cov
                max_prob = path_confidence

        if best_path:
            types_order = [node["type"] for node in best_path]
            prob = 1.0
            for step in best_path:
                prob *= step.get("edge_confidence", 1.0)

            cov_ratio = len(set(types_order) & target_set) / max(len(target_set), 1)
            final_conf = round(prob * cov_ratio, 2)
            mechanisms = [n.get("mechanism", "") for n in best_path if n.get("mechanism")]

            return {
                "chain": types_order,
                "confidence": max(final_conf, 0.3),
                "evidence": mechanisms,
            }

        return {
            "chain": distinct_issues,
            "confidence": 0.3,
            "evidence": ["Spatio-temporal clustering indicates incident correlation, but direct hydraulic/structural path unverified."],
        }

    @classmethod
    def synthesize_response_sequence(cls, issues: List[str]) -> List[Dict[str, Any]]:
        """
        Determines topologically validated sequence of municipal department interventions.
        """
        config = cls.load_departments()
        issue_map = config.get("issue_to_departments", {})
        registry = config.get("departments", {})
        rules = config.get("department_dependencies", {})

        needed_depts: Set[str] = set()
        dept_issue_catalog: Dict[str, List[str]] = {}

        for issue in issues:
            for d_code in issue_map.get(issue, []):
                needed_depts.add(d_code)
                dept_issue_catalog.setdefault(d_code, []).append(issue)

        # Kahn's Topological Sort Algorithm
        in_degrees: Dict[str, int] = {d: 0 for d in needed_depts}
        graph: Dict[str, List[str]] = {d: [] for d in needed_depts}

        for d in needed_depts:
            prereqs = rules.get(d, {}).get("must_complete_after", [])
            for p in prereqs:
                if p in needed_depts:
                    graph[p].append(d)
                    in_degrees[d] += 1

        zero_in_queue = deque([d for d in needed_depts if in_degrees[d] == 0])
        ordered_depts: List[str] = []

        while zero_in_queue:
            curr = zero_in_queue.popleft()
            ordered_depts.append(curr)
            for succ in graph.get(curr, []):
                in_degrees[succ] -= 1
                if in_degrees[succ] == 0:
                    zero_in_queue.append(succ)

        for d in needed_depts:
            if d not in ordered_depts:
                ordered_depts.append(d)

        plan = []
        for idx, code in enumerate(ordered_depts):
            d_info = registry.get(code, {})
            d_issues = dept_issue_catalog.get(code, [])
            d_rules = rules.get(code, {})

            plan.append({
                "step_number": idx + 1,
                "department": code,
                "department_name": d_info.get("name", code),
                "issues": d_issues,
                "action": f"Address {', '.join(d_issues)} operational failures",
                "reason": d_rules.get("reason", "Standard municipal response sequencing"),
                "depends_on": d_rules.get("must_complete_after", []),
                "sla_hours": d_info.get("sla_hours", {}),
                "resources": d_info.get("resources", []),
            })

        return plan


# ── Functional Wrappers for Complete Backward Compatibility ────────────────────

def get_departments() -> dict:
    return CausalInferenceEngine.load_departments()


def get_dependencies() -> dict:
    return CausalInferenceEngine.load_dependencies()


def get_department_for_issue(issue_type: str) -> List[Dict[str, Any]]:
    return CausalInferenceEngine.resolve_department(issue_type)


def get_department_dependencies() -> Dict[str, Dict]:
    return CausalInferenceEngine.load_departments().get("department_dependencies", {})


def find_causal_chain(issue_types: List[str]) -> Dict[str, Any]:
    return CausalInferenceEngine.trace_root_cause_chain(issue_types)


def get_response_order(issue_types: List[str]) -> List[Dict[str, Any]]:
    return CausalInferenceEngine.synthesize_response_sequence(issue_types)
