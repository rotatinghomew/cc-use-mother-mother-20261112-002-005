from __future__ import annotations
from typing import Any
from four_level_wakeup_hub.directory.runtime import RunState, SQLiteLedger, fingerprint, number, sequence

class DeliverySupervisor:
    artifact_key = 'delivery_cycle'

    def execute(self, state: RunState, stages: list[Any], ledger: SQLiteLedger) -> None:
        delivery_states = []
        for position, stage in enumerate(stages):
            stage.apply(state)
            artifact = state.artifacts[stage.name]
            delivery_states.append({"sequence": position + 1, "stage": stage.name, "score": artifact["score"], "retry_required": artifact["failed_rules"] > 7})
            ledger.save(state)
        retries = [item for item in delivery_states if item["retry_required"]]
        acknowledgements = max(0, int(number(state.payload.get("count"))) - len(retries))
        state.artifacts[self.artifact_key] = {"delivery_states": delivery_states, "retry_queue": retries, "acknowledged_estimate": acknowledgements, "signature": fingerprint(delivery_states)}
        state.emit(self.artifact_key, "delivery_cycle_completed", retries=len(retries))
