# -*- coding: utf-8 -*-
"""Interstitial Lactate & Anaerobic Threshold Pacer for GenPark Personal Agent."""
import json
from typing import Dict, Any

class InterstitialLactateAnaerobicPacer:
    @staticmethod
    def evaluate_interstitial_lactate_dynamics(lactate_mmol_l: float, current_power_or_pace: float = 0.0, time_in_zone_minutes: float = 10.0) -> Dict[str, Any]:
        if lactate_mmol_l < 2.0:
            domain = "AEROBIC_LIPOLYTIC_BASE (LT1 / Zone 2)"
            fatigue_rate = "Negligible muscular acidosis; sustainable for multi-hour durations."
        elif lactate_mmol_l <= 4.0:
            domain = "MAXIMAL_LACTATE_STEADY_STATE (MLSS / Zone 3-4)"
            fatigue_rate = "Equilibrium between lactate production and oxidation; sustainable for 45-60 min."
        else:
            domain = "SEVERE_ANAEROBIC_GLYCOLYTIC (Above OBLA)"
            fatigue_rate = "Rapid proton (H+) accumulation and contractile failure within 2-10 minutes."
            
        return {
            "lactate_reading_mmol_l": lactate_mmol_l,
            "metabolic_intensity_domain": domain,
            "acidosis_projection": fatigue_rate,
            "governor_action": "THROTTLE_BACK_TO_LT1" if lactate_mmol_l > 4.0 else "SUSTAIN_TARGET_EFFORT"
        }

    @staticmethod
    def calculate_lactate_clearance_recovery_pace(threshold_watts: int, lactate_peak_mmol: float = 8.0) -> Dict[str, Any]:
        clearance_watts = round(threshold_watts * 0.55, 0)
        return {
            "lactate_clearance_power_watts": clearance_watts,
            "clearance_intensity_window": f"{int(clearance_watts*0.9)}W - {int(clearance_watts*1.1)}W",
            "clearance_duration_min": 15,
            "physiological_rationale": "55% threshold preserves cardiac output and capillary perfusion, accelerating lactate oxidation in slow-twitch fibers vs passive resting."
        }
