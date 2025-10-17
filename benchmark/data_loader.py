"""
Data Loader Module for Multi-Turn Benchmark Evaluation

Loads and parses the synthetic mental health dataset (JSONL format)
Extracts multi-turn conversations for evaluation
"""

import json
import pandas as pd
from typing import List, Dict


def load_dataset(file_path: str = 'data/synthetic_mental_health_dataset.jsonl') -> List[Dict]:
    """
    Load the JSONL dataset containing therapy sessions
    
    Args:
        file_path: Path to the JSONL file
        
    Returns:
        List of session dictionaries
    """
    sessions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            sessions.append(json.loads(line))
    return sessions


def parse_conversation_turns(input_text: str) -> List[Dict]:
    """
    Parse multi-turn conversation from the 'input' field
    
    Format:
        "Patient: X\nDoctor: Y\nPatient: Z\nDoctor: W"
    
    Returns:
        [
            {"turn": 1, "patient": "X", "doctor": "Y"},
            {"turn": 2, "patient": "Z", "doctor": "W"}
        ]
    """
    lines = input_text.strip().split('\n')
    turns = []
    current_patient = None
    turn_num = 0
    
    for line in lines:
        line = line.strip()
        if line.startswith('Patient:'):
            current_patient = line.replace('Patient:', '').strip()
        elif line.startswith('Doctor:') and current_patient:
            doctor_response = line.replace('Doctor:', '').strip()
            turn_num += 1
            turns.append({
                'turn': turn_num,
                'patient': current_patient,
                'doctor': doctor_response
            })
            current_patient = None
    
    return turns


def get_scenario_by_id(scenario_id: str, dataset_path: str = 'data/synthetic_mental_health_dataset.jsonl') -> Dict:
    """
    Get a specific scenario by patient_id or index
    
    Args:
        scenario_id: Patient ID or index number
        dataset_path: Path to dataset
        
    Returns:
        Session dictionary with parsed turns
    """
    sessions = load_dataset(dataset_path)
    
    # Try to find by patient_id
    for session in sessions:
        if session.get('patient_id') == scenario_id:
            session['turns'] = parse_conversation_turns(session['input'])
            return session
    
    # Try as index
    try:
        idx = int(scenario_id)
        if 0 <= idx < len(sessions):
            session = sessions[idx]
            session['turns'] = parse_conversation_turns(session['input'])
            return session
    except:
        pass
    
    return None


def get_all_scenarios(dataset_path: str = 'data/synthetic_mental_health_dataset.jsonl', 
                      condition: str = None,
                      limit: int = None) -> List[Dict]:
    """
    Get all scenarios, optionally filtered by condition
    
    Args:
        dataset_path: Path to dataset
        condition: Filter by condition (e.g., 'depression', 'anxiety')
        limit: Maximum number of scenarios to return
        
    Returns:
        List of session dictionaries with parsed turns
    """
    sessions = load_dataset(dataset_path)
    
    # Filter by condition if specified
    if condition:
        sessions = [s for s in sessions if s.get('condition') == condition]
    
    # Limit if specified
    if limit:
        sessions = sessions[:limit]
    
    # Parse turns for each session
    for session in sessions:
        session['turns'] = parse_conversation_turns(session['input'])
    
    return sessions


def get_scenario_summary(dataset_path: str = 'data/synthetic_mental_health_dataset.jsonl') -> pd.DataFrame:
    """
    Get summary statistics about the dataset
    
    Returns:
        DataFrame with scenario counts by condition, session, etc.
    """
    sessions = load_dataset(dataset_path)
    
    summary_data = []
    for session in sessions:
        turns = parse_conversation_turns(session['input'])
        summary_data.append({
            'patient_id': session.get('patient_id'),
            'condition': session.get('condition'),
            'session_id': session.get('session_id'),
            'num_turns': len(turns),
            'risk_flag': session.get('risk_flag'),
            'severity': session.get('session_state', {}).get('severity', 'N/A')
        })
    
    return pd.DataFrame(summary_data)


if __name__ == '__main__':
    # Test the data loader
    print("Testing data loader...")
    
    # Load all scenarios
    scenarios = get_all_scenarios(limit=5)
    print(f"\nLoaded {len(scenarios)} scenarios")
    
    # Show first scenario
    if scenarios:
        print(f"\nFirst scenario:")
        print(f"  Patient ID: {scenarios[0]['patient_id']}")
        print(f"  Condition: {scenarios[0]['condition']}")
        print(f"  Turns: {len(scenarios[0]['turns'])}")
        print(f"\n  First turn:")
        print(f"    Patient: {scenarios[0]['turns'][0]['patient'][:100]}...")
        print(f"    Doctor: {scenarios[0]['turns'][0]['doctor'][:100]}...")
    
    # Show summary
    summary = get_scenario_summary()
    print(f"\nDataset summary:")
    print(summary.groupby('condition').size())

