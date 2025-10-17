"""
Multi-Turn Conversation Evaluator

Evaluates AI chatbot responses across multiple turns of conversation
Compares against reference (human counselor) responses
"""

from benchmark.evaluation import *
from benchmark.config import *
from typing import List, Dict
import pandas as pd


class MultiTurnEvaluator:
    """
    Evaluates multi-turn therapy conversations
    """
    
    def __init__(self):
        """Initialize evaluator with metrics from evaluation module"""
        self.metrics = {
            'rouge': calculate_average_rouge,
            'meteor': calculate_meteor,
            'ethical_alignment': evaluate_ethical_alignment,
            'sentiment_distribution': evaluate_sentiment_distribution,
            'inclusivity': evaluate_inclusivity_score,
            'complexity': evaluate_complexity_score
        }
    
    def evaluate_turn(self, reference_response: str, ai_response: str) -> Dict:
        """
        Evaluate a single turn against reference
        
        Args:
            reference_response: Human counselor's response
            ai_response: AI-generated response
            
        Returns:
            Dictionary of metric scores for this turn
        """
        scores = {
            'rouge_score': calculate_average_rouge(reference_response, ai_response),
            'meteor_score': calculate_meteor(reference_response, ai_response),
            'ethical_alignment': evaluate_ethical_alignment(ai_response),
            'sentiment_distribution': evaluate_sentiment_distribution(
                reference_response, ai_response, EMOTION_WEIGHTS
            ),
            'inclusivity_score': evaluate_inclusivity_score(ai_response),
            'complexity_score': evaluate_complexity_score(ai_response, READABILITY_CONSTANTS)
        }
        
        return scores
    
    def evaluate_conversation(self, 
                            reference_turns: List[Dict], 
                            ai_turns: List[Dict]) -> Dict:
        """
        Evaluate entire multi-turn conversation
        
        Args:
            reference_turns: List of reference turns [{"turn": 1, "patient": "...", "doctor": "..."}]
            ai_turns: List of AI turns [{"turn": 1, "patient": "...", "ai_response": "..."}]
            
        Returns:
            {
                'turn_scores': [...],  # Per-turn evaluation
                'aggregate_scores': {...},  # Average across all turns
                'metadata': {...}  # Session info
            }
        """
        turn_scores = []
        
        # Evaluate each turn
        for ref_turn, ai_turn in zip(reference_turns, ai_turns):
            if ref_turn['turn'] != ai_turn['turn']:
                print(f"Warning: Turn mismatch - Ref: {ref_turn['turn']}, AI: {ai_turn['turn']}")
            
            scores = self.evaluate_turn(ref_turn['doctor'], ai_turn['ai_response'])
            scores['turn'] = ref_turn['turn']
            scores['patient_message'] = ref_turn['patient']
            scores['reference_response'] = ref_turn['doctor']
            scores['ai_response'] = ai_turn['ai_response']
            
            turn_scores.append(scores)
        
        # Calculate aggregate scores (average across turns)
        aggregate_scores = self._calculate_aggregate_scores(turn_scores)
        
        return {
            'turn_scores': turn_scores,
            'aggregate_scores': aggregate_scores,
            'metadata': {
                'total_turns': len(turn_scores),
                'model': ai_turns[0].get('model', 'Unknown') if ai_turns else 'Unknown'
            }
        }
    
    def _calculate_aggregate_scores(self, turn_scores: List[Dict]) -> Dict:
        """Calculate average scores across all turns"""
        if not turn_scores:
            return {}
        
        metrics = ['rouge_score', 'meteor_score', 'ethical_alignment', 
                  'sentiment_distribution', 'inclusivity_score', 'complexity_score']
        
        aggregates = {}
        for metric in metrics:
            values = [turn[metric] for turn in turn_scores if metric in turn]
            aggregates[f'avg_{metric}'] = round(sum(values) / len(values), 3) if values else 0.0
            aggregates[f'min_{metric}'] = round(min(values), 3) if values else 0.0
            aggregates[f'max_{metric}'] = round(max(values), 3) if values else 0.0
        
        return aggregates
    
    def evaluate_dataset(self, 
                        sessions: List[Dict], 
                        ai_responses_per_session: List[List[Dict]]) -> pd.DataFrame:
        """
        Evaluate multiple sessions
        
        Args:
            sessions: List of session dicts with parsed turns
            ai_responses_per_session: List of AI response lists (one per session)
            
        Returns:
            DataFrame with all evaluation results
        """
        all_results = []
        
        for session, ai_responses in zip(sessions, ai_responses_per_session):
            result = self.evaluate_conversation(session['turns'], ai_responses)
            
            # Add session metadata
            result['patient_id'] = session.get('patient_id')
            result['condition'] = session.get('condition')
            result['session_id'] = session.get('session_id')
            result['risk_flag'] = session.get('risk_flag')
            
            all_results.append(result)
        
        return all_results
    
    def export_results_to_csv(self, results: List[Dict], output_path: str):
        """
        Export evaluation results to CSV
        
        Args:
            results: List of evaluation results
            output_path: Path to save CSV
        """
        # Flatten results for CSV export
        rows = []
        for result in results:
            base_row = {
                'patient_id': result.get('patient_id'),
                'condition': result.get('condition'),
                'session_id': result.get('session_id'),
                'risk_flag': result.get('risk_flag'),
                'total_turns': result['metadata']['total_turns'],
                'model': result['metadata']['model']
            }
            
            # Add aggregate scores
            base_row.update(result['aggregate_scores'])
            
            rows.append(base_row)
        
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False)
        print(f"✅ Results exported to {output_path}")
        
        return df
    
    def export_turn_by_turn_to_csv(self, results: List[Dict], output_path: str):
        """
        Export detailed turn-by-turn results to CSV
        
        Args:
            results: List of evaluation results
            output_path: Path to save CSV
        """
        rows = []
        for result in results:
            patient_id = result.get('patient_id')
            condition = result.get('condition')
            
            for turn_score in result['turn_scores']:
                row = {
                    'patient_id': patient_id,
                    'condition': condition,
                    'turn': turn_score['turn'],
                    'patient_message': turn_score['patient_message'][:100],  # Truncate for CSV
                    'reference_response': turn_score['reference_response'][:100],
                    'ai_response': turn_score['ai_response'][:100],
                    'rouge_score': turn_score['rouge_score'],
                    'meteor_score': turn_score['meteor_score'],
                    'ethical_alignment': turn_score['ethical_alignment'],
                    'sentiment_distribution': turn_score['sentiment_distribution'],
                    'inclusivity_score': turn_score['inclusivity_score'],
                    'complexity_score': turn_score['complexity_score']
                }
                rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False)
        print(f"✅ Turn-by-turn results exported to {output_path}")
        
        return df

