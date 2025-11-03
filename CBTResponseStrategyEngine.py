class CBTResponseStrategyEngine:
    def __init__(self):
        self.therapyapproaches = {
            "crisisintervention": {
                "priority": "immediate safety and stabilization",
                "techniques": ["grounding", "safety planning", "crisis resources"],
                "tone": "calm, directive, supportive"
            },
            "anxietyfocused": {
                "priority": "worry reduction and coping strategies",
                "techniques": ["breathing exercises", "cognitive restructuring", "exposure concepts"],
                "tone": "gentle, reassuring, educational"
            },
            "depressionfocused": {
                "priority": "behavioral activation and mood improvement",
                "techniques": ["activity scheduling", "thought records", "self-compassion"],
                "tone": "warm, encouraging, patient"
            },
            "traumainformed": {
                "priority": "safety, stabilization, processing",
                "techniques": ["grounding", "window of tolerance", "narrative therapy"],
                "tone": "careful, validating, empowering"
            },
            "relationshipfocused": {
                "priority": "communication and boundary setting",
                "techniques": ["interpersonal skills", "boundary setting", "attachment"],
                "tone": "balanced, insightful, practical"
            },
            "cognitiverestructuring": {
                "priority": "identifying and challenging thoughts",
                "techniques": ["thought challenging", "evidence examination", "balanced thinking"],
                "tone": "collaborative, curious, logical"
            }
        }

    def selectstrategy(self, emotionalanalysis):
        if emotionalanalysis["crisislevel"] == "high":
            return "crisisintervention"
        primaryemotions = emotionalanalysis.get("primaryemotions", [])
        if "trauma" in primaryemotions: return "traumainformed"
        if "anxiety" in primaryemotions: return "anxietyfocused"
        if "depression" in primaryemotions: return "depressionfocused"
        if "relationships" in primaryemotions: return "relationshipfocused"
        if emotionalanalysis.get("cognitivedistortions"):
            return "cognitiverestructuring"
        return "cognitiverestructuring"
