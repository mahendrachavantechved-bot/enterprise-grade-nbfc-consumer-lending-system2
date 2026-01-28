def run_credit_flow(config: dict, input_data: dict):
    bureau_score = input_data.get("bureau_score", 650)
    internal_score = input_data.get("internal_score", 620)

    composite = round(
        (config["composite_risk_score"]["bureau_weight"] * bureau_score) +
        (config["composite_risk_score"]["internal_weight"] * internal_score),
        -1
    )

    band = None
    for b in config["visualization_rules"]["score_bands"]:
        if b["min"] <= composite <= b["max"]:
            band = b
            break

    # Phase-2: Risk Flags
    flags = []
    if input_data.get("overdue_days", 0) >= 30:
        flags.append("SMA / NPA Risk")

    if input_data.get("emi_to_income", 0) > 55:
        flags.append("High EMI Burden")

    if input_data.get("device_risk") == "high":
        flags.append("High Device Risk")

    return {
        "bureau_score": bureau_score,
        "internal_score": internal_score,
        "composite_score": composite,
        "risk_band": band,
        "risk_flags": flags[:3]
    }
