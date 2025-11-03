class CBTResponseStrategyEngine:
    """
    This class is designed to act as the brain of our application. 
    It takes an emotional analysis as input and uses a set of rules to select 
    the most appropriate therapeutic strategy from a predefined library. 
    This ensures that the response is tailored to the user's immediate needs, 
    prioritizing crisis intervention above all else.
    """
    
    def __init__(self):
        """
        Initialize the strategy engine with a comprehensive library of 
        therapeutic approaches, each with defined priorities, techniques, and tones.
        """
        self.therapy_approaches = {
            "crisis_intervention": {
                "priority": "immediate safety and stabilization",
                "techniques": ["grounding", "safety planning", "crisis resources"],
                "tone": "calm, directive, supportive"
            },
            "anxiety_focused": {
                "priority": "worry reduction and coping strategies",
                "techniques": ["breathing exercises", "cognitive restructuring", "exposure concepts"],
                "tone": "gentle, reassuring, educational"
            },
            "depression_focused": {
                "priority": "behavioral activation and mood improvement",
                "techniques": ["activity scheduling", "thought records", "self-compassion"],
                "tone": "warm, encouraging, patient"
            },
            "trauma_informed": {
                "priority": "safety, stabilization, processing",
                "techniques": ["grounding", "window of tolerance", "narrative therapy"],
                "tone": "careful, validating, empowering"
            },
            "relationship_focused": {
                "priority": "communication and boundary setting",
                "techniques": ["interpersonal skills", "boundary setting", "attachment"],
                "tone": "balanced, insightful, practical"
            },
            "cognitive_restructuring": {
                "priority": "identifying and challenging thoughts",
                "techniques": ["thought challenging", "evidence examination", "balanced thinking"],
                "tone": "collaborative, curious, logical"
            }
        }

    def select_strategy(self, emotional_analysis):
        """
        Core decision-making method that selects the most appropriate 
        therapeutic strategy based on emotional analysis.
        
        Design Principle: Hierarchical Triage Logic
        ============================================
        
        1. SAFETY FIRST - Crisis Detection
           - If crisislevel == "high", immediately return "crisis_intervention"
           - This ensures that safety is the absolute top priority,
             overriding all other emotional indicators.
        
        2. EMOTION-BASED SELECTION
           - After ensuring safety, examine primary emotions detected by
             the EmotionalIntelligenceEngine.
           - Each primary emotion maps to a specific strategy:
             * trauma → trauma_informed
             * anxiety → anxiety_focused
             * depression → depression_focused
             * relationships → relationship_focused
        
        3. COGNITIVE DISTORTION FALLBACK
           - If no primary emotion is detected but cognitive distortions are present,
             use cognitive_restructuring (the core CBT technique).
        
        4. DEFAULT APPROACH
           - If none of the above conditions apply,
             return cognitive_restructuring as a safe, generally helpful approach.
        
        Args:
            emotional_analysis (dict): Output from EmotionalIntelligenceEngine.
                                       Contains: primaryemotions, sentiment, 
                                       cognitivedistortions, crisislevel
        
        Returns:
            str: Strategy name (one of the keys in self.therapy_approaches)
        """
        
        # RULE 1: SAFETY FIRST
        if emotional_analysis["crisislevel"] == "high":
            return "crisis_intervention"
        
        # RULE 2: EMOTION-BASED STRATEGY SELECTION
        primary_emotions = emotional_analysis.get("primaryemotions", [])
        
        if primary_emotions:
            # Check emotions in order of clinical severity
            if "trauma" in primary_emotions:
                return "trauma_informed"
            elif "anxiety" in primary_emotions:
                return "anxiety_focused"
            elif "depression" in primary_emotions:
                return "depression_focused"
            elif "relationships" in primary_emotions:
                return "relationship_focused"
        
        # RULE 3: COGNITIVE DISTORTION FALLBACK
        if emotional_analysis.get("cognitivedistortions"):
            return "cognitive_restructuring"
        
        # RULE 4: DEFAULT APPROACH
        # Cognitive restructuring is a foundational CBT technique,
        # always applicable and therapeutically sound.
        return "cognitive_restructuring"
