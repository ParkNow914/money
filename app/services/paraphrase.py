"""
Paraphrase and content variation service.

Provides simple text variation to improve content originality.
In production, could integrate with LLM or specialized paraphrasing APIs.
"""

import random
import re


class Paraphraser:
    """Simple paraphrasing service for content variation."""
    
    # Simple synonym mappings for demonstration
    SYNONYMS = {
        "important": ["crucial", "vital", "essential", "significant"],
        "good": ["excellent", "great", "outstanding", "remarkable"],
        "bad": ["poor", "subpar", "inadequate", "unfavorable"],
        "big": ["large", "substantial", "significant", "considerable"],
        "small": ["little", "modest", "minor", "compact"],
        "help": ["assist", "aid", "support", "facilitate"],
        "show": ["demonstrate", "illustrate", "display", "reveal"],
        "use": ["utilize", "employ", "apply", "leverage"],
        "make": ["create", "produce", "generate", "develop"],
        "get": ["obtain", "acquire", "achieve", "gain"],
    }
    
    def paraphrase_sentence(self, sentence: str, variation_level: float = 0.3) -> str:
        """
        Paraphrase a sentence with simple word substitution.
        
        Args:
            sentence: Input sentence
            variation_level: Probability of replacing each word (0.0-1.0)
        
        Returns:
            Paraphrased sentence
        """
        words = sentence.split()
        result = []
        
        for word in words:
            # Clean word
            word_clean = re.sub(r'[^\w]', '', word.lower())
            
            # Check if we should vary this word
            if random.random() < variation_level and word_clean in self.SYNONYMS:
                # Get synonym
                synonyms = self.SYNONYMS[word_clean]
                replacement = random.choice(synonyms)
                
                # Preserve capitalization
                if word[0].isupper():
                    replacement = replacement.capitalize()
                
                result.append(replacement)
            else:
                result.append(word)
        
        return " ".join(result)
    
    def paraphrase_text(self, text: str, variation_level: float = 0.2) -> str:
        """
        Paraphrase multiple sentences.
        
        Args:
            text: Input text (multiple sentences)
            variation_level: Probability of replacing words
        
        Returns:
            Paraphrased text
        """
        # Split into sentences
        sentences = re.split(r'([.!?]+\s+)', text)
        
        result = []
        for i, part in enumerate(sentences):
            if i % 2 == 0:  # Actual sentence (not delimiter)
                result.append(self.paraphrase_sentence(part, variation_level))
            else:  # Delimiter
                result.append(part)
        
        return "".join(result)
    
    def check_similarity(self, text1: str, text2: str) -> float:
        """
        Simple similarity check between two texts.
        
        Returns similarity score 0.0-1.0 (higher = more similar).
        In production, use proper similarity metrics or embeddings.
        """
        # Simple word-based similarity
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)


# Singleton instance
paraphraser = Paraphraser()
